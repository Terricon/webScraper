"""Create a command-line application that, given a list of website URLs as input, visits them and finds,
extracts and outputs the websites’ logo image URLs and all phone numbers (e.g. mobile phones,
land lines, fax numbers) present on the websites.
"""

# IMPORT THE DEPENDENCIES THAT THE PROGRAM RELIES ON
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import urllib.parse
import re


# CREATED THE FUNCTION TO RUN THE SAME CODE ON ALL THE WEBSITES THAT ARE LISTED ON THE TEXT DOCUMENT
def find_info(website, driver):
    # print(website)

    # ACCESSES THE WEBSITE THAT IS PASSED TO THE FUNCTION
    driver.get(website)

    # RETURNS THE PAGE SOURCE HTML AND THEN PARSES IT USING BEAUTIFUL SOUP
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    # FIND THE BASE URL DIRECTORY OF FILES, IF THERE IS A BASE, ADD IT TO THE URL
    logo_path = ""
    web_dir = website
    base = soup.find_all('base')
    if base:
        in_dir = base[0]['href']
        web_dir = urllib.parse.urljoin(website, in_dir)
        # print(web_dir)

    # FINDS ALL IMAGES IN THE HTML, AND CREATES A SET OF THEM
    images = soup.find_all('img')
    images = set(images)
    # print(images)

    # RUNS THROUGH ALL THE IMAGES THAT THE PROGRAM FINDS ON THE COMPUTER
    # PRIORITIZES THE 'LOGO' KEYWORD, BUT WILL ITERATE THROUGH ALL IMAGES
    if images:

        # CHOOSE THE LOWEST LENGTH LOGO
        low_len = 100

        for image in images:
            # print(image['src'])

            # CHECK TO SEE IF THE IMAGE ACTUALLY HAS THE KEYWORD LOGO IN IT
            if 'logo' in os.path.basename(image['src']):
                # print(image)
                temp_logo_path = image['src']

                # PREPARE SOME VALIDATION VARIABLES
                text, extension = os.path.splitext(os.path.basename(temp_logo_path))

                # FIND THE CURRENT LENGTH OF THE NAME
                curr_len = len(text)

                # CHECK THAT THE CURRENT LENGTH IS LOWER THAN THE LOWEST LENGTH
                if curr_len < low_len:  # FOR ASU THIS MEANS THAT IT RETURNS AN OBJECTIVELY WORSE LOGO, ATTEMPT SOLUTION
                    low_len = curr_len

                    # MERGE THE TWO URLS TOGETHER TO CREATE A FINAL COMPLETE ONE
                    logo_path = urllib.parse.urljoin(web_dir, temp_logo_path)
                    # print(abs_file_path)

                    # CHECK TO SEE IF THE IMAGE HAS THE LITERAL NAME LOGO
                    if text == 'logo':
                        # print(logo_path)
                        break

            # CHECKS IF THE IMAGE IS AN ICON
            elif 'icon' in os.path.basename(image['src']):  # check to see if the image is an icon or labeled as an icon
                temp_logo_path = image['src']

                # ADD THE TWO URLS TOGETHER
                logo_path = urllib.parse.urljoin(web_dir, temp_logo_path)

    # EXTRACTS TEXT FROM THE HTML FOR PROCESSING
    extracted_text = soup.get_text(strip=True)
    # print(extracted_text)

    # SETTING THE COMPILING SETTINGS FOR REGEX EXTERNALLY SO THAT IT IS NOT REPEATEDLY RESET
    compiled_settings = r".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?"
    phone_number = []

    # FIND THE NUMBERS THAT ARE HELD WITHIN THE HTML TEXT
    numbers = re.findall(compiled_settings, extracted_text)

    # CLEAN OUT THE NUMBERS
    for x in range(0, len(numbers)):
        numbers[x] = re.sub("\D", "", numbers[x])
    numbers = set(numbers)
    for num in numbers:
        f_phone_num = f"+({num[:3]}) {num[3:6]} {num[6:]}"
        phone_number.append(f_phone_num)

    # CHECK TO SEE IF THE PHONE NUMBER IS EMPTY
    if not phone_number:
        phone_number.append("None")

    # CHECK TO SEE IF THERE IS A LOGO PATH
    if not logo_path:

        # USING CLEAR BIT API TO RETURN THE LOGO IMAGE FOR THE WEBSITE
        new_website = urllib.parse.urlparse(website)
        driver.get("https://logo.clearbit.com/" + new_website.netloc)
        clear_api_html = BeautifulSoup(driver.page_source, 'html.parser')
        clear_logo_access = clear_api_html.find_all('img')

        # EDGE CASE DEFENSE
        try:
            logo_path = clear_logo_access[0]['src']
        except IndexError:
            logo_path = "This website has no logo"

    # CREATE THE OUTPUT FORMATTING FOR THE PRINTING
    output_dict = {'Phone numbers': phone_number, 'Logo': logo_path, 'Website': website}

    print(output_dict)


def main():
    # INITIALIZE THE DRIVER THAT IS USED TO ACCESS WEBSITES
    driver = webdriver.Chrome(r"C:\Users\Tal\anaconda3\envs\textModel\chromedriver.exe")

    # OPENS THE FILE THAT WILL CONTAIN ALL THE LINKS THAT WILL BE ITERATED THROUGH
    with open('websites.txt', 'r') as links_doc:
        web_links = links_doc.readlines()
        # print(web_links)
    for link in web_links:
        link = link.strip()
        find_info(link, driver)

    # # SINGLE URL TESTING PURPOSES
    # link = "https://www.westvalley.edu/contact/"
    # find_info(link, driver)

    driver.close()


if __name__ == "__main__":
    main()

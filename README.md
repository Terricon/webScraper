# Web scraping for company logos and phone numbers
Code to scrape websites for logos and for any telephone numbers that it can find

## How the code works
The code works when it is fed a text file, reads the text file, and then outputs the phone numbers that it found on the website as well as the website logo if there is one, if the code cannot detect the website logo, it uses the clear bit api to find a logo, and then outputs a hyperlink to the logo from there. The output also includes the website link itself.

## Things to add
Better international functionality. currently the regex filter is a dumb filter, and cannot differentiate between American and non-American numbers, and would require a check to see what country the website is from to adjust filtering. 

Command line controls. The program needs to be run from the command line, but this functionality has not been implemented yet

User based chrome driver detection. The program currently relies on an absolute path to a chrome driver that will need to be optimized so that users can put their chrome drivers anywhere without needing to specify the absolute path of the driver

## Know issues
Currently lacking in international phone number capabilities and has some issues detecting the best possible logo, as well as logos that do not include 'logo' within their filename.

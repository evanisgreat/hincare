This repo is for HINCare, a project by the STAR Lab in the University of Hong Kong

Each folder contains a web-scraper named after the websites they are scraping

All scrapers utilize the Python Scrapy Framework

Each web-scraper generates a dictionary, representing different fields provided by the website for each activity

To map out the events into a JSON file run the following command:

scrapy crawl [spider_name] -O [file_name].json

The spider name can be found in the code

Error code names in json file:
'*' - Missing Data
'@' - Wrong Formatting
'#' - Multiple Data Points

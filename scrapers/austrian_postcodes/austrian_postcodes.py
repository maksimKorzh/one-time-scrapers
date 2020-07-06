#########################################################
#
# Script to scrape Austrian postal codes from wikipedia
#                        
#                         by
#
#                   Code Monkey King
#
#########################################################

# packages
import requests
from bs4 import BeautifulSoup

# URL to crawl
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_in_Austria'

# make HTTP GET request
response = requests.get(url)

# parse content
content = BeautifulSoup(response.text, 'lxml')

# extract postal codes
postcodes = [
                postcode.text for postcode in content.find_all('li')
                if ' - ' in postcode.text
            ]

# filter postal codes
postcodes = [
    postcode.split()[0]
    for postcode in postcodes
    if len(postcode.split()) in [3, 4]
]


# write output to file
with open('austrian_postcodes.txt', 'a') as f:
    # loop over list of extracted postal codes
    for postcode in postcodes:
        f.write(postcode + '\n')
    
    
    
    
    
    
    
    
    
    
    
    
    

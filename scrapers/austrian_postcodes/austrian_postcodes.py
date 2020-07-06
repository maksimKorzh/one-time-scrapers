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

# extract and filter postcodes
postcodes = [postcode.split()[0] for postcode in content.find_all('li')
             if '-' in postcode.text and len(postcode.split()) in [3, 4]
        

# write output to file
with open('austrian_postcodes.txt', 'a') as f:
    f.write('\n'.join(postcodecs))
    
    
    
    
    
    
    
    
    
    
    
    
    

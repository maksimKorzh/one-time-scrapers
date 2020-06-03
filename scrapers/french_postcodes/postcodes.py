#########################################
#
# Script to scrape French postal codes
#   from GitHub (from user "ggouv")
#
#                  by
#
#           Code Monkey King
#
#########################################

# import Tiny Scraper
from ts import *

'''
# tagret URL
url = 'https://raw.githubusercontent.com/ggouv/Villes-de-France/master/villes_data.sql'

# make HTTP request to the target URL
content = parse(url)

# store response text to local file
with open('postcodes_raw.txt', 'w') as f:
    f.write(content['text'])
'''

# parse local postcodes copy
content = parse('postcodes_raw.txt')['text']

# extract postal codes
postcodes = [
    [
        item.strip()
        for item in
        postcode[0:-1].strip('()').replace("'", '').split(',')
    ]
    for postcode in
    content.split('\n')[18:]
    if 'INSERT' not in postcode
]

# loop over postcodes
for postcode in postcodes:
    # create postcode string
    postcode_string = postcode[3] + '_' 
    postcode_string += postcode[0]

    # append article to postcode string if available
    if postcode[2] != '':
        postcode_string = postcode[2] + ' ' + postcode_string
    
    # write postcodes to file
    with open('postcodes.txt', 'a') as f:
        f.write(postcode_string + '\n')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

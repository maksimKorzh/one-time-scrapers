################################################
#
# Script to scrape all postal codes in Spain
#              from wikipedia
#
#                    by
#
#             Code Monkey King
#
################################################

# import packages
import requests
from bs4 import BeautifulSoup

# target URL
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_in_Spain#10000%E2%80%9310999:_C%C3%A1ceres'

# make HTTP GET request to target URL
response = requests.get(url)

# parse HTML response
content = BeautifulSoup(response.text, 'lxml')

# extract all the list items
items = [
    item.text.split(' – ')[0]
    for item in
    content.find_all('li')
    if ' – ' in item.text
][0: -1]

# postcodes list
postcodes = []

# loop over scraped items
for item in items:
    # extract postcodes list
    postcodes_list = item.split(', ')
    
    # extract single postcode items
    if len(postcodes_list) == 1 and '–' not in item:
        if ' through ' not in item and 'to' not in item:
            postcodes.append(item)
        
        if 'to' in item:
            # extract "to" range
            from_range = int(item.split(' to ')[0])
            to_range = int(item.split(' to ')[1])
            
            # loop over "to" range
            for postcode in range(from_range, to_range + 1):
                postcodes.append(postcode)
    
    else:
        # loop over postcodes sub list
        for postcode in postcodes_list:
            # extract postcodes range
            postcodes_range = postcode.split('–')

            #print(postcodes_range)
            if len(postcodes_range) == 1:
                if ' through ' not in postcodes_range[0]:
                    postcodes.append(postcodes_range[0])

                else:
                    # extract through range
                    through_range = postcodes_range[0].split(' through ')
                    from_postcode = int(through_range[0])
                    to_postcode = int(through_range[1])

                    # loop over through range
                    for through_range_postcode in range(from_postcode, to_postcode + 1):
                        postcodes.append(through_range_postcode)
            
            else:
                # extract postcodes ranges
                from_postcodes_range = int(postcodes_range[0])
                to_postcodes_range = int(postcodes_range[1])
                
                # loop over postcodes ranges
                for postcode_range in range(from_postcodes_range, to_postcodes_range + 1):
                    postcodes.append(postcode_range)


# loop over scraped postcodes
for postcode in postcodes:
    # write postcode to "postcodes.txt"
    with open('postcodes.txt', 'a') as f:
        f.write(str(postcode) + '\n')

















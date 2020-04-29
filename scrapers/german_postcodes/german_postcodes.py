# packages
import requests
from bs4 import BeautifulSoup
import json

# base URL
base_url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_in_Germany'

# make HTTP GET request to base URL
res = requests.get(base_url)

# parse response
content = BeautifulSoup(res.text, 'lxml')

# postcodes list
postcodes = []

# data extraction logic
for ul in content.find_all('ul')[19:217]:
    
    for li in ul.find_all('li'):
        if li.text.split()[-1] != '\u2013':
            # extract postcodes
            item = {
                'postcode': li.text.split()[0],
                'region': li.text.split()[-1]
            }
            
            # fix double postcodes
            if '\u2013' in item['postcode']:
                item['postcode'] = item['postcode'].split('\u2013')[0]
            
            # append item to postcodes list
            postcodes.append(item)

# convert postcodes to string
postcodes = json.dumps(postcodes, indent=2)

# write postcodes to JSON file
with open('german_postcodes.json', 'w') as f:
    f.write(postcodes)

# print results
print(postcodes)
print('\nwritten %s postcodes to "german_postcodes.json" file' % len(json.loads(postcodes)))




























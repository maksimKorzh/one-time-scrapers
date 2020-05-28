#########################################
#
# Script to scrape Italian postal codes
#           from wikipedia
#
#                 by
#
#          Code Monkey King
#
#########################################

# packages
import requests
from bs4 import BeautifulSoup
import re

# target URL
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_in_Italy'

# make HTTP request to the target URL
response = requests.get(url)

# parse HTML document
content = BeautifulSoup(response.text, 'lxml')

# extract postcodes table
table = content.find('table') # .find('table', {'class': 'wikitable sortable'})

# extract table rows
rows = table.find_all('tr')

# extract row columns
cols = [
    [
        col.text.strip('\n')
        for col in
        row.find_all('td')
    ]
    
    for row in
    rows
]

# init raw data postcodes list
raw_data = []

# init postcodes list
postcodes = []

# loop over postcode columns
for col in cols[1:]:
    raw_data.append(col[3])
    raw_data.append(col[4])

# loop over postcodes
for item in raw_data:
    # extract capital towns' postcodes
    if len(item.split()) == 1 and item != '-':
        postcodes.append(item)

# extract raw postcode ranges
ranges = re.findall(r'(\d+ to \d+)', '\n'.join(raw_data))

# loop over raw postcode ranges
for item in ranges:
    from_range = int(item.split(' to ')[0])
    to_range = int(item.split(' to ')[1])
    
    # loop over current range
    for postcode in range(from_range, to_range + 1):
        postcodes.append(str(postcode).zfill(5))

# extract raw postcode set
sets = re.findall(r'(\d+)?,(\d+)', '\n'.join(raw_data))
sets = ','.join([','.join(item) for item in sets]).replace(',,', ',')
sets = sets.split(',')

# loop over postcode sets
for postcode in sets:
    postcodes.append(postcode)

# extract all the left sets
other_sets = re.findall(r'(\d+ \(.+\), \d+ \(.+\))', '\n'.join(raw_data))

# loop over left sets
for item in other_sets:
    raw = [text.split() for text in item.split(',')]
    
    # loop over raw lists
    for postcode in raw:
        postcodes.append(postcode[0])

# loop over postcodes
for postcode in postcodes:
    # write postcodes to file
    with open('postcodes.txt', 'a') as f:
        f.write(postcode + '\n')
    












##############################
#
# Beautiful Soup cheat sheet
#
#            by
#
#     Code Monkey King
#
##############################

# Step 1: import packages
import requests
from bs4 import BeautifulSoup

# Step 2: define target URL
url = 'https://podsearch.com/listing/car-talk.html'

# Step 3: make HTTP request to the target URL
response = requests.get(url)

# Step 4: parse entire HTML document
content = BeautifulSoup(response.text, 'lxml')

# Step 5: parse PARENT element conteining needed data
parent = content.find('div', {'class': 'col-md-8 col-sm-12 col-xs-12 pdl0'})

# Step 6: parse CHILD element containing the exact data we need
child = parent.find('span').text

# Step 7: split the target string if needed
data = child.split(': ')[-1]

# Step 8: print data to console
print(data)

#####################################
#
# Useful data extraction techniques
#
#####################################

# extract FIRST data occurence by unique class
description = content.find('p', {'class': 'pre-line'}).text
print('\n', description)

# extract ALL data occurences by unique class
text = [
    item.text
    for item in
    content.find_all('p', {'class': 'pre-line'})
]
print('\n', text)

# reference similar data occurences by index
print('\n', text[0])
print('\n', text[1])

# join list elements into one single string by whatever character
print('\n', '\n joined by new line \n'.join(text))

# reference element by whatever attribute (ID in this case)
button = content.find('button', {'id': 'headerSearchButton'}).text
print(button)

# extract FIRST other but textual node data element, e.g. HREF attribute or whatever
link = content.find('a')['href']
print(link)

# extract ALL other but textual node data elements, e.g. HREF attribute or whatever
links = [
    link['href']
    for link in
    content.find_all('a')
    # filter on condition if needed
    #if link['href'] == 'https://podsearch.com/listing/rethinking-weight-loss.html'
]
print(links)
















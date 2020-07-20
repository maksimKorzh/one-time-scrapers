#############################################
#
#    Sacrilegious web scraping challenge
#
#                 solved by
#
#              Code Monkey King
#
#############################################


# packages
import requests
from bs4 import BeautifulSoup
import json
import csv

# make HTTP GET request to target URL
response = requests.get('http://audioeden.com/useddemo-gear/4525583102')

# parse content
content = BeautifulSoup(response.text, 'lxml')

# extract <style> tag's content!
style = content.find('style').text

# extract ABSOLUTE TOP COORDINATES
tops = [
    int(item.split('top:')[-1].split('px;')[0])
    for item in style.split('}\n')
        if 'page_useddemo-gear' in item and
           'top' in item
]

# sort ABSOLUTE TOP COORDINATES in ascending order
tops.sort()

# map ABSOLUTE TOP COORDINATES in pixels to class names!
coordinates = [
    {
        'class': item.split('{')[0][1:-1],
        'top': int(item.split('top:')[-1].split('px;')[0]),
    }
    
    for item in style.split('}\n')
        if 'page_useddemo-gear' in item and
           'top' in item 
]

# init raw data item list
data_raw = []

# loop over ABSOLUTE TOP COORDINATES
for top in tops:
    # loop over ABSOLUTE TOP COORDINATES mapped to class names
    for entry in coordinates:
        # match entries in the order presented on website
        if entry['top'] == top:
            try:
                try:
                    # append image URLs
                    data_raw.append('http://audioeden.com' + content.find('img', {'class': entry['class']})['src'])
                    print('http://audioeden.com' + content.find('img', {'class': entry['class']})['src'])
                except:
                    pass
                
                # append descriptions and prices
                data_raw.append(content.find('div', {'class': entry['class']}).text.strip())
                print(content.find('div', {'class': entry['class']}).text.strip())
                
            except:
                pass

# init output data list
data = []

# loop over raw data list
for index in range(5, len(data_raw)):
    # pick up descriptions
    if len(data_raw[index]) > 10 and 'http' not in data_raw[index]:
        # set up index offset in case of image URL
        if 'http' not in data_raw[index + 1]:
            offset = 1
        else:
            offset = 2
        
        # pick up prices
        if len(data_raw[index + offset]) < 10 and len(data_raw[index + offset + 1]) < 10:
            try:
                # map items
                features = {
                    'description': data_raw[index],
                    'selling_price': data_raw[index + offset],
                    'retail_price': data_raw[index + offset + 1],
                    'image_url': []
                }
                
                if 'http' in data_raw[index - 1]:
                    features['image_url'].append(data_raw[index - 1])
                
                if 'http' in data_raw[index + 1]:
                    features['image_url'].append(data_raw[index + 1])
                
                # append mapped row to data list
                data.append(features)
                
            except:
                pass

# fixing price shuffles
for index in range(5, len(data)):                
    if data[index]['selling_price'] == '':       
        data[index]['selling_price'] = data[index]['retail_price']
        data[index]['retail_price'] = ''

    if (
            data[index]['retail_price'] == 'CALL' or
            data[index]['retail_price'] == 'SOLD' or
            data[index]['retail_price'] == 'In-Store'
       ):
        selling = data[index]['selling_price']
        data[index]['selling_price'] = data[index]['retail_price']
        data[index]['retail_price'] = selling
    
    try:
        if int(data[index]['selling_price'][1:].replace(',', '')) > int(data[index]['retail_price'][1:].replace(',', '')):
            selling = data[index]['selling_price']
            data[index]['selling_price'] = data[index]['retail_price']
            data[index]['retail_price'] = selling
    except:
        pass

# print extracted data
print(json.dumps(data, indent=2))

# write extracted data to CSV
with open('speakers.csv', 'w') as f:
    writer = csv.DictWriter(f, data[0].keys())
    writer.writeheader()
    writer.writerows(data)






















#####################################################################
#
# Libraries
#
#####################################################################

import requests
from bs4 import BeautifulSoup
import csv
import time


#####################################################################
#
# Scraper
#
#####################################################################

# Parse HTTP response
def parse(response):
    print('HTTP GET: %s | Status code: %s' % (response.url, response.status_code))
    
    # Parse HTML document
    content = BeautifulSoup(response.text, 'lxml')

    # Extract fields from HTML document
    titles = [title.find('a')['title'] for title in content.findAll('h2', {'class': 'product-name'})]
    links = [link.find('a')['href'] for link in content.findAll('h2', {'class': 'product-name'})]
    mpns = [mpn.text.split(':')[-1].strip() for mpn in content.findAll('div', {'class': 'product-list-sku'}) if 'MPN' in mpn.text]
    skus = [sku.text.split(':')[-1].strip() for sku in content.findAll('div', {'class': 'product-list-sku'}) if 'SKU' in sku.text]
    features = [ul.findAll('li') for ul in content.findAll('div', {'class': 'desc std'})]
    bases = [''.join([base.text for base in feature if 'Base:' in base.text]).split(':')[-1].strip() for feature in features]
    wattages = [''.join([wattage.text for wattage in feature if 'Wattage:' in wattage.text]).split(':')[-1].strip() for feature in features]
    watt_eqvs = [''.join([wattage.text for wattage in feature if 'Watt Equivalent:' in wattage.text]).split(':')[-1].strip() for feature in features]
    lumens = [''.join([lumen.text for lumen in feature if 'Lumens:' in lumen.text]).split(':')[-1].strip() for feature in features]
    lumens_per_watt = [''.join([lumen.text for lumen in feature if 'Lumens Per Watt:' in lumen.text]).split(':')[-1].strip() for feature in features]
    warranties = [''.join([warranty.text for warranty in feature if 'Warranty:' in warranty.text]).split(':')[-1].strip() for feature in features]
    extras = [''.join([extra.text for extra in feature if 'Features:' in extra.text]).split(':')[-1].strip() for feature in features]

    # Loop over the index range scraped items
    for index in range(0, len(titles)):
        # Append scraped item to results list
        results.append({
            'Title': titles[index],
            'Link': links[index],
            'MPN': mpns[index],
            'SKU': skus[index],
            'Base': bases[index],
            'Wattage': wattages[index],
            'Wattage equivalent': watt_eqvs[index],
            'Lumens': lumens[index],
            'Lumens per Watt': lumens_per_watt[index],
            'Warranty': warranties[index],
            'Features': extras[index]
        })

# Export scraped results to CSV file
def export_csv(filename):
    # Create file stream
    with open(filename, 'w') as csv_file:
        # Create CVS dictionary writer object
        writer = csv.DictWriter(csv_file, results[0].keys())
        
        # Write CSV column names to file
        writer.writeheader()
        
        # Loop over scraped results
        for row in results:
            # Write scraped item as CSV row
            writer.writerow(row)
        
        print('Exported results to "%s" file' % filename)


#####################################################################
#
# Crawler
#
#####################################################################

# Crawler's entry point URL
base_url = 'https://www.lightup.com/standard-household-lighting.html?p='

# Number of pages to scrape
page_number = 3

# List of scraped results
results = []

# Loop over the range of pages to scrape
for page in range(1, page_number + 1):
    # Init next page URL
    url = base_url + str(page)
    
    # Make HTTP GET request to the next page URL
    response = requests.get(url)
    
    # Parse the HTML response
    parse(response)
    
    # Wait for 31 seconds
    time.sleep(31)

# Export date to CSV file
export_csv('bulbs.csv')


#
# Libraries
#

import requests
from bs4 import BeautifulSoup
from tabulate import *
import csv

# Get HTML response
html = requests.get('https://www.free-proxy-list.net/')

# Parse HTML response
content = BeautifulSoup(html.text, 'lxml')

# Extract proxies table
table = content.find('table')

# Extract table rows
rows = table.findAll('tr')

# Extract table headers
headers = [header.text for header in rows[0]]

# Create proxies result list
results = [headers]

# Loop over table rows
for row in rows:
    # Use only non-empty rows
    if len(row.findAll('td')):
        # Append rows containing proxies to results list
        results.append([data.text for data in row.findAll('td')])

# Pretty print results to console
print(tabulate(results, headers, tablefmt='fancy_grid'))

# Store results as csv file
with open('proxies.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(results)

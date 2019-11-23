#
# Libraries
#

from bs4 import BeautifulSoup
from tabulate import *
import requests
import time
import json
import csv


# Scraper class to inherit from
class Scraper:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    # URLs to crawl
    urls = []
    
    # Base URL
    base_url = ''
    
    # The number of pages to be scraped
    page_number = 0
    
    # Results list
    results = []
    
    # Column names
    columns = []
    
    # Run scraper
    def run(self):
        # Loop over the range of pages to crawl
        for index in range(1, self.page_number + 1):
            # Populate URLs list with pages to crawl
            self.urls.append(self.base_url + str(index))
        
        # Loop over the URLs
        for url in self.urls:
            # Make HTTP GET request
            response = requests.get(url, proxies={'https':'151.253.165.70:8080'}, headers=self.headers)
            print('GET: %s | Status code: %s' % (url, response.status_code))
            
            # Call parse method when the response is obtained
            self.parse(response)
            
            # 2 seconds delay to avoid torturing web sites
            time.sleep(2)
    
    # User's parse function to extract data
    def parse(self, response):
        pass
    
    # Pretty print results to console
    def print_results(self):
        # Make sure results available
        if len(self.results):
            # Results in dictionary format case
            if type(self.results[0]) == dict:
                print(tabulate([row.values() for row in self.results], self.results[0].keys(), tablefmt='fancy_grid'))            
            # Results in list format case
            if type(self.results[0]) == list:
                print(tabulate(self.results, tablefmt='fancy_grid'))
    
    # Export results as CSV file
    def export_csv(self, filename):
        # Create file stream
        with open(filename, 'w', newline='') as csv_file:
            # Make sure results available
            if len(self.results):
                # Results in dictionary format case
                if type(self.results[0]) == dict:
                    # Create dictionary writer
                    writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
                    
                    # Write column names
                    writer.writeheader()
                    
                    # Loop over results
                    for row in self.results:
                        writer.writerow(row)
                
                # Results in list format case   
                elif type(self.results[0]) == list:
                    # Create writer
                    writer = csv.writer(csv_file)
                    
                    # Write results
                    writer.writerows(self.results)
                
                # Return on unsupported results type  
                else:
                    print('ERROR! Unsupported results type!')
                    return
            
            # Return if no results available
            else:
                print('Failed to export "%s" - no results to store!' % filename)

    # Export results in JSON format
    def export_json(self, filename):
        # Create file stream
        with open(filename, 'w') as json_file:
            # Write data in JSON format
            json_file.write(json.dumps(self.results, indent=2))

        

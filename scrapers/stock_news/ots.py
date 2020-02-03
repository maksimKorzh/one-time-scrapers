import requests
from bs4 import BeautifulSoup
import csv
import json


class Onetimescraper:
    results = []
    
    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        res = requests.get(url)
        print(' | Status code: %s' % res.status_code)
        
        return res
    
    def to_html(self, html):
        with open('res.html', 'w') as html_file:
            html_file.write(html)
    
    def from_html(self):
        html = ''
        
        with open('res.html', 'r') as html_file:
            for line in html_file.read():
                html += line
        
        return html
    
    def to_csv(self):
        with open('results.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
            
            for row in self.results:
                writer.writerow(row)
        
        print('"results.csv" has been written successfully!')

import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import time


class BassScraper:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '_ga=GA1.2.361244036.1579946020; _gid=GA1.2.230637940.1579946020; _gat=1',
        'pragma': 'no-cache',
        'referer': 'https://www.thebassplace.com/product-category/basses/',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    results = []
    
    def fetch(self, url):
        print('HTTP GET requests to URL: %s' % url, end='')
        res = requests.get(url, headers=self.headers)
        print(' | Status code: %s' % res.status_code)
        
        return res
    
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        products = content.findAll('li', {'class': 'product-grid-view'})
        
        for product in products:
            self.results.append({
            	'image': product.find('img')['src'],
                'title': product.find('h3', {'class': 'product-title'}).text.strip(),
                'price': product.find('div', {'class': 'fusion-price-rating'}).text.strip()
            })
    
    def load_response(self):
        html = ''
        
        with open('./GUEST/res.html', 'r') as res:
            for line in res:
                html += line
        
        return html
            
    def store_response(self, html):
        with open('./GUEST/res.html', 'w') as res:
            res.write(html)
    
    def to_csv(self):
        with open('basses.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
        
            for result in self.results:
                writer.writerow(result)
    
    def list_files(self):
        os.system('ls ./GUEST > ls.txt')
        
        ls = ''
        
        with open('ls.txt', 'r') as f:
            for line in f.read():
                ls += line
        
        print(ls)
    
    def view_file(self, path):
        content = ''
        
        with open(path, 'r') as f:
            for line in f.read():
                content += line
        
        print(content)
    
    def run(self):
        url = 'https://www.thebassplace.com/product-category/basses/4-string/'
        
        for index in range(1, 4):
            if index == 1:
                next_page = url
            
            else:
                next_page = url + 'page/' + str(index) + '/'
        
            res = self.fetch(next_page)
            self.parse(res.text)
        
        self.to_csv()

scraper = BassScraper()
scraper.run()
#scraper.list_files()
#scraper.view_file('.codelog')




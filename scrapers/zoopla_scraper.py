import requests
from bs4 import BeautifulSoup
import csv
import time


class ZooplaScraper:
    results = []

    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        res = requests.get(url)
        print(' | Status code: %s' % res.status_code)
        
        return res
    
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')        
        
        cards = content.findAll('div', {'class': 'listing-results-wrapper'})
        
        try:
            phone = card.find('span', {'class': 'agent_phone'})  .text.strip()
        except:
            phone = 'N/A'
            
        
        for card in cards:
            self.results.append({
                'title': card.find('a', {'style': 'text-decoration:underline;'}).text,
                'address': card.find('p', {'class': 'listing-results-marketed'}).text.split('Listed on')[1].split('by')[0].strip(),
                'date': card.find('small').text,
                'description': card.find('p').text.strip(),
                'price': card.find('a', {'class': 'listing-results-price'}).text.strip().split(' ')[0].strip(),
                'phone': phone,
                'image': card.find('a', {'class': 'photo-hover'}).find('img')['data-src']
            })
    
    def to_csv(self):
        with open('zoopla.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
        
            for row in self.results:
                writer.writerow(row)
            
            print('Stored results to "zoopla.csv"')
    
    def run(self):
        for page in range(1, 5):
            url = 'https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&q=London&search_source=for-sale&radius=0&pn='
            url += str(page)
            res = self.fetch(url)
            self.parse(res.text)
            time.sleep(2)

        self.to_csv()
        

if __name__ == '__main__':
    scraper = ZooplaScraper()
    scraper.run()

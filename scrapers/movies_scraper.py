# Libraries
import requests
from bs4 import BeautifulSoup
import csv
import json
import os.path
import time


class MovieScraper:
    # Crawler's entry point
    base_url = 'https://en.hkcinema.ru/films/?pg='
    
    def fetch(self, url):
        '''Make HTTP GET request'''
        
        print('HTTP GET request to URL: %s' % url, end='')
        # Retrieve data from URL
        response = requests.get(url)
        print(' | Status code: %s' % response.status_code)
        
        # Return response object
        return response
    
    def to_html(self, response):
        '''Save response as HTML file'''
        
        print('Writing "res.html"')
        
        # Write HTML file to disk
        with open('res.html', 'w') as html_file:
            html_file.write(response.text)
    
    def from_html(self):
        '''Load HTML response from disk'''
        html = ''
        
        print('Reading "res.html"')
        
        # Load HTML response
        with open('res.html', 'r') as html_file:
            for line in html_file.read():
                html += line
        
        # Return HTML string
        return html
    
    def parse(self, html):
        '''Parse HTML response'''
        
        # Parse content
        content = BeautifulSoup(html, 'lxml')
        
        # Extract data
        title = [title.find('span', {'class': 'red'}).text for title in content.findAll('div', {'class': 'top-block'})]
        description = ['\n'.join([item.text for item in descr.findAll('div', {'data-role': 'links'})]) for descr in content.findAll('div', {'class': 'middle-block'})]
        
        # Loop over entries' indexes
        for index in range(0, len(title)):
            # Extract genre
            genre = description[index].split('\n')[1]
            
            # Pick up only kungfu movies
            if 'martial arts' in genre:
                if description[index].split('\n')[5] == '':
                    director = ''
                    starring = description[index].split('\n')[3]
                else:
                    director = description[index].split('\n')[3]
                    starring = description[index].split('\n')[5]
                
                # Init scraped item
                item = {
                    'title': title[index],
                    'release_year': description[index].split('\n')[0],
                    'genre': genre,
                    'director': director,
                    'starring': starring,
                }
                
                # Write scraped item to CSV file
                self.to_csv(item)
            
            # Skip non-kungfu movies
            else:
                continue
    
    def to_csv(self, item):
        '''Write item to CSV file'''
        
        # Check if "movies.csv" file exists
        movies_exists = os.path.isfile('movies.csv')
        
        # Append data to CSV file
        with open('movies.csv', 'a') as csv_file:
            # Init dictionary writer
            writer = csv.DictWriter(csv_file, fieldnames=item.keys())
            
            # Write header only ones
            if not movies_exists:
                writer.writeheader()
            
            # Write entry to CSV file
            writer.writerow(item)
    
    def run(self):
        '''Start scraper'''
        
        # Loop over page range
        for page in range(1, 711):
            # Init next page's URL
            next_page = self.base_url + str(page)
            
            # Make HTTP GET request to the next page
            response = self.fetch(next_page)
            
            # Parse the response
            self.parse(response.text)
            
            # Wait for 2 sec
            time.sleep(2)


# Main driver
if __name__ == '__main__':
    # Init scraper instance
    scraper = MovieScraper()
    
    # Start scraper
    scraper.run()




# Import one time scraper and dependencies
from lib.ots import *

class ProxyScraper(Scraper):
    # Define url to scrape data from
    urls = ['https://free-proxy-list.net/']

    # Parse content
    def parse(self, response):
        # Parse response
        content = BeautifulSoup(response.text, 'lxml')
        
        # Extract proxy table
        table = content.find('table')
        
        # Extract table rows
        rows = table.findAll('tr')
        
        # Extract headers
        headers = [header.text for header in rows[0].findAll('th')]
        
        # Append headers to results list
        self.results.append(headers)
        
        # Loop over table rows
        for row in rows:
            if len(row.findAll('td')):
                # Append proxies to results list
                self.results.append([data.text for data in row.findAll('td')])
        

# Create QuotesScraper instance
scraper = ProxyScraper()

# Run QuotesScraper
scraper.run()

# Pretty print results to console
scraper.print_results()

# Export extracted data to CSV file
scraper.export_csv('./data/proxies.csv')

# Export extracted data to JSON file
scraper.export_json('./data/proxies.json')




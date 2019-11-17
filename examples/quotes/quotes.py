# Import Scraper class and dependencies
from lib.ots import *

# Create QuotesScraper class inherited from Scraper class
class QuotesScraper(Scraper):
    # Define base URL
    base_url = 'http://quotes.toscrape.com/page/'
    
    # Define the number of pages to be scraped
    page_number = 2
    
    # Define results list
    results = []
    
    # Parse response for each page
    def parse(self, response):
        # Parse content
        content = BeautifulSoup(response.text, 'lxml')
        
        # Extract quotes
        quotes = content.findAll('span', {'class': 'text'})
        
        # Extract author names
        authors = content.findAll('small', {'class': 'author'})

        # Loop over extracted data
        for index in range(0, len(quotes)):
            # Append row in dictionary format to results
            self.results.append({
                'quote': '"' + quotes[index].text[:50] + '...' + '"',
                'author': authors[index].text
            })

# Create QuotesScraper instance
scraper = QuotesScraper()

# Run QuotesScraper
scraper.run()

# Pretty print results to console
scraper.print_results()

# Export extracted data to CSV file
scraper.export_csv('./data/quotes.csv')

# Export extracted data to JSON file
scraper.export_json('./data/quotes.json')



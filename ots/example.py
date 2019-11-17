# Import Scraper class and dependencies
from ots import *

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
quotes = QuotesScraper()

# Run QuotesScraper
quotes.run()

# Pretty print results to console
quotes.print_table()

# Export extracted data to CSV file
quotes.export_csv('quotes.csv', ['quote', 'author'])

# Export extracted data to JSON file
quotes.export_json('quotes.json')



# Import Scraper class and dependencies
from lib.ots import *

# Create QuotesScraper class inherited from Scraper class
class TemplateScraper(Scraper):
    # Define url to scrape data from
    urls = []
    
    # Parse response for each page
    def parse(self, response):
        # Parse content
        content = BeautifulSoup(response.text, 'lxml')


# Create QuotesScraper instance
scraper = TemplateScraper()

# Run QuotesScraper
scraper.run()

# Pretty print results to console
scraper.print_results()

# Export extracted data to CSV file
#scraper.export_csv('./data/template.csv')

# Export extracted data to JSON file
#scraper.export_json('./data/template.json')



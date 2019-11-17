from ots import *

class QuotesScraper(Scraper):
    base_url = 'http://quotes.toscrape.com/page/'
    page_number = 2
    results = [{'y': '1', 'h': '2'}, {'e': '3', 'r': '4'}]
    #results = [['a', 'b'], ['1', '2'], ['3', '4']]
    
    def parse(self, response):
        print('parse', response.text)

quotes = QuotesScraper()
#quotes.run()
quotes.print_table()

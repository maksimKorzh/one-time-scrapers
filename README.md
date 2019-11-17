# One time scraper
A simple class to inherit from while writing one time scrapers

# Install dependencies
pip install requests, bs4, lxml, tabulate

# One time scraper class documentation
  # Inner class fields
  - List of URLs to crawl: urls = []
  - Entry point when pagination is used: base_url = ''
  - The number of pages to be scraped: page_number = 0
  - Results list. Append eithter dictionaries or lists: results = []
  
  # Methods
  - run()                       // Start the scraper
  - print_results()             // Pretty print results list to console
  - export_csv(filename):       // Export results to CSV format
  - export_json(filename):      // Export results to JSON format

# Youtube tutorials
  - one time scraper class: https://www.youtube.com/watch?v=tiC6JZkeiaI

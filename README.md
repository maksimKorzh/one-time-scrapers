# One time scrapers
requests/beautiful soup based one time web scrapers

# Install dependencies
pip install requests, bs4, lxml, tabulate

# One time scraper class documentation
  // Inner class fields
  - urls = []                   // List of URLs to crawl
    
  - base_url = ''               // Entry point when pagination is used
    
  - page_number = 0             // The number of pages to be scraped
    
  - results = []                // Results list. Append eithter dictionaries or lists
  
  // Methods
  - run()                       // Start the scraper
  - print_results()             // Pretty print results list to console
  - export_csv(filename):       // Export results to CSV format
  - export_json(filename):      // Export results to JSON format

# One time scraper class usage example
https://github.com/maksimKorzh/one-time-scrapers/blob/master/ots/example.py

# Youtube tutorials
  - one time scraper class: https://www.youtube.com/watch?v=tiC6JZkeiaI
  - free proxy list: https://www.youtube.com/watch?v=AHoeziSYSgs

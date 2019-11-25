# Libraries
import requests
from bs4 import BeautifulSoup
import csv
import time


# Parse the HTTP response
def parse(response):
    print('HTTP GET: %s | Status code: %s' % (response.url, response.status_code))
    
    # Parse HTML content
    content = BeautifulSoup(response.text, 'lxml')

    # Extract data fields
    titles = [title.text for title in content.findAll('h2', {'class': 'home-title'})]
    links = [link['href'] for link in content.findAll('a', {'class': 'story-link'})]
    labels = content.findAll('div', {'class': 'item-label'})
    dates = [[tag for tag in date][1] for date in labels]
    authors = [[tag for tag in author][2].text.strip('\n')[1:] for author in labels]
    descriptions = [desc.text.strip() for desc in content.findAll('div', {'class': 'home-desc'})]
    
    # Extract next page URL
    next_page = content.find('a', {'class': 'blog-pager-older-link-mobile'})['href']

    # Loop over the indexes of scraped items
    for index in range(0, len(titles) - 1):
        # Append scraped item to results
        results.append({
            'title': titles[index],
            'link': links[index],
            'description': descriptions[index],
            'date': dates[index],
            'author': authors[index],
        })
    
    # Append next page URL to URL's list
    urls.append(next_page)

# Export scraped results to CSV file
def export_csv(filename):
    # Create file stream
    with open(filename, 'w') as csv_file:
        # Create CSV dictionary writer object
        writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
        
        # Write column names to CSV file
        writer.writeheader()
        
        # Loop over scraped results
        for row in results:
            # Write scraped results to CSV file
            writer.writerow(row)
            

# Limit page number to scrape
page_number = 5

# List of pages to scrape
urls = []

# List of scraped results
results = []

# Make initial HTTP GET request to obtain HTML response
html = requests.get('https://thehackernews.com/')

# Parse initial response
parse(html)

# Loop over the number of pages to scrape
for page in range(0, page_number):
    # Get next pages
    next_page = requests.get(urls[-1])
    
    # Parse next page
    parse(next_page)
    
    # Sleep for 2 seconds
    time.sleep(2)

# Export scraped results to CSV file
export_csv('news.csv')


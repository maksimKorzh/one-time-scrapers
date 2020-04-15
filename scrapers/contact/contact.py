# packages
import requests
from bs4 import BeautifulSoup
import re
import json
import csv

# website URL links
urls = ''

# load website URLs
with open('websites.txt', 'r') as f:
    for line in f.read():
        urls += line

# convert string to list of URLs
urls = list(filter(None, urls.split('\n')))

# loop over URLs
for url in urls:
    # make HTTP request to the URL
    res = requests.get(url)
    print('crawled base URL:', res.url)
    
    # parse response
    content = BeautifulSoup(res.text, 'lxml')
    
    # extract contact data
    emails_home = re.findall('(\w+@\w+\.\w+\.\w+)', content.get_text())
    phones_home = re.findall('(\d{3,4} \d{3,4} \d{3,4})', content.get_text())
    
    #print('\nEMAILS (home):', emails_home)
    #print('\nPHONES: (home)', phones_home)
    
    # create a data structure to store contacts
    contacts = {
        'website': res.url,
        'emails_home': ', '.join(emails_home),
        'phones_home': ', '.join(phones_home),
        'emails_contact': '',
        'phones_contact': ''
    }
    
    # extract contact link if available
    try:
        contact = content.find('a', text=re.compile('contact', re.IGNORECASE))['href']
        
        if 'http' in contact:
            contact_url = contact
        else:
            contact_url = res.url[0:-1] + contact
        
        # crawling contact URL recursively
        res_contact = requests.get(contact_url)
        contact_content = BeautifulSoup(res_contact.text, 'lxml').get_text()
        print('crawled contact URL:', res_contact.url)
        
        # extract contact data
        emails_contact = re.findall('(\w+@\w+\.\w+\.\w+)', contact_content)
        phones_contact = re.findall('(\d{3,4} \d{3,4} \d{3,4})', contact_content)
        
        #print('\nEMAILS (contact):', emails)
        #print('\nPHONES: (contact)', phones)
        
        # append additional contacts data
        contacts['emails_contact'] = ', '.join(emails_contact)
        contacts['phones_contact'] = ', '.join(phones_contact)
        
    except Exception as e:
        print(e)
    
    # print output
    print(json.dumps(contacts, indent=2))
    
    # store data to CSV file
    with open('contacts.csv', 'a') as f:
        # create CSV writer
        writer = csv.DictWriter(f, fieldnames=contacts.keys())
        
        # write headers
        #writer.writeheader()
        
        # append row to the CSV
        writer.writerow(contacts)
    
    
    
    

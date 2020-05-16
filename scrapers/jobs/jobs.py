#########################################
#
# Script to scrape images from jobs.lk
# 
#                  by
#
#           Code Monkey King
#
#########################################

# import packages
import requests
from bs4 import BeautifulSoup

# base URL
base_url = 'http://topjobs.lk'

# initial URL
url = 'http://topjobs.lk/applicant/vacancybyfunctionalarea.jsp;jsessionid=v-yF+jLJvrmXYEtW9TRWTAmF?FA=SDQ'

# custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

# print debug info
print('HTTP GET: %s', url)

# make initial HTTP request
response = requests.get(url, headers=headers)

# parse response
content = BeautifulSoup(response.text, 'lxml')

# extract job URLs
job_urls = [
    base_url + url['href'].split("JavaScript:openSizeWindow('..")[-1].split('jsp')[0] + 'jsp'
    for url in
    content.find_all('a')
    if "JavaScript:openSizeWindow('.." in url['href']
]

# loop over job urls
for url in job_urls:
    # print debug info
    print('HTTP GET: %s' % url)

    # make HTTP request to job URL
    job_response = requests.get(url, headers=headers)
    
    # parse response
    job_content = BeautifulSoup(job_response.text, 'lxml')
    
    try:
        # extract image URL
        image_url = base_url + job_content.find('div', {'id': 'remark'}).find('img')['src']
        
        # print debug info
        print('HTTP GET: %s' % image_url)

        # make HTTP request to the image URL
        image_response = requests.get(image_url, headers=headers)

        # init filename
        filename = image_url.split('/logo/')[-1].replace(' ', '_').replace('/', '_')
        
        # store image locally
        with open('./images/' + filename, 'wb') as f:
            f.write(image_response.content)
        
        # print debug info
        print('Writing image to "%s"' % filename)
    
    except:
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

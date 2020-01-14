import requests
from bs4 import BeautifulSoup


class PinterestScraper:
    def load_images(self):
        html = ''
        
        with open('images.html', 'r') as image:
            for line in image.read():
                html += line
        
        return html
    
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        return [image['src'] for image in content.findAll('img')]
    
    def download(self, url):
        response = requests.get(url)
        filename = url.split('/')[-1]
        
        print('Downloading image %s from URL %s' % (filename, url))
        
        if response.status_code == 200:
            with open('./images/' + filename, 'wb') as image:
                for chunk in response.iter_content(chunk_size=128):
                    image.write(chunk)
    
    def run(self):
        html = self.load_images()
        urls = self.parse(html)
        
        for url in urls:
            self.download(url)

if __name__ == '__main__':
    scraper = PinterestScraper()
    scraper.run()

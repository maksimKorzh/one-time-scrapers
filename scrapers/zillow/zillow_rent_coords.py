import requests
from bs4 import BeautifulSoup
import csv
import json


class ZillowScraper:
    results = []

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'zguid=23|%2403435e76-0699-4a32-b86d-77d033c907ef; _ga=GA1.2.1271511001.1575011821; zjs_user_id=null; zjs_anonymous_id=%2203435e76-0699-4a32-b86d-77d033c907ef%22; _gcl_au=1.1.1333357279.1575011822; _pxvid=3cfcc163-1278-11ea-bff8-0242ac12000b; ki_r=; __gads=ID=84d8013cfac6df96:T=1575012041:S=ALNI_MaSvVNZsir2JXJ17pv54bjsPuyfcw; ki_s=199442%3A0.0.0.0.0%3B199444%3A0.0.0.0.2; zgsession=1|c0999376-b167-4a47-a1cd-0e456d882d4e; _gid=GA1.2.55965867.1578668946; JSESSIONID=87D0662A6BC141A73F0D12620788519C; KruxPixel=true; DoubleClickSession=true; KruxAddition=true; ki_t=1575011869563%3B1578669044158%3B1578669044158%3B2%3B10; _pxff_tm=1; _px3=2e6809e35ce7e076934ff998c2bdb8140e8b793b53e08a27c5da11f1b4760755:DFItCmrETuS2OQcztcFmt0FYPUn00ihAAue2ynQgbfSq6H+p2yP3Rl3aeyls3Unr1VRJSgcNue8Rr1SUq4P1jA==:1000:9ueZvAJ6v5y4ny7psGF25dK+d3GlytY2Bh+Xj9UUhC4DaioIZ+FMXPU0mOX+Qnghqut0jIT61gLecN4fyu6qXaPDlBX6YsZVbIry1YyBN/37l0Ri3JP+E0h+m+QEBB+bqb6MbE2HtgGBJRJAry8dgOKGM5JtBGdX+X/nuQX1xaw=; AWSALB=E6JYC43gXQRlE2jPT9e2vAQOYPvdHnccBlqi0mcXevYExTaHro0M+uo/Qxahi6JyLz9LpotY9eLtEbYrAOeQXcCm6UhjWnTopQHernmjlR/ibE6JmE8F6tReiBn4; search=6|1581261153229%7Crect%3D40.96202658306895%252C-73.55498286718745%252C40.4487909557045%252C-74.40093013281245%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D3%26z%3D0%26lt%3Dfsbo%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%09%01%096181%09%09%09%090%09US_%09',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.142 Chrome/75.0.3770.142 Safari/537.36'
    }

    def fetch(self, url, params):
        print('HTTP GET request to URL: %s' % url, end='')
        res = requests.get(url, params=params, headers=self.headers)
        print(' | Status code: %s' % res.status_code)
        
        return res
   
    def save_response(self, res):
        with open('res.html', 'w') as html_file:
            html_file.write(res)

    def load_response(self):
        html = ''
        
        with open('res.html', 'r') as html_file:
            for line in html_file:
                html += line
        
        return html
   
    def parse(self, html):
        # parse response
        content = BeautifulSoup(html, 'lxml')
        
        # extract property cards
        cards = content.findAll('article', {'class': 'list-card'})
        
        # extract coordinates script
        script = content.find('script', {'data-zrr-shared-data-key': 'mobileSearchPageStore'}).text
        
        # loop over property cards
        for card in cards:
            # try to extract image
            try:
                image = card.find('div', {'class': 'list-card-top'}).find('img')['src']
            except:
                image = 'N/A'
                
            # extract items
            items = {
                'url': card.find('a', {'class': 'list-card-link'})['href'],
                'details': [
                            price.text for price in
                            card.find('ul', {'class': 'list-card-details'}).find_all('li')
                          ],
                'address': card.find('address', {'class': 'list-card-addr'}).text,
                'image': image
            }
            
            # try to extract price if not extracted yet
            try:
                items['price'] = card.find('div', {'class': 'list-card-price'}).text
            except:
                pass
            
            # try to extract coordinates from script
            try:
                splitter = '"detailUrl":"' + items['url'] + '","latLong":'
                coords = json.loads(script.split(splitter)[-1].split('},')[0] + '}')
                items['coordinates'] = coords
            except:
                coords = script.split(splitter)[-1].split('},')[0] + '}'
                splitter = '<!--{"queryState":{"mapBounds":'
                
                try:
                    map_bounds = json.loads(coords.split(splitter)[-1])
                    items['coordinates'] = map_bounds
                except:
                    items['coordinates'] = 'N/A'
            
            # append scraped items to results list
            self.results.append(items)
            print(json.dumps(items, indent=2))
    
    def to_json(self):
        with open('zillow_rent.json', 'w') as f:
            f.write(json.dumps(self.results, indent=2))
        
    def run(self):
        for page in range(1, 5):
            params = {
                'searchQueryState': '{"pagination":{"currentPage":%s},"mapBounds":{"west":-84.69197781640625,"east":-84.26900418359375,"south":33.61815664689875,"north":33.91554940040142},"regionSelection":[{"regionId":37211,"regionType":6}],"isMapVisible":true,"mapZoom":11,"filterState":{"isForSaleByAgent":{"value":false},"isForSaleByOwner":{"value":false},"isNewConstruction":{"value":false},"isForSaleForeclosure":{"value":false},"isComingSoon":{"value":false},"isAuction":{"value":false},"isPreMarketForeclosure":{"value":false},"isPreMarketPreForeclosure":{"value":false},"isForRent":{"value":true}},"isListVisible":true}' % str(page)
            }
            
            res = self.fetch('https://www.zillow.com/atlanta-ga/rentals/2_p/?', params)
            self.parse(res.text)

        self.to_json()
        
        #html = self.load_response()
        #self.parse(html)
        

if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()








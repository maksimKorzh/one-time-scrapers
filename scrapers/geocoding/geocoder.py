# packages
import requests
import json
import time

# geocoder class
class Geocoder:
    # base url
    base_url = 'https://nominatim.openstreetmap.org/search'
    
    # results
    results = []

    def fetch(self, address):
        # headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        
        # string query parameters
        params = {
            'q': address,
            'format': 'geocodejson'
        }
        
        # make HTTP GET request to Nominatim API
        res = requests.get(url=self.base_url, params=params, headers=headers)
        print('HTTP GET request to URL: %s | Status code: %s' % (res.url, res.status_code))
        
        if res.status_code == 200:
            return res
        else:
            return None
    
    def parse(self, res):
        try:
            label = json.dumps(res['features'][0]['properties']['geocoding']['label'], indent=2)
            coordinates = json.dumps(res['features'][0]['geometry']['coordinates'], indent=2).replace('\n', '').replace('[', '').replace(']', '').strip()                       
            
            # retrieved data
            self.results.append({
                'address': label,
                'coordinates': coordinates
            })
            
        except:
            pass
    
    def store_results(self):
        # write results to file
        with open('results.json', 'w') as f:
            f.write(json.dumps(self.results, indent=2))
    
    def run(self):
        # addresses list
        addresses = ''
        
        # fetch addresses from file
        with open('addresses.txt', 'r') as f:
            for line in f.read():
                addresses += line
        
        # convert addresses to list
        addresses = addresses.split('\n')
        
        # loop over addresse
        for address in addresses:
            res = self.fetch(address).json()
            self.parse(res)
            
            # respect Nominatim crawling policies
            time.sleep(2)
        
        # store results
        self.store_results()

# main driver
if __name__ == '__main__':
    geocoder = Geocoder()
    geocoder.run()









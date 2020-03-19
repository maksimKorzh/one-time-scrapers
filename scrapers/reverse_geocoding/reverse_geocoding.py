# packages
import requests
import json
import time

# reverse geoceder
class ReverseGeocoder:
    # base url
    base_url = 'https://nominatim.openstreetmap.org/reverse'
    
    # results
    results = []
    
    def fetch(self, lat, lon):
        # headers
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        
        # parameters
        params = {
            'format': 'geocodejson',
            'lat': lat,
            'lon': lon
        }
    
        # HTTP GET request
        res = requests.get(url=self.base_url, params=params, headers=headers)
        print('HTTP GET request to URL: %s | Status code: %s' % (res.url, res.status_code))
        
        if res.status_code == 200:
            return res
        else:
            return None
    
    def parse(self, res, lat, lon):
        data = res['features'][0]['properties']['geocoding']
        data['lat'] = lat
        data['lon'] = lon
        
        self.results.append(data)
    
    def store_results(self):
        # write results to file
        with open('results.json', 'w') as f:
            f.write(json.dumps(self.results, indent=2))
            
    
    def run(self):
        # load coordinates
        content = ''
        
        # open source coordinates file
        with open('coordinates.txt', 'r') as f:
            for line in f.read():
                content += line
        
        # create coordinates list
        coordinates = content.split('\n')
        
        # loop over coordinates
        for coordinate in coordinates:
            try:
                # extract coordinates
                lon = coordinate.split(',')[0].strip()
                lat = coordinate.split(',')[1].strip()

                # make HTTP request to Nominatim API
                res = self.fetch(lat, lon)
                self.parse(res.json(), lat, lon)
                
                # respect crawling policies
                time.sleep(1)
                
            except:
                pass
        
        # store results
        self.store_results()

# main driver
if __name__ == '__main__':
    reverse_geocoder = ReverseGeocoder()
    reverse_geocoder.run()
        
        
        
        
        
        
        
        
        
        
        
        
        
        

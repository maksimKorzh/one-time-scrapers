#########################################################################
#
# Script to sxtract data from JavaScript variable from "menu_data.js"
#           from https://www.districtcouncils.gov.hk/
#
#                              by
#
#                       Code Monkey King
#
#########################################################################

# packages
import requests
import json
import re

# target URL endpoint
url = 'https://www.districtcouncils.gov.hk/east/js/menu_data.js'

# make HTTP GET request to URL endpoint
response = requests.get(url)

# extract JSON data
json_data = re.findall(r'(.*)(=)([^;]*)', response.text)[0][2].replace("'", '"')

# parse JSON data
json_data = json.loads(json_data)

# print the rest of the links
for item in json_data[2][-1]:
    for link in item[1]:
        print(link)
        











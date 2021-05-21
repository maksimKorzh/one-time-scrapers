#
# JavaScript에서 따옴표를 가져 오는 스크립트
#

# 밖에서 코드를 가져 오는
import requests
from bs4 import BeautifulSoup
import json

# 타겟 URL
url = 'https://quotes.toscrape.com/js/page/'

# 출력 데이터
data = []

# 페이지 넘다 (1-10)
for page in range(1, 11):
    # HTTP 요청 만들다
    response = requests.get(url + str(page) + '/')
    print(response, url + str(page) + '/')
    
    # JAVASCRIPT으로 변하게 하다
    content = BeautifulSoup(response.text, 'lxml').find_all('script')[-1].text
    
    # JSON으로 변하게 하다
    json_data = content.split('var data = ')[-1].split('];')[0] + ']'
    
    # PYTHON으로 변하게 하다
    python_data = json.loads(json_data)
    
    # 출력 데이터 만들다
    [data.append(quote) for quote in python_data]
    
# JSON로 저장
with open('quotes.json', 'w') as f:
    f.write(json.dumps(data, indent=2))

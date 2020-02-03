from ots import *

class StockNewsScraper(Onetimescraper):
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        
        titles = [title.text for title in content.find_all('h2', {'class': 'entry-title'})]
        links = [link.find('a')['href'] for link in content.find_all('h2', {'class': 'entry-title'})]
        dates = [date.text for date in content.find_all('span', {'class': 'meta-date'})]
        articles = []
        
        for link in links:
            res = self.fetch(link)
            article_content = BeautifulSoup(res.text, 'lxml')
            article_body = ''.join([line.text for line in article_content.find('div', {'class': 'entry-content'}).find_all('p')])
            articles.append(article_body)
        
        for index in range(0, len(titles)):
            self.results.append({
            	'title': titles[index],
                'links': links[index],
                'dates': dates[index],
                'article': articles[index]
            })
    
    def run(self):
        url = 'http://www.stockpricetoday.com/stock-news/'

        # initial page request
        res = self.fetch(url)
        self.parse(res.text)
        
        # crawling pages
        for page in range(2, 5):
            next_page = url + 'page/' + str(page) + '/'
            res = self.fetch(next_page)
            self.parse(res.text)
        
        self.to_csv()


scraper = StockNewsScraper()
scraper.results = []
scraper.run()

from lib.ots import *


class AgentScraper(Scraper):
    base_url = 'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/'
    page_number = 2
    
    def parse(self, response):
        #with open('res1.html', 'r') as html_file:
            #html_file.write(response.text)
            #for line in html_file.read():
            #    response += line
        
        content = BeautifulSoup(response.text, 'lxml')
        table = content.find('table')
        rows = table.findAll('tr')
        
        if response.url.split('/')[-1] == '1':
            self.columns = [header.text.strip('\n') for header in rows[0].findAll('th')]
        
        for row in rows:
            if len(row.findAll('td')):
                self.results.append([data.text for data in row.findAll('td')])

        print('rows', len(rows))

scraper = AgentScraper()
scraper.run()
scraper.results.insert(0, scraper.columns)
scraper.print_results()
scraper.export_csv('./data/user_agents.csv')

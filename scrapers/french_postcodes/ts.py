##########################################
#
#              Tiny Scraper
#
#    A minimalist web scraping library
#         (created just for fun)
#
#                   by
#
#            Code Monkey King
#
##########################################

# packages
from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.parse import unquote
import json
import csv
import re

# HTML parser
def parse(uri, *args, **kwargs):
    try:
        try:
            # create request object
            request = Request(uri, **kwargs)
            
            # handle method keyword availability
            try:
                request.__dict__['method']
            
            except:
                request.__dict__['method'] = 'GET'

            # print request info
            print(' Tiny Scraper: HTTP "%s" to URL: %s' % 
                     (request.__dict__['method'], uri))

            try:
                # make HTTP request to the target URL
                response = urlopen(request)
            
            except Exception as e:
                if e.code in [400, 403, 405]:
                    print(' Tiny Scraper: %s' % e)
                    return
            
            # print response status code
            print(' Tiny Scraper: Response %s' % response.getcode())

            # extract HTML text from response
            text = response.read().decode(encoding='utf-8', errors='ignore')
        
        except:
            # init empty response
            response = 'local file source'
        
            # init local HTML content
            text = ''
            
            # open local HTML file
            with open(uri, 'r') as f:
                for line in f.read():
                    text += line        
        
        # init regex to parse HTML
        regex = r'''(< *\w+( +\w+( *= *[\"|'][^\"|^']+[\"|'])?)* */? *>)([^<]*)'''        

        # try custom regular expresiion if available
        try:
            regex = args[0]
            print(' Tiny Scraper: using custom regular expression %s' % regex)
        
        except:
            pass
            
        # parse content
        tags = [
            {
                'tag': item[0].strip('<>').split()[0],
                'attrs': [
                    {
                        attr.split('=')[0]: attr.split('=')[-1]
                                                .strip('"')
                                                .strip("'")
                    }
                    for attr in
                    item[0].replace(': ', ':').strip('>').split()[1:]
                ],
                'text': item[-1]
            }
            for item in
            re.findall(regex, text)
        ]
        
        # fix tag attributes type
        for item in tags:
            try:
                # init temp attributes dictionary
                temp_attrs = {}
                
                # loop over attributes list
                for attr in item['attrs']:
                    key = list(attr.items())[0][0]
                    val = list(attr.items())[0][-1]
                    
                    # append key value pairs
                    temp_attrs[key] = val
                
                # update tag attributes
                item['attrs'] = temp_attrs

            except:
                item['attrs'] = {}
        
        # init available attrs for emty tags
        all_attrs = []
        
        # loop over all tags
        for item in tags:
            # store all available tag attributes
            [
                all_attrs.append(attr)
                for attr in
                list(item['attrs'].keys())
            ]
        
        # init unique attributes
        all_attrs = dict.fromkeys(all_attrs, '')
        
        # apply unique attributes
        for item in tags:
            if item['attrs'] == {}:
                item['attrs'] = all_attrs

            else:
                for key in all_attrs:
                    try:
                        item['attrs'][key]
                    
                    except:
                        item['attrs'][key] = ''
 
        # return parsed content
        return {
            'response': response,
            'text': text,
            'tags': tags
        }
    
    except Exception as e:
        print(' Tiny Scraper:', e)

# tests
if __name__ == '__main__':
    # parse quotes
    content = parse('http://quotes.toscrape.com')
    
    # get response object
    print('\n\nResponse object:\n', content['response'])
    
    # get response text
    print('\n\nHTML document:\n', content['text'])

    # print all tag elements
    print('\n\nAll tag elements:\n')
    print(json.dumps(content['tags'], indent=2))
    
    # print all tag names
    print('\n\nAll tag names:\n')
    for item in content['tags']:
        print(item['tag'])
    
    # print all tag attributes
    print('\n\nAll tag attributes:\n')
    for item in content['tags']:
        print(item['attrs'])
    
    # print all tag textual nodes
    print('\n\nAll tag text:\n')
    for item in content['tags']:
        print(item['text'])    
    
    # print all quotes
    print('\n\nExtracted quotes:\n')
    quotes = [
        print(item['text'])
        for item in content['tags']
        if item['tag'] == 'span' and
           item['attrs']['class'] == 'text'
    ]
    
    # print all authors
    print('\n\nExtracted authors:\n')
    authors = [
        print(item['text'])
        for item in content['tags']
        if item['tag'] == 'small' and
           item['attrs']['class'] == 'author'
    ]
    
    # print all author links
    print('\n\nAuthor detail URLs:\n')
    links = [
        print(item['attrs']['href'])
        for item in content['tags']
        if item['tag'] == 'a' and
           item['text'] == '(about)'
    ]
    
    # print all tags
    print('\n\nAll tags:\n')
    tags = [
        print(item['text'], item['attrs']['href'])
        for item in content['tags']
        if item['tag'] == 'a' and
           item['attrs']['class'] == 'tag'
    ]
                
                
                














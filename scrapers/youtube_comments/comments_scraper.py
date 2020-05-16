from selenium import webdriver

import time

driver=webdriver.Chrome()

driver.get('https://www.youtube.com/watch?v=iFPMz36std4')

#driver.execute_script('window.scrollTo(1, 500);')

#now wait let load the comments
time.sleep(10)

#driver.execute_script('window.scrollTo(1, 3000);')



comment_div=driver.find_element_by_xpath('//*[@id="contents"]')
comments=comment_div.find_elements_by_xpath('//*[@id="content-text"]')

for comment in comments:
    print(comment.text)
    
driver.close()

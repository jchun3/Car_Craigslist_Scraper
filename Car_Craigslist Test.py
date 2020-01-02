from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import time

class car_scraper(object):
    def __init__(self):
        self.browser = webdriver.Chrome(r'F:\Working Codes\chromedriver')
        self.url = 'https://orangecounty.craigslist.org/'
        self.first_gen = [1995, 2000]
        self.sec_gen = [2000,2005]
        self.thir_gen = [2005,2011]
        self.fo_gen = [2011, 2015]
    #starting up Chrome
    #def startdriver(self):

    def fill_details(self):

        #parsing on html with id = query
        self.browser.get(self.url)
        search_bar = self.browser.find_element_by_id('query')

        search_bar.send_keys('honda civic')
        
        search_bar.send_keys(Keys.ENTER)
        
        min_price = self.browser.find_element_by_name('min_price')
        min_price.send_keys('1000')
        min_year = self.browser.find_element_by_name('min_auto_year')
        min_year.send_keys(self.sec_gen[0])
        max_year = self.browser.find_element_by_name('max_auto_year')
        max_year.send_keys(self.sec_gen[1])
        max_year.send_keys(Keys.ENTER)

        time.sleep(3)
        limit = self.browser.find_element_by_class_name('totalcount').text
        limit = int(limit)
        
        
        data_list=[]
        lists_urls = []
        all_posts = self.browser.find_elements_by_class_name('result-row')
        all_hdrlnk = self.browser.find_elements_by_class_name('result-title.hdrlnk')
        
        source = requests.get(self.browser.current_url).text
        soup = BeautifulSoup(source, 'lxml')

        finding_link = soup.find_all('a',{'class':'result-title hdrlnk'})
        find_info = self.browser.find_elements_by_class_name('attrgroup')
        
        
        for links in finding_link:
            lists_urls.append(links.get('href'))
            #self.browser.get(links.get('href'))
        for link in range(limit):
            temp_list= ""
            last_list = []
            new_list = []
            self.browser.switch_to.window(self.browser.window_handles[0])
            self.browser.execute_script("window.open('');")
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.get(lists_urls[link])
            time.sleep(5)
            #breaks down html file from the element site
            source = requests.get(self.browser.current_url).text
            soup = BeautifulSoup(source, 'lxml')
            #pulling data
            finding_link = soup.find_all('p',{'class':'attrgroup'})
            #first convert html to line of strings
            for texts in finding_link:
                texts.text
                temp_list += texts.text
            #split strings into lists with split
            new_list = temp_list.split('\n')
            #filter out empty spaces
            new_list = list(filter(None, new_list))
            #condition to split only with ":" to convert into category for dict
            for elem in new_list:
                if ':' in elem:
                    first_split = elem.split(':')
                    last_list += first_split
                else:
                    elem
            #convert strings into dict
                res_dct = { last_list[i]: last_list[i+1] for i in range(0, len(last_list), 2)}
            print(res_dct)

            
            self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.close()
            
##            post_titles_list = []
##            for title in all_hdrlnk:
##                post_titles_list.append(title.text)

##        except exceptions.InvalidSessionIdException as e:
##            print(e.message)


car_scraper().fill_details()


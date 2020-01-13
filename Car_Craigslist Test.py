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
import sqlite3

class car_scraper(object):
    def __init__(self):
        self.browser = webdriver.Chrome(r'chromedriver')
        self.url = 'https://orangecounty.craigslist.org/'
        self.first_gen = [1995, 2000]
        self.sec_gen = [2000,2005]
        self.thir_gen = [2005,2011]
        self.fo_gen = [2011, 2015]
        self.conn1 = sqlite3.connect(r'Testing.db')
        self.sql_table1 = """
            CREATE TABLE data (
            id INTEGER PRIMARY KEY,
            vin_number text,
            car_year integer,
            car_type text,
            car_brand text,
            car_price integer,
            car_date integer
            )
            """
        self.sql_table2 = """
            CREATE TABLE detail (
            id INTEGER PRIMARY KEY,
            title_name text,
            car_post_date integer,
            condition text,
            cylinder text,
            drive text,
            fuel text,
            odometer integer,
            paint_color text,
            size text,
            title_status text,
            transmission text,
            type text
            )
            """
        self.data1 ="INSERT INTO data (vin_number, car_year, car_type, car_brand, car_price, car_date) VALUES(?,?,?,?,?,?)"
        self.data2 ="INSERT INTO detail (title_name, car_post_date, condition, cylinder, drive, fuel, odometer, paint_color, size, title_status, transmission, type) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
        self.item_list=[]
    #starting up Chrome
    #def startdriver(self):

    def adding_data(self, car_data):
        
        cur1 = self.conn1.cursor()
        for car_info in car_data:
            cur1.execute(self.data1, (car_info['VIN'], car_info['year'], car_info['model'], car_info['brand'], car_info['price'], car_info['posted date']))
            cur1.execute(self.data2, (car_info['name'], car_info['posted date'], car_info['condition'], car_info['cylinders'],
                                      car_info['drive'], car_info['fuel'], car_info['odometer'], car_info['paint color'], car_info['size'], car_info['title status'],
                                      car_info['transmission'], car_info['type']))
                                                                                                                            
            self.conn1.commit()
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
            #find the date of posted ad
            posted_date = soup.find('time', {'class':'date timeago'})['datetime'].split('T')
            #pulling data set 1
            title_name = soup.find('span', {'id':'titletextonly'}).text
            print(title_name)
            name_price_list = soup.find('span', {'class':'price'}).text
            print(name_price_list)
            #pulling data set 2
            finding_link = soup.find_all('p',{'class':'attrgroup'})
            #first convert html to line of strings
            for texts in finding_link:
                texts.text
                temp_list += texts.text
            #split strings into lists with split
            new_list = temp_list.split('\n')
            #filter out empty spaces
            new_list = list(filter(None, new_list))
            new_name = new_list[0].split(' ')
            #condition to split only with ":" to convert into category for dict
            for elem in new_list:
                if ':' in elem:
                    first_split = elem.split(':')
                    last_list += first_split
                else:
                    elem
            #convert strings into dict
                res_dct = { last_list[i]: last_list[i+1] for i in range(0, len(last_list), 2)}
            res_dct['name'] = new_list[0]
            res_dct['price'] = name_price_list
            res_dct['year']= new_name[0]
            res_dct['brand'] = new_name[1]
            res_dct['model']= new_name[-1]
            res_dct['posted date']= posted_date[0]
            self.item_list.append(res_dct)
            print('ok')


            
            self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.close()
        return self.item_list


options = ['VIN', 'condition', 'cylinders', 'drive', 'fuel', 'odometer', 'paint color',
           'size', 'title status', 'transmission', 'type', 'name', 'price',
           'year', 'brand', 'model', 'posted date']
data = car_scraper().fill_details()

for info in data:
    for option in options:
        if option not in info:
            info[option] = ''
        else:
            continue

car_scraper().adding_data(data)

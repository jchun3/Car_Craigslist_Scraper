from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request

class CraigslistScraper(object):
    def __init__(self, location, postal, radius, model, year_min, year_max):
        self.location = location
        self.postal = postal
        self.radius = radius
        self.model = model
        self.year_min = year_min
        self.year_max = year_max

        
        self.url = f'https://{location}.craigslist.org/search/sss?query={model}&s=120&sort=rel&search_distance={radius}&postal={postal}&min_auto_year={year_min}&max_auto_year={year_max}'
        
        #self.url = f"https://{location}.craigslist.org/search/sss?search_distance={radius}&postal={postal}&max_price={max_price}"
        
        self.driver = webdriver.Chrome(r"F:\Working Codes\chromedriver")
        self.delay = 3

        
    def load_craigslist_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print("page is ready")
            print(self.url)
        except TimeoutException:
            print("loading took too much time")

    def extract_post_information(self):
        all_posts = self.driver.find_elements_by_class_name("result-row")
        post_titles_list = []
        dates = []
        titles = []
        prices = []

        for post in all_posts:
            title= post.text.split("$")

            
            if title[0] =="":
                title=title[1]
            else:
                title = title[0]
                
            title = title.split("\n")
            price = title[0]
            title = title[-1]
            
            date = title.split(" ")
            
            month = date[0]
            day = date[1]
            title = ''.join(title[6:])
            date = month + " " + day
            try:
                if 'honda' in str(title.lower()):
                    titles.append(title)
                    prices.append(price)
                    dates.append(date)
                    post_titles_list.append(post.text)
                    print("Price: " + price)
                    print("Title: " + title)
                    print("Date: " + str(date))  
                else:
                    continue
            except UnicodeEncodeError:

                continue
    
            
        #for name in post_titles_list:
            #if 'honda' not in post_titles_list[name]:
                #print('fail')
            #else:
                #print('pass')
        return titles, prices, dates

    def extract_post_urls(self):
        url_list = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page,"lxml")
        for link in soup.findAll('a', {"class": "result-title hdrlnk"}):
            print(link)
            url_list.append(link["href"])
        return url_list
        
    def quit(self):
        self.driver.close()


        
location ="orangecounty"
postal = "92612"
radius = "50"
model = "honda civic"
year_min = "2001"
year_max = "2005"



scraper = CraigslistScraper(location,postal, radius, model, year_min, year_max)
scraper.load_craigslist_url()
titles, prices, dates  = scraper.extract_post_information()
#scraper.extract_post_urls()
scraper.quit()

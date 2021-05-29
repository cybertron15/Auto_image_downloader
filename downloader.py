from typing import Text
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import action_chains # to make the browser headless
from selenium.webdriver.support.ui import WebDriverWait # to make it wait explicitly
from selenium.webdriver import ActionChains
import selenium.common.exceptions as selenium_exeptions
# from selenium.webdriver.support import expected_conditions
# class for show more results = mye4qd
# class for result may not be what you are looking for = WYR1I
# class for looks like you have reached the end = OuJzKb Yu2Dnd
import os

   

class Downloader():
    """The main class for Google Image Dowloader"""
    def __init__(self,search,items,headless=False):
        self.url = f"https://www.google.com/search?q={search}&tbm=isch"
        self.usr_agent = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
        }
        self.items = items
        self._creating_Driver(headless)
    

    def _creating_Driver(self,headless):
        """Initialises a driver of the webbrowser, make sure you have the webdriver 
        installed and set on path"""
        if headless:
            options = Options()
            options.add_argument("--headless")# setting headless argument
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()

        try:
            self.driver.get(self.url)
        except:
            print("Internet Disconnected")
        self._right_clicking()

    def scroll_down(self):
        """A method for scrolling the page."""
        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while len(self.elements) < self.items:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.implicitly_wait(5)
            self.elements = self.driver.find_elements_by_class_name("rg_i.Q4LuWd")
            response = self._page_end_check()
            if response == "break":
                break

    def _page_end_check(self):
        """When scrolling sometimes you may reach to the end of the page
        and have to take some actions inorder to procceed or end the program"""

        # checking if we have reached the page and getting show more results button
        try:
            show_more_results = self.driver.find_element_by_class_name("mye4qd")
            action = ActionChains(self.driver)
            action.click(show_more_results)
            action.perform()
            self.driver.implicitly_wait(5)
            return
            
        except:
            pass

        # checking if we have reached the page and getting undesiered results warning
        try:
            undesired_results = self.driver.find_element_by_class_name("WYR1I")
            see_more = self.driver.find_element_by_class_name("r0zKGf")
            print(f"fetched {len(self.elements)} valid results")
            print("The rest of the results might not be what you're looking for")
            ans = input("Get more results anyway?(yes/no): ")
            while True:
                if ans == "yes":
                    action = ActionChains(self.driver)
                    action.click(see_more)
                    action.perform()
                    self.driver.implicitly_wait(5)
                    return
                elif ans == "no":
                    return "break"
                else:
                    print("Print valid answer")
                    
        except selenium_exeptions.NoSuchElementException:
            pass
        

        # checking if we have reached the page and no more results are available
        # try:
        #     no_more_results = self.driver.find_element_by_class_name("DwpMZe")
        #     print(f"fetched {len(self.elements)} results")
        #     print("No more retults found on Google Image search")
        #     return "break"

        # except selenium_exeptions.NoSuchElementException:  
        #     pass

        



    
    def _right_clicking(self):
        """This method right clicks each picture which you want to download,
        this is done because until and unless you don't click on a image google 
        won't load the image URL of that image"""

        self.elements = self.driver.find_elements_by_class_name("rg_i.Q4LuWd")
        if len(self.elements) < self.items:
            self.scroll_down()
        
        #setting the limit for images
        self.elements = self.elements[:self.items]
        limit = len(self.elements)
        print(f"Fetching {limit} image links...")

        actions = ActionChains(self.driver)
        # for element in elements:
        #     actions.context_click(element)
        # actions.perform()
        # self._getting_links(limit)

    def _getting_links(self,limit):
        """Rightclicking on every image google search will render the links 
        of the images we need this function is used to get those links from the 
        HTML tags of the image"""

        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        # self.driver.quit()
        a_tags = soup.findAll("a",class_="wXeWr islib nfEiy mM5pbd",limit=limit)
        self._filtering_links(a_tags)
    
    def _filtering_links(self,a_tags):
        """links that we scrape from the google page is not which we can directly
        use to get the image from the web. so we need to filter the image link."""
        self.links = []
        for i in a_tags:
            link = i["href"]
            start,end = link.index("="), link.index("&")
            img_link = link[start+1:end]
            symbols = {"%3A":":","%2F":"/","%3F":"?","%3D":"=","%26":"&",}
            for keys,values in symbols.items():
                img_link = img_link.replace(keys,values)
            self.links.append(img_link)
        
        print("Done...")


    def download_iamges(self):
        folder = "images"
        
        if not os.path.exists(folder):
            os.mkdir(folder)
        print("Downloading Images...")
        
        for i,links in enumerate(self.links):
            image_name = f"{folder}/image{i+1}.jpg"
            
            with open(image_name,'wb') as file:
                file.write(requests.get(links).content)

            print(f"{i+1} Image downloaded")
            

search = input("What you want to download: ")
items = int(input("How many images you want to download: "))
download = Downloader(search,items)
#download.download_iamges()

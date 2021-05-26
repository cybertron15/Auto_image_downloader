import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options# to make the browser headless
from selenium.webdriver import ActionChains


class Downloader():
    """The main class for Google Image Dowloader"""
    def __init__(self,search):
        self.url = f"https://www.google.com/search?q={search}&tbm=isch"
        self.usr_agent = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
        }
        self._creating_Driver()
    
    def _creating_Driver(self,headless=False):
        """Initialises a driver of the webbrowser, make sure you have the webdriver 
        installed and set on path"""
        if headless:
            options = Options()
            options.add_argument("--headless")# setting headless argument
            self.driver = webdriver.Chrome(options=options)
        else:
             self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self._right_clicking()

    def _right_clicking(self):
        """This method right clicks each picture which you want to download,
        this is done because until and unless you don't click on a image google 
        won't load the image URL of that image"""

        actions = ActionChains(self.driver)
        elements = self.driver.find_elements_by_class_name("rg_i.Q4LuWd")
        self.driver.implicitly_wait(2) #add explicit waiting here
        for element in elements:
            actions.context_click(element)
        actions.perform()
        self._getting_links()

    def _getting_links(self):
        """Rightclicking on every image google search will render the links 
        of the images we need this function is used to get those links from the 
        HTML tags of the image"""

        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        self.driver.quit()
        a_tags = soup.findAll("a",class_="wXeWr islib nfEiy mM5pbd")
        self._filtering_links(a_tags)
    
    def _filtering_links(self,a_tags):
        """links that we scrape from the google page is not which we can directly
        use to get the image from the web. so we need to filter the image link."""
        links = []
        for i in a_tags:
            try:
                link = i["href"]
                start,end = link.index("="), link.index("&")
                img_link = link[start+1:end]
                symbols = {"%3A":":","%2F":"/","%3F":"?","%3D":"=","%26":"&",}
                for keys,values in symbols.items():
                    img_link = img_link.replace(keys,values)
                    links.append(img_link)
            except KeyError:
                pass
        print(len(links))

download = Downloader("banana")

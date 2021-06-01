import requests                                         # to get the web pages
from bs4 import BeautifulSoup                           # to parse web pages
from selenium import webdriver                          # to interact with web pages
from selenium.webdriver.chrome.options import Options   # to change web driver settings
from selenium.webdriver.common import action_chains     # to make the browser headless
from selenium.webdriver.support.ui import WebDriverWait # to make it wait explicitly
from selenium.webdriver import ActionChains             # to perform clicks and other actions
import selenium.common.exceptions as selenium_exeptions # handle exeptions such as reaching bottom of the page
import os                                               # to create a folder and save images
import time                                             # to halt the script when needed

   

class Downloader():
    """The main class for Google Image Dowloader"""
    def __init__(self,search,items,headless=True,internet_speed="normal"):
        """
        search: the images which you want to search
        items: number of images you want
        headless: whether you want to see a browser window or not, set to false if you want to see the window
        internet_speed: according to your connection speed set it to 'very fast','fast','normal','slow','very slow','very very slow'

        """
        self.search = search
        self.url = f"https://www.google.com/search?q={search}&tbm=isch"

        #its required to using requests as some pages require it to verify the request is commming from valid source
        self.usr_agent = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
        }
        self.items = items
        self.internet_speed = "normal"
        self.internet_connectivity()
        self._creating_Driver(headless)



    def internet_connectivity(self):
        """depending on the internet the page load time differs
        so to be flexible and not wait for longer period of time
        for people with high intenet speed this method moderates
        wait time for diffrent internet speed"""

        # the waitTime values will be passed in the functions which halt the script for specified time
        if self.internet_speed == "very very slow":
            self.waitTime = 10        

        if self.internet_speed == "very slow":
            self.waitTime = 5
        
        if self.internet_speed == "slow":
            self.waitTime = 4

        if self.internet_speed == "normal":
            self.waitTime = 3
        
        if self.internet_speed == "fast":
            self.waitTime = 2
        
        if self.internet_speed == "very fast":
            self.waitTime = 1



    def _creating_Driver(self,headless):
        """Initialises a driver of the webbrowser, make sure you have the webdriver 
        installed and set on path"""
        if headless:
            # setting headless argument to browser so we don't see a browser window pop
            options = Options()
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()

        try:
            self.driver.get(self.url)
        except:
            print("Internet Disconnected")
        self._right_clicking()



    def scroll_down(self):
        """Google loads images as we scroll down the page so we need to scroll down the
        page to get more elements. As we scroll we need to handle certain situations 
        like page end"""

        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        # scrolling till we get required items
        while len(self.elements) < self.items:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Get new scroll heigh after scrolling
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # wait for the page to load
            self.driver.implicitly_wait(self.waitTime)

            # get newly loaded elemenets
            self.elements = self.driver.find_elements_by_class_name("rg_i.Q4LuWd")

            # checking if we reached the end
            response = self._page_end_check()

            # based on page end conditon we stop scrolling
            if response == "break":
                break
            
            #check if can't scroll more and depending on the situation stop or continue scrolling
            if new_height == last_height:
                if len(self.elements) < self.items:
                    # halt the script to allow it to load incase we are not able to scroll due to slow internet
                    time.sleep(self.waitTime)

                    # checking new hight after waiting to make sure its not internet issue
                    new_height = self.driver.execute_script("return document.body.scrollHeight")

                    #if still we get a problem we stop scrolling and proceed with existing results
                    if new_height == last_height:
                        print(f"fetched {len(self.elements)} links")
                        print(f"No more images to find on Google")

                        # taking 400 as limit of elements because after 400 elements we get 
                        # the show more button and it takes the most time to load so we warn the use about slow connection
                        if len(self.elements) <= 400:
                            print("There is a high chance that you have got less search results due to slow internet speed.")
                            print("make sure you have specified internet speed correctly.")
                            print("by default the speed is set to normal set it to slow or very slow and you may get more results\n")
                        else:
                            print(f"fetched {len(self.elements)} links. No more images present on Google\n")
                        break

            last_height = new_height

    def _page_end_check(self):
        """When scrolling sometimes you may reach to the end of the page
        and have to take some actions inorder to procceed or end the program"""

        # checking if we have reached the page and getting show more results button
        try:
            #if we get the show more button we click it and load more elements
            show_more_results = self.driver.find_element_by_class_name("mye4qd")
            action = ActionChains(self.driver)
            action.click(show_more_results)
            action.perform()
            self.driver.implicitly_wait(self.waitTime)
            return
        
        #we get this eception when the element is not present in page source
        except:
            pass

        # checking if we have reached the page and getting undesiered results warning
        try:
            # sometimes google warns us about getting undesirable results and gives us the option to proceed
            # here we give our user the warning and ask for procceding or stopping
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
                    self.driver.implicitly_wait(self.waitTime)
                    return
                elif ans == "no":
                    return "break"
                else:
                    print("Print valid answer")
                    
        except selenium_exeptions.NoSuchElementException:
            pass

    
    def _right_clicking(self):
        """This method right clicks each picture which you want to download,
        this is done because until and unless you don't click on a image google 
        won't load the image URL of that image"""

        self.elements = self.driver.find_elements_by_class_name("rg_i.Q4LuWd")

        # scrolling down if we have less items than we need
        if len(self.elements) < self.items:
            self.scroll_down()
        
        #setting the limit for images
        self.elements = self.elements[:self.items]
        limit = len(self.elements)
        print(f"Fetching {limit} image links...")

        # clicking on the specified number of images so image links can get loaded
        actions = ActionChains(self.driver)
        for element in self.elements:
            actions.context_click(element)
        actions.perform()

        self._getting_links(limit)

    def _getting_links(self,limit):
        """Rightclicking on every image google search will render the links 
        of the images we need this function is used to get those links from the 
        HTML tags of the image"""

        # sing beautiful soup to parse the HTML source
        soup = BeautifulSoup(self.driver.page_source,"html.parser")

        # shutting down the driver after use
        self.driver.quit()

        #getting a tags to get image links
        a_tags = soup.findAll("a",class_="wXeWr islib nfEiy mM5pbd",limit=limit)
        self._filtering_links(a_tags)
    
    def _filtering_links(self,a_tags):
        """links that we scrape from the google page is not which we can directly
        use to get the image from the web. so we need to filter the image link."""
        
        self.links = []
        for i in a_tags:
            # getting href attribute and slicing the string to get rid of unneccesary part
            link = i["href"]
            start,end = link.index("="), link.index("&")
            img_link = link[start+1:end]

            # this are the symbold we want to replace from the links
            symbols = {"%3A":":","%2F":"/","%3F":"?","%3D":"=","%26":"&","%25":"%"}
            for keys,values in symbols.items():
                img_link = img_link.replace(keys,values)

            self.links.append(img_link)
        
        print("Done...")


    def assigning_extensions(self,links,index,extensions):
        """on the web there are images with diffrent formats. so when we are storing
        the images on our local memory we need to strore it in its original format"""

        if links[-4:] in extensions:
            image_name = f"{self.folder}/image{index+1}{links[-4:]}"
        else:
            image_name = f"{self.folder}/image{index+1}.jpg"

        return image_name


    def download_images(self):
        while True:
            res = input(f"Do you want proceed with downloading {len(self.elements)} images?(y/n)")
            if res == "y":
                self.folder = self.search
                extensions = [".jpg",".JPG",".png",".PNG",".gif",".GIF"]
                if not os.path.exists(self.folder):
                    os.mkdir(self.folder)
                print("Downloading Images...")

                for i,links in enumerate(self.links):
                    image_name = self.assigning_extensions(links,i,extensions)

                    with open(image_name,'wb') as file:
                        file.write(requests.get(links).content)

                    print(f"{i+1} Image downloaded")
                
                print("Download Completed Successfully...")
                print("Terminating script...")
                break

            elif res == "n":
                print("Download cancelled")
                print("Terminating script")
                break
            
            else:
                print("Invalid input! respond with 'y' or 'n' only.")


            
if __name__ == "__main__":
    search = input("What you want to download: ")
    items = int(input("How many images you want to download: "))
    download = Downloader(search,items)
    download.download_images()




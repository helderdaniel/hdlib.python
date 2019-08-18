'''
Simple chrome browser htl, javascript parser

v0.1 jul 2019
hdaniel@ualg.pt

Note: needs chrome browser driver installed:

$> sudo apt install chromium-chromedriver

Maybe it will be necessary to update Chrome to match driver version
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import hdf5storage as hdf


class ChromeBrowser:
    def __init__(self, chromedriverPath='/usr/bin/chromedriver', hideBrowser = True):
        if hideBrowser:
            chrome_options = Options()  
            chrome_options.add_argument("--headless") 
            chrome_options.add_argument('--no-sandbox')				#needed for Colab
            chrome_options.add_argument('--disable-dev-shm-usage')  #needed for Colab
        else:
            chrome_options = None

        self.browser = webdriver.Chrome(chromedriverPath, chrome_options=chrome_options) 

    def __del__(self):
        #todo: if program ends right after starting gives exception, 
        #cause browser still shuting down
        self.browser.quit()

    def getPage(self, url):
        #self.browser.implicitly_wait(20)
        self.browser.get(url)

    def getElementByLinkText(self, linkText, findTimeout = 20):
        try:
            element = WebDriverWait(self.browser, findTimeout).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, linkText)))
        except:
            element = None
        return element

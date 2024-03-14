#  Importing the WebDriver class for automated web browsing.
from selenium import webdriver

# Importing the Keys class for simulating keyboard inputs.
from selenium.webdriver.common.keys import Keys

# Importing the By class for locating elements on web pages.
from selenium.webdriver.common.by import By

# Importing the time module for adding time delays.
import time

# Importing the requests module for sending HTTP requests.
import requests

# Importing the BeautifulSoup class for parsing HTML and XML documents.
from bs4 import BeautifulSoup

# Importing the pandas library for data manipulation with the alias pd.
import pandas as pd


def openWebPage(url):
    """
    Opens a web page specified by the URL using a WebDriver instance.

    The WebDriver instance returned, allows you to automate interactions with the web page.
    """
    driver=webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    return driver

def extractArticles(driver,n):
    """
    Scraping n articles from the web page using the WebDriver instance.

    It returns a list of article elements found while scrolling through the page.
    """
    # The maximum number of articles we can scarpe is 160:
    if n>160:
        n=160

    # Finding the <body> element to enable scrolling:
    element=driver.find_element(By.TAG_NAME,'body')

    while len(articlesList)<n:
        # Scrolling down the web page by sending PAGE_DOWN key.
        element.send_keys(Keys.PAGE_DOWN)

        # Extracting the page source and parsing it with BeautifulSoup:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extracting the articles.
        articlesList=soup.find('ul',{'class':'My(0) P(0) Wow(bw) Ov(h)'}).find_all('h3',{'class':'Mb(5px)'})

        time.sleep(3)
    driver.quit()
    return articlesList
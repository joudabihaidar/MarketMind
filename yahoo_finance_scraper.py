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

import concurrent.futures

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
}
allNews=[]

def openWebPage(url):
    """
    Opens a web page specified by the URL using a WebDriver instance.

    The WebDriver instance returned, allows you to automate interactions with the web page.
    """
    driver=webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    return driver

def extractNews(driver):
    """
    Scraping n number of news from the web page using the WebDriver instance.

    It returns a list of article elements found while scrolling through the page.
    """

    # Finding the <body> element to enable scrolling:
    element=driver.find_element(By.TAG_NAME,'body')

    while len(articlesList)<100:
        # Scrolling down the web page by sending PAGE_DOWN key.
        element.send_keys(Keys.PAGE_DOWN)

        # Extracting the page source and parsing it with BeautifulSoup:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # The list of article elements:
        articlesList=soup.find('ul',{'class':'My(0) P(0) Wow(bw) Ov(h)'}).find_all('h3',{'class':'Mb(5px)'})

        time.sleep(3)
    driver.quit()
    return articlesList

def fetchNewsInfo(List):
    for article in List:
        link = 'https://finance.yahoo.com/quote/AAPL' + article.find('a')['href']
        
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        articles = soup.find('div', {'class': 'caas-body'}).find_all('p')

        paragraph = ''

        for p in articles:
            paragraph += p.text
        print(article.find('a').text)
        news = {
            'Date': soup.find('time')['datetime'],
            'article_title': article.find('a').text,  # Corrected line
            'article': paragraph,
            'source_name': 'Yahoo Finance',
            'source_link': link
        }

        allNews.append(news)
    return 

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(fetchNewsInfo,extractNews(openWebPage("https://finance.yahoo.com/quote/AAPL/news")))
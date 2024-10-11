#  Importing the WebDriver class for automated web browsing.
from selenium import webdriver

# Importing the Keys class for simulating keyboard inputs.
from selenium.webdriver.common.keys import Keys

# Importing the By class for locating elements on web pages.
from selenium.webdriver.common.by import By

# Importing the requests module for sending HTTP requests.
import requests

# Importing the BeautifulSoup class for parsing HTML and XML documents.
from bs4 import BeautifulSoup

# Importing the pandas library for data manipulation with the alias pd.
import pandas as pd

# Concurrent task execution in python.
import concurrent.futures

import re

url="https://finance.yahoo.com/quote/AAPL/news"

"""
Setting up a user-agent header to mimic a request coming from a specific web browser.
This can help in scenarios where websites need to indentify the client's browser type,
for compatibility or access purposes.
"""
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
}

# Global list allNews that will contain all the data about each article:
allNews=[]

def openWebPage(url):
    """
    Opens a web page specified by the URL using a WebDriver instance.

    The WebDriver instance returned, allows you to automate interactions with the web page.
    """
    driver=webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)
    return driver

def extractNews(driver,n):
    """
    Scraping n number of news from the web page using the WebDriver instance.

    It returns a list of article elements found while scrolling through the page.
    """
    articlesList=[]
    # Finding the <body> element to enable scrolling:
    element=driver.find_element(By.TAG_NAME,'body')

    prev_articles_count = 0
    consecutive_no_new_articles = 0

    while len(articlesList)<n:
        # Scrolling down the web page by sending PAGE_DOWN key.
        element.send_keys(Keys.PAGE_DOWN)

        # Extracting the page source and parsing it with BeautifulSoup:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # The list of article elements:
        new_articles_list =soup.find('ul',class_='stream-items yf-1usaaz9').find_all('li')

        # Checking if new articles are loaded
        # if not we will wait, but if the page tried to load new content for more than a certain amount of time and no new data appeared, we stop the loop
        if len(new_articles_list) == prev_articles_count:
            consecutive_no_new_articles += 1
        else:
            consecutive_no_new_articles = 0

        # If no new articles are loaded for several consecutive times, break the loop
        if consecutive_no_new_articles >= 40:
            break

        articlesList = new_articles_list
        prev_articles_count = len(articlesList)

        # for debugging:
        print(f"{len(articlesList)} articles extracted.")

        driver.implicitly_wait(3)
    driver.quit()
    return articlesList

def fetchNewsInfo(article,ticker_symbol):
    """
    Fetching the data of each article that we get from 'extractNews' function.
    Getting the date, title, context, source_namme and link of each article.
    """

    anchor=article.find('a',href=True)
    # Making sure that we're not scraping the ads
    if anchor and 'finance.yahoo.com/news' in anchor['href']:
        title=article.h3.text
        # Printing the article's title for debugging
        print(f"Parsing: {title} \n")

        # Full URL of the articles:
        link=anchor['href']

        r = requests.get(link, headers=headers)

        # Parsing the HTML content of the article page:
        soup = BeautifulSoup(r.text, 'lxml')

        # Finding all the paragraphs of the article and concatenating them:
        articles = soup.find('div', {'class': 'body yf-5ef8bf'}).find_all('p')
        paragraph = ''
        for p in articles:
            paragraph += p.text

        # Dictionary containing all the data we want:
        news = {
            'Date': soup.find('time')['datetime'],
            'article_title': title, 
            'article': paragraph,
            'source_name': 'Yahoo Finance',
            'source_link': link,
            'ticker_symbol':ticker_symbol
        }

    # Global list allNews containing all the data about each article:
    allNews.append(news)
    return

def preProcess(df):
    # Removing duplicates based on article title
    df.drop_duplicates(subset='article_title', keep='first', inplace=True)

    # Sorting DataFrame based on the 'Date' column in reverse order
    df= df.sort_values(by='Date', ascending=False)

    # Converting the 'Date' column to datetime format because errors='coerce' will turn invalid parsing to NaT
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Filtering out rows with valid dates (non-NaT)
    df= df.dropna(subset=['Date'])
    
    return df

def turnToCSV():
    """
    Converting the collected news data into a dataframe and then into a csv file,
    while handling duplicates and cleaning the data.
    """
    try:
        existing_data = pd.read_csv(r"../data/News.csv")
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    new_data=pd.DataFrame(allNews)

    # Appending new data to existing DataFrame
    df = pd.concat([existing_data, new_data])

    # handling duplicates and cleaning the data:
    df=preProcess(df)

    # Turning the df into a csv file:
    df.to_csv(r"../data/News.csv", index=False)

def scrape(ticker_url):
    ticker_symbol, url=ticker_url
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda article: fetchNewsInfo(article,ticker_symbol),extractNews(openWebPage(url),150))
    turnToCSV()

def main():
    """
    Making the program run x100 faster by using concurrent execution,
    to make the code fetch information from multiple news articles in parallel.
    """
    tickers = [("AAPL", "https://finance.yahoo.com/quote/AAPL/latest-news")]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrape,tickers)
    # turnToCSV()

main()

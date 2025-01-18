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

# Logging for debugging purposes
import logging 

# Setting up logging configuration
logging.basicConfig(
    filename='scraper.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

logging.info("Scraper started.")

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
    logging.info(f"Opening webpage: {url}")
    driver=webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)
    return driver

def extractNews(driver,n):
    """
    Scraping n number of news from the web page using the WebDriver instance.

    It returns a list of article elements found while scrolling through the page.
    """
    logging.info(f"Starting news extraction for {n} articles")
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
            logging.warning("No new articles loaded after several attempts. Stopping extraction.")
            break

        articlesList = new_articles_list
        prev_articles_count = len(articlesList)
        logging.info(f"{len(articlesList)} articles extracted so far.")
        driver.implicitly_wait(3)
    driver.quit()
    logging.info(f"Finished extracting {len(articlesList)} articles.")
    return articlesList

def fetchNewsInfo(article,ticker_symbol,article_number):
    """
    Fetching the data of each article that we get from 'extractNews' function.
    Getting the date, title, context, source_namme and link of each article.
    """

    anchor=article.find('a',href=True)
    # Making sure that we're not scraping the ads
    if anchor and 'finance.yahoo.com/news' in anchor['href']:
        title=article.h3.text
        # Printing the article's title for debugging
        logging.info(f"Parsing article #{article_number}: '{title}' \n")

        # Full URL of the articles:
        link=anchor['href']

        r = requests.get(link, headers=headers)

        # Parsing the HTML content of the article page:
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            # Finding all the paragraphs of the article and concatenating them:
            articles = soup.find('div', {'class': 'article-wrap no-bb'}).find_all('p')
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
            logging.info(f"Article #{article_number} processed successfully.\n")
        except Exception as e:
            logging.error(f"Error processing article #{article_number}: '{title}' {e}")
    return allNews

def preProcess(df):
    logging.info("Starting data preprocessing.")
    # Removing duplicates based on article title
    logging.info("Removing duplicates")
    df.drop_duplicates(subset='article_title', keep='first', inplace=True)

    # Sorting DataFrame based on the 'Date' column in reverse order
    logging.info("Sorting the the data based on the data of publication.")
    df= df.sort_values(by='Date', ascending=False)

    # Converting the 'Date' column to datetime format because errors='coerce' will turn invalid parsing to NaT
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Filtering out rows with valid dates (non-NaT)
    df= df.dropna(subset=['Date'])
    
    logging.info("Data preprocessing completed.")
    return df

def turnToCSV():
    """
    Converting the collected news data into a dataframe and then into a csv file,
    while handling duplicates and cleaning the data.
    """
    logging.info("Converting data to CSV.")
    new_data = pd.DataFrame(allNews)
    print(f"New data: {new_data}")

    try:
        # Check if the file exists
        with open('data/News.csv', 'r') as file:
            pass
        # Append data without headers
        new_data.to_csv('data/News.csv', mode='a', header=False, index=False)
        logging.info("Appended new data to existing CSV.")
    except FileNotFoundError:
        # File does not exist, create it with headers
        new_data.to_csv('data/News.csv', mode='w', index=False)
        logging.info("Created new CSV file and saved data.")


def scrape(ticker_url):
    ticker_symbol, url = ticker_url
    logging.info(f"Scraping started for {ticker_symbol} at {url}")
    articles = extractNews(openWebPage(url), 150)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, article in enumerate(articles):
            executor.submit(fetchNewsInfo, article, ticker_symbol, i + 1)  # Pass article number
    turnToCSV()
    logging.info(f"Scraping completed for {ticker_symbol}.")


def main():
    """
    Making the program run x100 faster by using concurrent execution,
    to make the code fetch information from multiple news articles in parallel.
    """
    tickers = [("AAPL", "https://finance.yahoo.com/quote/AAPL/latest-news")]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrape,tickers)


if __name__ == "__main__":
    try:
        main()
        logging.info("Scraper completed successfully.")
    except Exception as e:
        logging.error(f"Scraper encountered an error: {e}")

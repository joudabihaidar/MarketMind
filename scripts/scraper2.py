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

url = "https://finance.yahoo.com/quote/AAPL/news"

# Setting up a user-agent header to mimic a request coming from a specific web browser.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
}

# Global list to hold all the news data.
allNews = []

def openWebPage(url):
    """
    Opens a web page specified by the URL using a WebDriver instance.
    """
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)
    return driver

def extractNews(driver, n):
    """
    Scraping n number of news from the web page using the WebDriver instance.
    It returns a list of article elements found while scrolling through the page.
    """
    articlesList = []
    element = driver.find_element(By.TAG_NAME, 'body')

    prev_articles_count = 0
    consecutive_no_new_articles = 0

    while len(articlesList) < n:
        # Scrolling down the web page by sending PAGE_DOWN key.
        element.send_keys(Keys.PAGE_DOWN)

        # Extracting the page source and parsing it with BeautifulSoup:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # The list of article elements:
        new_articles_list = soup.find('ul', class_='stream-items yf-1usaaz9').find_all('li')

        # Check if new articles are being loaded:
        if len(new_articles_list) == prev_articles_count:
            consecutive_no_new_articles += 1
        else:
            consecutive_no_new_articles = 0

        # If no new articles are loaded for too long, break the loop:
        if consecutive_no_new_articles >= 40:
            break

        articlesList = new_articles_list
        prev_articles_count = len(articlesList)
        print(f"Number of articles loaded: {len(articlesList)}")  # For debugging

        driver.implicitly_wait(3)

    driver.quit()
    return articlesList

def fetchNewsInfo(article, ticker_symbol):
    """
    Fetching the data of each article that we get from 'extractNews' function.
    """
    anchor = article.find('a', href=True)
    if anchor and 'finance.yahoo.com/news' in anchor['href']:
        title = article.h3.text
        print(f"Scraping article: {title}")  # Debugging

        link = anchor['href']
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')

        # Extracting the paragraphs of the article.
        articles = soup.find('div', {'class': 'body yf-5ef8bf'}).find_all('p')
        paragraph = ' '.join(p.text for p in articles)

        # Dictionary containing all the data we want:
        news = {
            'Date': soup.find('time')['datetime'],
            'article_title': title,
            'article': paragraph,
            'source_name': 'Yahoo Finance',
            'source_link': link,
            'ticker_symbol': ticker_symbol
        }

        return news

def preProcess(df):
    # Remove duplicates based on article title
    df.drop_duplicates(subset='article_title', keep='first', inplace=True)

    # Sort DataFrame based on the 'Date' column in reverse order
    df = df.sort_values(by='Date', ascending=False)

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Filter out rows with invalid dates (NaT)
    df = df.dropna(subset=['Date'])
    
    return df

def turnToCSV():
    """
    Convert the collected news data into a DataFrame and then into a CSV file.
    """
    try:
        existing_data = pd.read_csv(r"data\News.csv")
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    new_data = pd.DataFrame(allNews)

    # Append new data to existing DataFrame
    df = pd.concat([existing_data, new_data])

    # Process the data to remove duplicates and clean it
    df = preProcess(df)

    # Save the DataFrame to CSV
    df.to_csv(r"data\News.csv", index=False)

def scrape(ticker_url):
    """
    Scrape news for a specific ticker symbol and save it to CSV.
    """
    ticker_symbol, url = ticker_url
    driver = openWebPage(url)
    articles = extractNews(driver, 150)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        news_list = list(executor.map(lambda article: fetchNewsInfo(article, ticker_symbol), articles))

    # Add the news from threads to the global allNews list
    global allNews
    allNews.extend(news_list)

    # Write to CSV
    turnToCSV()

def main():
    """
    Main function that initiates the scraping process.
    """
    tickers = [("AAPL", "https://finance.yahoo.com/quote/AAPL/latest-news")]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrape, tickers)

main()

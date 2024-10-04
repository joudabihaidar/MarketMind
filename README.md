<img src="./readme/title1.svg"/>

<br><br>

<!-- project philosophy -->
<img src="./readme/title2.svg"/>

> MarketMind is a system that enhances financial analysis by integrating sentiment data from news articles into traditional market metrics. By analyzing sentiment, it provides investors with valuable insights into the emotional factors influencing market movements, which are often missed by conventional methods.

> The strength of MarketMind lies in its ability to connect financial data with market sentiment. By correlating sentiment with stock price shifts, it helps investors and analysts anticipate market trends and make more informed decisions. As real-time sentiment data becomes increasingly important, MarketMind offers a reliable tool for evaluating market sentiment, supporting better decision-making and improved risk management strategies.

### User Stories
- As an investor, I want to assess market sentiment to make informed investment decisions based on news and trends.
- As a financial analyst, I want to correlate sentiment analysis with stock price shifts to explore emotional factors driving market dynamics.
- As a data scientist, I want to implement advanced web scraping and sentiment analysis tools to provide accurate and timely insights into market sentiment.

<br><br>
<!-- Tech stack -->
<img src="./readme/title3.svg"/>

###  MarketMind is built using the following technologies:

- <span style="color: purple">**Financial News Data Collection**</span>: A custom web scraper was developed to automate the extraction of financial news articles from Yahoo Finance for specific stock symbols (e.g., AAPL). This streamlined data collection allowed for the retrieval of up-to-date news articles with minimal manual intervention. By using <span style="color:#dabfff">**<a href="https://www.selenium.dev/" style="color:#dabfff">Selenium</a>**</span> and <span style="color:#dabfff">**<a href="https://www.crummy.com/software/BeautifulSoup/" style="color:#dabfff">BeautifulSoup</a>**</span>, the scraper navigated dynamic web pages, handling infinite scrolling and dynamic content loading, ensuring the extraction of relevant article information. The process was further optimized using <span style="color:#dabfff">**<a href="https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor" style="color:#dabfff">ThreadPoolExecutor</a>**</span> for concurrent scraping, improving efficiency and reducing time.<br>
Irrelevant and promotional content was filtered out, and duplicate articles were removed. Dates were standardized, and the cleaned dataset was stored as a CSV for future analysis.

- <span style="color:#dabfff">**Stock Prices Data Collection**</span>: Stock price data was collected using <span style="color:#dabfff">**<a href="https://pypi.org/project/yfinance/" style="color:#dabfff">yfinance</a>**</span> library, focusing on intraday data to match news article publication dates. Since yfinance imposes restrictions on retrieving data (limited to seven days at a time for one-minute intervals), the process was iteratively structured. Retrieved stock data was stored in CSV format, allowing easy integration with the news dataset. Each article was then assigned the stock price closest to its publication timestamp, ensuring clean, consistent data.<br>
The stock price dataset was processed to align with the articles' timestamps by removing the seconds component and converting all dates to UTC for consistency. Python libraries <span style="color:#dabfff">**<a href="https://docs.python.org/3/library/datetime.html" style="color:#dabfff">datetime</a>**</span> and <span style="color:#dabfff">**<a href="https://pypi.org/project/pytz/" style="color:#dabfff">pytz</a>**</span> were used for handling date formatting and time zone conversion.

- <span style="color:#dabfff">**Sentiment Analysis**</span>: <span style="color:#dabfff">**<a href="https://github.com/cjhutto/vaderSentiment" style="color:#dabfff">VADER (Valence Aware Dictionary and Sentiment Reasoner)</a>**</span> was used for sentiment analysis of financial news articles. It provided four key sentiment scores: positive, negative, neutral, and a compound score. Each article's sentiment was classified as Positive, Negative, or Neutral based on the compound score.

- <span style="color:#dabfff">**Labeling**</span>: Stock price changes were labeled relative to article publication times. Labels were assigned based on percentage changes in stock prices using predefined thresholds. A label of 1 indicated an increase, -1 a decrease, and 0 stable prices. Three time intervals were considered: 30 minutes, 6 hours, and 1 day, with thresholds adjusted according to the time horizon.

- **Visualizations**: Various visualizations were created using **[Matplotlib](https://matplotlib.org/)** and **[Seaborn](https://seaborn.pydata.org/)** to illustrate the relationship between compound sentiment scores and stock price changes, including scatter plots and violin plots.

- **Statistical Tests**: 
   - The **Shapiro-Wilk test** from **[SciPy](https://www.scipy.org/)** assessed whether compound sentiment scores and percentage changes in stock prices followed a normal distribution. A significant p-value (< 0.05) would indicate a deviation from normality.
   
   - A **Spearman rank correlation test** was conducted using **[SciPy](https://www.scipy.org/)** to evaluate the monotonic relationship between sentiment scores and stock prices. A significant p-value (< 0.05) suggests a meaningful relationship.
   
   - The **Pearson correlation test**, also from **[SciPy](https://www.scipy.org/)**, examined the linear relationship between sentiment scores and stock prices. A low p-value (< 0.05) indicates a significant correlation, meaning changes in one variable are associated with changes in the other.


<br><br>


<!-- Database Design -->
<!-- <img src="./readme/title5.svg"/>

###  Star Schema:
The star schema for TerrAlert offers several advantages, including simplicity, as its clear structure with a central fact table and surrounding dimension tables makes data access intuitive and easy to navigate. It provides improved performance for queries on large datasets, crucial for analyzing both historical records and real-time data.

<img src="./readme/ER_Diagram.png"/>


<br><br> -->


<!-- Implementation -->
<img src="./readme/title6.svg"/>


<!-- ### User Screens (Power BI report)

| Landing Page                          | Overview                                |
| ----------------------------------------- | ----------------------------------------- |
| ![Demo](./readme/landing_page.png) | ![Demo](./readme/overview.png) |

| Country-Specific Drill-Through          | Sneak Peek                          |
| --------------------------------- | -------------------------------------- |
| ![Demo](./readme/country_drill_through.png) | ![Demo](./readme/sneak_peek1.gif) | -->

### News Extraction

| Running the Scraper                         | 
| ----------------------------------------- | 
| <img src="./readme/scraper.mp4" width="800" height="auto" /> |



<br><br> 


<!-- Unit Testing -->
<!-- <img src="./readme/title9.svg"/>

###  Ensuring Quality: The Importance of Data Validation:

- Data validation ensures the accuracy of the ETL process through detailed logging. During extraction, logs track data sources and any access issues. In transformation, they document processing steps and validation checks. The loading phase logs capture the success of data uploads and any conflicts. These logs are essential for monitoring data flow and maintaining data quality, ensuring the final dataset is reliable for analysis.
<br><br>

| Logs                        | 
| ----------------------------------------- | 
| ![Demo](./readme/logs.png) |


<br><br> -->


<!-- How to run -->
<img src="./readme/title10.svg"/>

> To set up the MarketMind locally, follow these steps:

<!-- ### Prerequisites

Make sure to have the following dependencies installed:

- PostgreSQL
- Required Python libraries (listed in requirements.txt)

### Installation
1. Clone the repository:
   ```
      git clone https://github.com/joudabihaidar/TerrAlert.git
   ```
2. Install the necessary Python libraries:
   ```
      pip install -r requirements.txt
   ```
Now, you should be able to run the project locally and explore its features. -->

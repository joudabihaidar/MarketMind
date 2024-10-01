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
- <span style="color:#dabfff">**Statistical Tests**</span>: Transitioning to statistical analyses, the <span style="color:#dabfff">**Shapiro-Wilk test**</span> was initiated to evaluate the distribution of compound sentiment scores and percentage changes in stock prices. The formula for the test is given by:

   \[
   w = \frac{(\sum_{i=1}^{n} a_i x_{(i)})^2}{\sum_{i=1}^{n} (x_i - \bar{x})^2}
   \]

   The Shapiro-Wilk test is used to assess whether a given sample comes from a normally distributed population. In this context, it was employed to evaluate whether the compound sentiment scores and percentage changes in stock prices followed a normal distribution. 

   The test compares the observed distribution of data to what would be expected under the assumption of normality. The null hypothesis is that the data is normally distributed, while the alternative hypothesis is that it is not. A significant p-value (usually < 0.05) indicates evidence against the null hypothesis, suggesting that the data significantly deviates from normality. Therefore, a significant p-value would indicate that either the compound sentiment scores, the percentage changes in stock prices, or both deviate significantly from a normal distribution, affecting the validity of subsequent statistical analyses that assume normality, such as parametric tests like the Pearson correlation test.<br>

   Next, a <span style="color:#dabfff">**Spearman rank correlation test**</span> was employed to assess the strength and direction of the monotonic relationship between compound sentiment scores and percentage changes in stock prices. The formula for this test is:

   \[
   \rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}
   \]

   The Spearman rank correlation test is a non-parametric statistical test used to evaluate the strength and direction of the relationship between two variables. Unlike the Pearson correlation coefficient, which assesses linear relationships, the Spearman test evaluates monotonic relationships, where variables consistently increase or decrease together, though not necessarily at a constant rate. This makes the Spearman test more robust to non-linear associations and outliers.<br>

   The test ranks the values of each variable independently and calculates the difference in ranks for each pair of observations. A significant Spearman correlation coefficient, indicated by a p-value < 0.05, suggests evidence of a monotonic relationship between the variables, implying that as one variable increases or decreases, the other tends to change in the same direction.<br>

   Finally, a <span style="color:#dabfff">**Pearson correlation test**</span> was conducted to investigate the linear relationship between compound sentiment scores and percentage changes in stock prices. The formula for the Pearson correlation coefficient is:

   \[
   r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
   \]

   The Pearson correlation coefficient provides a measure of the strength and direction of the linear relationship between the two variables. A coefficient approaching 1 indicates a strong positive linear correlation, while a coefficient nearing -1 suggests a strong negative correlation. A coefficient close to 0 signifies a weak or negligible linear relationship.<br>

   The statistical significance of the observed correlation coefficient is evaluated by the Pearson correlation test p-value. A low p-value (< 0.05) suggests a significant linear relationship between the variables, indicating that changes in stock prices are meaningfully associated with changes in compound sentiment scores. Conversely, a high p-value denotes no meaningful linear association, implying the correlation may have occurred at random.


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
| ![Demo](./readme/country_drill_through.png) | ![Demo](./readme/sneak_peek1.gif) |

### User Screens (Python)

| Real Time Earthquake Monitoring                          | 
| ----------------------------------------- | 
| <img src="./readme/earthquakes.gif" width="800" height="auto" /> |
<!-- | ![Demo](./readme/earthquake.gif) | -->


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

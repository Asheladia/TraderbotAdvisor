# **TraderbotAdviser**

### **Contributors : Alpa Sheladia, Brian Withrow, Lee R. Redfearn, Mischelle Massey, Nathan Bratz**
                                           


The purpose of this project is to investigate the effect of several variables on the prediction of stock prices with emphasis on the analysis of the correlation between stock price and news media. Moreover, prediction of future stock movement using the Convolutional Neural Network model allows the User to choose a company from the S&P 500 and predict the price movement of a company's stock on the next trading move based on current sentiment (Vader) from GoogleNews articles related to such company.


![Fintech_project_2](Images/Robo-Advisors.png)

Looking for executable orders using automated pre-programmed trading instructions accounting for variables such as VIX, Beta, price, sentiment, and volume?
You've come to the right place, we'll have your back using vix score volitality measurement to decide whether to buy, sell or hold on to your investment. In this project, we'll be comparing prices of the past three to four years. We will follow corporations and build a algorethmic robo advisor that can guide you with your investments... it'll research new media and past stock patterns to come up with the best decision for your stock invesment so you don't have to spend time following market trends. Our bot will be equiped for trading attempts that leverage the speed and computational resources of computers relative to human traders. According to a Wallstreet journal article, a study in 2019 showed that around 92% of trading in the Forex market was performed by trading algorithms rather than humans.

Focusing on some of the most volatile industries as below. 

![Fintech_project_2](Images/Americanairline.png)
![Fintech_project_2](Images/Apple.png)
![Fintech_project_2](Images/xom.png)
![Fintech_project_2](Images/BTC.png) 
![Fintech_project_2](Images/pfe.png)
![Fintech_project_2](Images/download.png)



#### **Indutries:**

Airline = American Airline (AAL)
Tech = Apple (AAPL)
Oil & Gas = Exxon (XOM)
Crypto = Bitcoin (BTC)  
Medical = pfizer (PFE)
media = Zoom(ZM)

#### NOTE: You must have active keys from the following APIs to run this program:

   Quandl API : https://www.quandl.com/tools/api
  IEX Finance: https://iexcloud.io/
  News API: https://newsapi.org/
  Alpha Vantage: https://www.alphavantage.co/
  Yahoo Finance: https://finance.yahoo.com/quote/API/
  Google News :https://newsapi.org/s/google-news-api
  Newspaper 3K: https://newspaper.readthedocs.io/en/latest/user_guide/advanced.html
  
#### **Construction**

We will collect data that seems reasonable in influencing price such as Closing Price (Adjusted), Volume, VIX, Beta, Sentiment Scores (Factors/Features). 

* Measuring Sentiment in Financial Articles:
Terms in finance can vary in meaning depending on context; ex: “decrease” in dividends or “decrease” in overall expenses.
Standard sentiment analysis methods cannot be expected to work well on financial articles since such articles are intended to be written objectively rather than subjectively.

* Computing Sentiment Scores
We used Newspaper3k API to extract articles from links generated from GoogleNews API. Manual tokenization was used in articles without nltk using regular expression
LM to compute various sentiment proportions (positive, negative, uncertainty,etc.) Results were compiled into a DataFrame object and stored for further use.



#### **Possible New Metrics/Tools to Use:**

![Fintech_project_2](Images/Stock_Market_Numbers_Concept.png)

●Cross Validation (Better estimation of test error)

●Use nltk and tensorflow for neural networks on natural language processing

●Graph performance results using multiple layers, ​network types​ and ​learning rates

● we used Googlenews API to pull articles

● we used YahooFinance to pull stock data and articles

● we used training a 2D-convolutional neural network

● we used Loughran-McDonald Master Dictionary to get sentiments 

● We made new class stockscurb to collect, organized data for the assets.



![Fintech_project_2](Images/sa-cummalative-returns.png)




## **TraderbotAdvisor** 

![Fintech_project_2](Images/FAB-robo-072916-adobe.png)
 



#### **Questions to be solved by the end of the project:**

● What are your findings of the news media's contribution in the stock market volatility over past three-four years?

We used several features and academic research to figure out that media context plays a crucial role in market volatility. We redefined sentiment and used multivariant analysis to extract data from news articles and identify the effect on the future prices of stocks.
 

● Is this a supervised or unsupervised learning task? What are data features and what is the target variable? If unsupervised, what are the data features and what do we hope to find?
 This is considered to be a supervised learning task since the data is provided with target variables as the next day's price . Data features include parameters, prices,VIX, Sentiment, Closing price and Volume. 


● How did the Machine learning play a role in it?
In deep learning, a Convolutional Neural Network is a class of deep neural networks, most commonly applied to analyzing visual imagery. There are also shift invariant or space invariant artificial neural networks, based on their shared-weight architecture and translation invariance characteristics. We repurposed the CNN to become a multivarious signal to achieve readable results and produce information from all features and identify the feature significant enough to predict the price for next day. 

![Fintech_project_2](Images/Stock_Cyborg-Dabbing.png)

 

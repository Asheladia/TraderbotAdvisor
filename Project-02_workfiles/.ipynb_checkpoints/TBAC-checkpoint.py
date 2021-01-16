"""Class contains main tools used for project"""
# Import libraries and dependencies
import numpy as np                                                        # for numpy
import pandas as pd                                                       # for pandas
import os                                                                 # for extracting environment variables
from datetime import datetime,timedelta                                   # for working with datetimes and algebra on dates
import requests                                                           # for requests to urls
from dotenv import load_dotenv                                            # loading environment variables
import re                                                                 # for regular expressions
import time                                                               # used to delay execution of sequences; if necessary
from sqlalchemy import create_engine                                      # used to pull data from sql server
import quandl                                                             # for using hte Quandl api
from GoogleNews import GoogleNews                                         # for using Google API
from newspaper import Article                                             # for extracting information from hyperlinks
import re                                                                 # for using regular expression
from nltk.tokenize import sent_tokenize                                   # for tokenizing words
import yfinance as yf                                                     # for working with yahoo finance api
import Generic_Parser_Mod                                                 # for using constructed sentiment function
load_dotenv()                                                             # Load .env enviroment variables
appkey=os.getenv("ALPHA_KEY")                                             # storing API key for AL
quandl_key=os.getenv("QUANDL_API_KEY")                                    # Getting the api for quandl requests


#Ticker mapping
tick_map={"AAPL":"APPLE","FB":"FACEBOOK","PFE":"PFIZER","BTC":"BITCOIN","AAL":"AMERICAN AIRLINES","AMZN":"AMAZON","XOM":"EXXON","ZM":"ZOOM"}

#List of Financial Sources (For future research, we would like to use a different API and restrict search to financial news articles)
fin_sources=["reuters",'bloomberg','market watch','cnbc', 'wall stree journal', 'cnn','nbc news', 'the wall street journal','the new york times', 'business insider']

#"""-----------------           TABC TOOLS !!!!           ---------------"""

#############                                                                          #######################
##########################             Assisting Functions                ####################################   
#############                                                                           ######################
"""Functions that are used in the code to simplify certain tasks"""


####################################     DATA CLEAN FUNCTION       #########################################  
def data_clean(df):
    """Cleans a data set and removes all None/NA entries"""
    if( sum(df.isnull().sum())>0 ):                                                  # checks if there are any missing values
        df.fillna(method='ffill')                                                    # fills entries using forward fill
        df.dropna(axis=0,inplace=True)                                               # gets rid of rows win NA values
    return(df)                                    # returns the DataFrame
        
    
    
####################################     GET VIX FUNCTION       ######################################### 
def VIX_update():
    """Function pulls in VIX data from Quandl API"""                                 # Description
    result=quandl.get("CHRIS/CBOE_VX1", authtoken=quandl_key, collapse="daily")      # request pulling VIX data
    result.to_csv('Quandl_VIX_Data/VIX_DAILY.csv')                                   # saves VIX data to csv file
    print("Data successfully stored.")
    
    
####################################     GET SP500 FUNCTION       #########################################
def sp500_update():
    """Function pulls in S&P500 data from Quandl API"""                              # Description
    spx = yf.Ticker("^GSPC")                                                         # ticker used to identify S&P500
    df = spx.history(period="max")                                                   # gets all available data
    df.to_csv("Yahoo_Finance_Data/SP500_DAILY.csv")                                  # saves S&P500 data to csv file
    


####################################       PROCESS TEXT         #########################################
def process_text(text):
    """Function recieves text, cleans it, and returns tokens"""
    regex = re.compile("[^a-zA-Z ]")                                                 # Making our regular expression
    clean_text = regex.sub(' ', text)  #consider hyphenated words                    # erasing nonalphabetic characters
    clean_text = re.findall('[a-zA-Z]+',clean_text)                                  # performing tokenization on clean text
    clean_text= [token.upper() for token in clean_text]                              # makes tokens uppercase for dictionary
    return clean_text                                                                # returning cleaned tokens
 

    
    
               
####################          DEFINING THE CLASS USED IN FINANCIAL ANALYSIS.       ##########################
class StockScrub:
    """ This class is for pulling financial information for specfic companies for a specific time range
        
     Attributes
        ticker=contains ticker symbols of specified companies
    """
###############    Initializing the Function
###############
    def __init__(self, ticker=["AAPL"]):                                                    # defining default inputs for class 
                
###############     Checking for Errors
        if not isinstance(ticker,list):                                                     # makes sure ticker is in right format
            raise TypeError("ticker must be a list")
#Setting class attributes
        self.ticker=ticker
    
    
#############################                                               ##############################     
#############################           CLOSING PRICES AND VOLUME           ############################## 
#############################                                               ################################
    def get_data(self):
        """Description: This function is used to collect information from stocks on closing prices and volume"""
        #stock_list=pd.DataFrame()                                                                                             # initialized DataFrame for company info
        for tick in self.ticker:                                                                                               # gets info for each stock ticker
###################   Initializing try instance
#############
########
####
            try:        # When ticker is BTC                                                                                   # initializing try instance
                if tick=="BTC":                                                                                                # what to do ticker is Bitcoin
                    query=f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={tick}&market=CNY&apikey={appkey}"
                    response=requests.get(query)                                                                               # making a query to AlphaVantage
                    data=response.json()                                                                                       # converting data in json object
                    D={}                                                                                                       # initialize dictionary
                    #Finish getting Bitcoin Data
                    D['date']=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data['Time Series (Digital Currency Daily)'].keys()]
                    D["close"]=[ float(data["Time Series (Digital Currency Daily)"][DATE]["4b. close (USD)"]) for DATE in data["Time Series (Digital Currency Daily)"]]
                    D["volume"]=[ float(data["Time Series (Digital Currency Daily)"][DATE]["5. volume"]) for DATE in data["Time Series (Digital Currency Daily)"]]
                   ################   Manipulating Subsequent DataFrames
                    D=pd.DataFrame(D)                                                                                          # creating DataFrame
                    D.set_index("date",inplace=True)                                                                           # setting Date column to be the index
                    D.sort_index(ascending=True,inplace=True)                                                                  # sorting the index
                    D=data_clean(D)                                                                                            # cleans the dataframe
                    file_path=f"AlphaVantage_Asset_Data/AV_{tick}_data.csv"                                                    # constructing file path to store data
                    D.to_csv(file_path)                                                                                        # saving DataFrame to CSV               
                else:    #When ticker is not BTC
                  #Defining API Query
                    query=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={tick}&outputsize=full&apikey={appkey}"
                    response=requests.get(query)                                                                               # Making request with parameters
                    data=response.json()                                                                                       # converting data in json object
                    D={}                                                                                                       # initialize dictionary             
                    ##############         Collecting data from json object and putting it into a DataFrame
                    #############
                    ############### Use of List Comprehensions to Collect Necessary Data: *** PRICE AND VOLUME VALUES MUST BE CONVERTED TO FLOATS.  ****
                    
                D["date"]=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data['Time Series (Daily)']]
                D["close"]=[ float(data['Time Series (Daily)'][DATE]['5. adjusted close']) for DATE in data['Time Series (Daily)']]
                D["volume"]=[ float(data['Time Series (Daily)'][DATE]['6. volume']) for DATE in data['Time Series (Daily)']]                       
                    #####                        
                    #########                       
                    #############                        
                    ################# Specifying the error type                                    
            except KeyError:                                                                                                   # specifying error
                print('KeyError. Trying again in 60 seconds...\n\n',end='\r')
                time.sleep(60)                                                                                                 # sleep time 60s
                print('Resuming Execution...\n\n',end='\r')
                               
                               
                #When ticker is BTC
                if tick=="BTC":                                                                                               # when the ticker is Bitcoin
                    query=f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={tick}&market=USD&apikey={appkey}"
                    response=requests.get(query)                                                                              # making a query to AlphaVantage
                    data=response.json()                                                                                      # converting data in json object
                    D={}                                                                                                      # initialize dictionary
                    #Finish getting Bitcoin Data
                    D['date']=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data['Time Series (Digital Currency Daily)'].keys()]
                    D["close"]=[ float(data["Time Series (Digital Currency Daily)"][DATE]["4b. close (USD)"]) for DATE in data["Time Series (Digital Currency Daily)"]]
                    D["volume"]=[ float(data["Time Series (Digital Currency Daily)"][DATE]["5. volume"]) for DATE in data["Time Series (Digital Currency Daily)"]]
                    ################   Manipulating Subsequent DataFrames
                    D=pd.DataFrame(D)                                                                                         # creating DataFrame
                    D.set_index("date",inplace=True)                                                                          # setting Date column to be the index
                    D.sort_index(ascending=True,inplace=True)                                                                 # sorting the index
                    #D=D[self.start:self.end]                                                                                 # refining to selection
                    D=data_clean(D)                                                                                           # cleans the dataframe
                    file_path=f"AlphaVantage_Asset_Data/AV_{tick}_data.csv"                                                   # constructing file path to store data
                    D.to_csv(file_path)                                                                                       # saving DataFrame to CSV
                 #When ticker is not BTC
                else:           
                    #Defining API Query
                    query=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={tick}&outputsize=full&apikey={appkey}"
                    response=requests.get(query)                                                                              # Making request with parameters
                    data=response.json()                                                                                      # converting data in json object
                    D={}                                                                                                      # initialize dictionary             
                    ##############         Collecting data from json object and putting it into a DataFrame
                    #############
                    ############### For Dates
                D["date"]=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data['Time Series (Daily)']]
                D["close"]=[ float(data['Time Series (Daily)'][DATE]['5. adjusted close']) for DATE in data['Time Series (Daily)']]
                D["volume"]=[ float(data['Time Series (Daily)'][DATE]['6. volume']) for DATE in data['Time Series (Daily)']]                           
################   Manipulating Subsequent DataFrames
            D=pd.DataFrame(D)                                                                                                 # creating DataFrame
            D.set_index("date",inplace=True)                                                                                  # setting Date column to be the index
            D.sort_index(ascending=True,inplace=True)                                                                         # sorting the index
            #D=D[self.start:self.end]                                                                                         # refining to selection
            D=data_clean(D)                                                                                                   # cleans the dataframe
            file_path=f"AlphaVantage_Asset_Data/AV_{tick}_data.csv"                                                           # constructing file path to store data
            D.to_csv(file_path)                                                                                               # saving DataFrame to CSV
            print('Data successfully stored.')
            
            
            
            
            
            
            
            
####################################       GET SENTIMENT         #########################################
    def get_sentiment(self,start='2019-03-29',end=datetime.now().strftime("%Y-%m-%d")):
        """Gets daily sentiment using news sources from Google News for the specified time range"""
        start=datetime.strptime(start,"%Y-%m-%d").strftime("%m/%d/%Y")                                                        # puts start time in GoogleNews format
        end=datetime.strptime(end,"%Y-%m-%d").strftime("%m/%d/%Y")                                                            # puts end time in GoogleNews format
        googlenews=GoogleNews(lang='en',start=start,end=end,encode='utf-8')                                                   # creating object for collecting news
        googlenews.search(tick_map[self.ticker[0]])                                                                           # specifying the company
        
        
        # Getting Google Results
        for i in range(1,50):
            googlenews.getpage(i)                                                                                             # loops through google pages
            result=googlenews.result()                                                                                        # stores results
            df=pd.DataFrame(result)                                                                                           # appends results to DataFrame
        df.drop_duplicates(['link'],keep='first',inplace=True)                                                                # removes duplicate articles via links
        
        
        # Collecting Text From Articles
        L=[]                                                                                                                  # initializing empty list
        for ind in df.index:
            try:                                                                                                              # "try" for forbidden websites
                D={}                                                                                                          # initializing the dictionary
                article = Article(df['link'][ind])                                                                            # extracting information from articles
                article.download()
                article.parse()
                article.nlp()
                D['Date']=df['datetime'][ind]                                                                                 # storing information from articles
                D['Media']=df['media'][ind]
                D['Title']=article.title
                D['Article']=article.text
                D['Summary']=article.summary
                L.append(D)                                                                                                   # appending results to list
            except:
                pass
        news_df=pd.DataFrame(L)                                                                                               # make DataFrame from list
        #Preliminary Cleaning
        news_df1=news_df.dropna(axis=0)                                                                                       # dropping old "date" column
        news_df2=news_df1[news_df1['Media']!=""].set_index('Date').sort_index(ascending=True)                                 # remove articles with no media source
        news_df2=news_df2[news_df2['Article'].values!=""]                                                                     # remove articles with no content
        # Making time format %Y-%m-%d and Additional Cleaning
        new_time_format=list(pd.Series(news_df2.index).apply(lambda DATE :DATE.strftime("%Y-%m-%d")).values)                  # string form of new time format   
        new_time_format=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in new_time_format]                                      # datetime form of new time format
        news_df2.index=new_time_format                                                                                        # apply new time format
        news_df2.drop(columns=['Summary','Title'],inplace=True)                                                               # dropping columns
        news_df2=Generic_Parser_Mod.LM_sentiment(news_df2)                                                                    # DataFrame of sentiment scores
        
        
        # Handling of Duplicated Entries
        duplicate_index=news_df2.index[news_df2.index.duplicated()]                                                           # identify duplicate time entries
        collapsed_dates=list(duplicate_index.unique())                                                                        # collapsing duplicate dates
        news_df3=[news_df2.loc[collapsed_dates[i]].median() for i in range(len(collapsed_dates))]                             # collapsing info in duplicate entries
        news_df3=pd.DataFrame(news_df3)                                                                                       # DataFrame of collapsed info
        news_df3.index=collapsed_dates                                                                                        # new collapsed info
        
        
        #Making new DataFrame without Duplicates
        news=news_df2.loc[[news_df2.index[i] not in duplicate_index for i in range(len(news_df2.index))]].append(news_df3,sort=False)
        
        
        # Post-Cleaning, due to unstable nature of API
        news=news.loc[start:end]                                                                                              # only articles from selected period
        news.sort_index(ascending=True,inplace=True)                                                                          # order by date
        news.to_csv(f"Sentiment_Data/{self.ticker[0]}_scores.csv",index='date')                                         # storing the sentiment data
        return news                                                                                                           # return sentiment scores
    
    
    
    
    
    
    
    
    
    
    
####################################     DATA COMPILE       #########################################                
    def data_compile(self,start='2019-03-29',end=datetime.now().strftime("%Y-%m-%d"),beta_period=20):
        """Takes a given ticker symbol and combines data from AlphaVantage, Quandl and sentiment analysis"""
        start=datetime.strptime(start,"%Y-%m-%d")                                                                             # converting start time to datetime
        end=datetime.strptime(end,"%Y-%m-%d")                                                                                 # converting end time to datetime
        file_path=f"AlphaVantage_Asset_Data/AV_{self.ticker[0]}_data.csv"                                                     # Defining the file path
        AV_df=pd.read_csv(file_path,index_col='date',parse_dates=True,infer_datetime_format=True)                             # reading data from file path
        VIX_df=pd.read_csv('Quandl_VIX_Data/VIX_DAILY.csv',index_col='Trade Date',parse_dates=True,infer_datetime_format=True,usecols=['Close','Trade Date'])
        VIX_df.index.name='date'                                                                                              # adjusting index column name
        VIX_df.columns=['VIX']                                                                                                # adjusting DataFrame column name
        beta_df=self.get_beta(start=start,end=end,period=beta_period)                                                         # collecting average beta values
        
        #Getting the Sentiment DataFrame
        senti_df=pd.read_csv(f"Sentiment_Data/{self.ticker[0]}_scores.csv",index_col=[0],parse_dates=True,infer_datetime_format=True)
        senti_df.index.name='date'                                                                                            # naming the index
        #Combining all the DataFrames        
        senti_df=senti_df[start:end]                                                                                          # slice senti_df
        combined_df=pd.concat([AV_df.loc[start:end],VIX_df.loc[start:end],beta_df],axis=1,join="inner")                       # joining DataFrames on common index
        combined_df=data_clean(combined_df)                                                                                   # combining all DataFrames 
        combined_df=combined_df.join(senti_df,how="left").fillna(value=0)                                                     # join DataFrames; fill  NAs with zeros
        if combined_df.empty:                                                                                                    # when we obtain an empty DataFrame
            combined_df=pd.concat([AV_df.loc[start:end],VIX_df.loc[start:end],beta_df,senti_df],axis=1,join="inner") 
        return combined_df                                                                                     
  





 ####################################       GET BETA         #########################################  
    def get_beta(self,start='2019-03-29',end=datetime.now().strftime("%Y-%m-%d"),period=15):
        """Computes P-Day rolling beta of given stock data, where period=P. There will be NAs but will remove them from collective DataFrame"""
        file_path=f"AlphaVantage_Asset_Data/AV_{self.ticker[0]}_data.csv"                                                     # Defining the file path
        stock_df=pd.read_csv(file_path,index_col='date',parse_dates=True,infer_datetime_format=True)                          # reading data from file path
        stock_df=stock_df.loc[start:end]                                                                                      # slicing stock data
        sp500_df=pd.read_csv("Yahoo_Finance_Data/SP500_DAILY.csv",index_col='Date',parse_dates=True,infer_datetime_format=True,usecols=["Date","Close"]) # SP500 data
        sp500_df=data_clean(sp500_df.loc[start:end])                                                                          # slicing S&P500 DataFrame
        daily_returns_stock_df=stock_df.pct_change()                                                                          # computing daily returns for stock
        daily_returns_sp500_df=sp500_df.pct_change()                                                                          # computing daily returns for S&P500
        rolling_covariance = daily_returns_stock_df['close'].rolling(window=period).cov(daily_returns_sp500_df)               # computing rolling covariance w/ S&P500
        rolling_variance = daily_returns_sp500_df.rolling(window=period).var()                                                # computing variance of S&P500
        rolling_beta = rolling_covariance / rolling_variance                                                                  # Computing beta-average values
        rolling_beta.columns=['beta']                                                                                         # changing column name
        return rolling_beta                                                                                                   # returning rolling_beta DataFrame
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
import re                                                                 # for using regular expression
from nltk.tokenize import sent_tokenize                                   # for tokenizing words

load_dotenv()                                                             # Load .env enviroment variables
appkey=os.getenv("ALPHA_KEY")                                             # storing API key for AL
quandl_key=os.getenv("QUANDL_API_KEY")                                    # Getting the api for quandl requests




#This will be useful if we decide to include additional features
#Prelim Dictionary : Keeps track of items in API Request
mk={"Date" : "fiscalDateEnding", "Symbol": "symbol", "Net Income" : "netIncome",'Short Term Debt':'shortTermDebt',
   'Long Term Debt':'longTermDebt',"Total Liabilities":"totalLiabilities","Total Share Holder Equity":"totalShareholderEquity","Free Cash Flow":"changeInCashAndCashEquivalents","Reported EPS":"reportedEPS","Estimated EPS":"estimatedEPS"}


#Ticker mapping
tick_map={"AAPL":"APPLE","FB":"FACEBOOK","PFE":"PFIZER","BTC":"BITCOIN"}

#List of Financial Sources
fin_sources=["reuters",'bloomberg','market watch','cnbc', 'wall stree journal', 'cnn','nbc news', 'the wall street journal','the new york times', 'business insider']



#"""-----------------           TABC TOOLS !!!!           ---------------"""
#"""  Ideas of functions from previous project"""


#Computing Rolling Beta Averages
 #def BETA(df1,df2,WIN):
 #   """Computes rolling beta averages
 #   df1=first DataFrame
 #   df2=second DataFrame (reference DataFrame)
 #   W=specified window for computations"""
    
 #   rolling_covariance = df1.rolling(window=WIN).cov(df2) #gets rolling covariance between DataFrames
 #   rolling_variance = df.rolling(window=WIN).var() # gets rolling variance of DataFrame
  #  rolling_beta = rolling_covariance / rolling_variance #compute rolling beta
  #  return(rollinb_beta)

#Computing Bollinger Bands
# def BBands(df,WIN,S):
 #   """ Computes the Bollinger Bands for given data over specific rolling window
 #   df=DataFrame containing data
  #  WIN=specified window for computations
  #  S=multiple of standard deviations to use for Bollinger Bands; must specify positive or
  #  negative"""
  #  BB = df.rolling(window=WIN).mean() +( S * df.rolling(window=W).std()) #gets Bollinger Bands

    #upper_band.plot(ax=ax)
    #lower_band.plot(ax=ax)
  #  return(BB)


# Horizontal Analysis
 #def HA(df):
 #   """Performs horizontal analysis on data frame"""
    #computes percent changes for horizontal analysis
    #return(df_HA)

#############                                                                          #######################
##########################             Assisting Functions                ####################################   
#############                                                                           ######################
"""Functions that are used in the code to simplify certain tasks"""



###################################     KEYFIND       ######################################################
def keyfind(D,string):
    """Description: Searches through keys of a dictionary and looks for a match, after keys have been converted to lowercase format"""
    
    L=[key for key in D.keys()]                                                                                                   # gets list of keys from dictionary
    I=L[[key.lower()==string for key in L].index(True)]                                                                           # boolean index to locate dictionary key 
    return(I)                                                                                                                     # returns the corresponding key from the dictionary
    

###################################       MAPKEY        ###################################################
def mapkey(string):
    string=string.lower().replace(" ","")
    return(string)


####################################     DATA CLEAN FUNCTION       #########################################  
def data_clean(df):
    """Cleans a data set and removes all None/NA entries"""
    if( sum(df.isnull().sum())>0 ):     #checks if there are any missing values
        df.fillna(method='ffill')       #fills entries using forward fill
    return(df)                          #returns the DataFrame
        
    
    
####################################     GET VIX FUNCTION       ######################################### 
def VIX_update():
    """Function pulls in VIX data from Quandl API"""                                                                              # Description
    result=quandl.get("CHRIS/CBOE_VX1", authtoken=quandl_key, collapse="daily")                                                   # request pulling VIX data
    result.to_csv('Quandl_VIX_Data/VIX_DAILY.csv')                                                                                # saves VIX data to csv file
    print("Data successfully stored.")
    
    
####################################     GET SP500 FUNCTION       #########################################
def sp500_update():
    """Function pulls in S&P500 data from Quandl API"""                                                                           # Description
    result=quandl.get("BCIW/_INX", authtoken=quandl_key,collapse='daily',start_date="2000-01-01", end_date=datetime.now().strftime("%Y-%m-%d")) # request pulling S&P500 data
    result.to_csv('SP500_DAILY.csv')                                                                                              # saves S&P500 data to csv file
    

####################################       GET BETA         #########################################  
def get_beta(stock_df,period):
    """Computes P-Day rolling beta of given stock data, where period=P. There will be NAs but will remove them from collective DataFrame"""
    sp500_df=pd.read_csv("SP500_DAILY.csv",index_col='Date',parse_dates=True,infer_datetime_format=True,usecols=["Date","Close"]) # getting S&P500 data w/ specific columns
    sp500_df.loc[stock_df.index[0]:stock_df.index[-1]]                                                                            # slicing S&P500 DataFrame
    daily_returns_stock_df=stock_df.pct_change()                                                                                  # computing daily returns for stock
    daily_returns_sp500_df=sp500_df.pct_change()                                                                                  # computing daily returns for S&P500
    rolling_covariance = daily_returns_stock_df.rolling(window=period).cov(daily_returns_sp500_df)                                # computing rolling covariance w/ S&P500
    rolling_variance = daily_returns_sp500_df.rolling(window=period).var()                                                        # computing variance of S&P500
    rolling_beta = rolling_covariance / rolling_variance                                                                          # Computing beta-average values
    return rolling_beta                                                                                                           # returning rolling_beta DataFrame


####################################       CLEAN TEXT         #########################################
def process_text(text):
    """Function recieves text, cleans it, and returns tokens"""
    regex = re.compile("[^a-zA-Z ]")                                                                                              # Making our regular expression
    clean_text = regex.sub('', text)                                                                                              # erasing nonalphabetic characters
    clean_text = re.findall('[a-zA-Z]+',clean_text)                                                                               # performing tokenization on clean text
    clean_text= [token.upper() for token in clean_text]                                                                           # makes tokens uppercase for dictionary
    return clean_text                                                                                                             # returning cleaned tokens
 

               
####################          DEFINING THE CLASS USED IN FINANCIAL ANALYSIS.       ##########################
class StockScrub:
    """ This class is for pulling financial information for specfic companies for a specific time range
        
     Attributes
        ticker=contains ticker symbols of specified companies
    """
###############    Initializing the Function
###############
    def __init__(self, ticker=["AAPL"]):                          #defining inputs for class 
                
###############     Checking for Errors
        if not isinstance(ticker,list):
            raise TypeError("ticker must be a list")
#Setting class attributes
        self.ticker=ticker
    
    
#############################                                               ##############################     
#############################           CLOSING PRICES AND VOLUME           ############################## 
#############################                                               ################################
    def get_data(self):
        """Description: This function is used to collect information from stocks on closing prices and volume"""
        #stock_list=pd.DataFrame()                                                                                             # initialized DataFrame to hold company info
        for tick in self.ticker:                                                                                               # gets info for each stock ticker
###################   Initializing try instance
#############
########
####
            try:                                                                                                               # initializing try instance
            #When ticker is BTC
                if tick=="BTC":                                                                                                # when the ticker is Bitcoin
                    query=f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={tick}&market=CNY&apikey={appkey}"
                    response=requests.get(query)                                                                               # making a query to AlphaVantage
                    data=response.json()                                                                                       # converting data in json object
                    D={}                                                                                                       # initialize dictionary
                    #Finish getting Bitcoin Data
                    D['date']=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data['Time Series (Digital Currency Daily)'].keys()]
                    D["close"]=[ float(data["Time Series (Digital Currency Daily)"][DATE]["4b. close (USD)"]) for DATE in data["Time Series (Digital Currency Daily)"]]
                    D["volume"]=[ float(data["Time Series (Digital Currency Daily)"][DATE]["5. volume"]) for DATE in data["Time Series (Digital Currency Daily)"]]
                   ################   Manipulating Subsequent DataFrames
                    D=pd.DataFrame(D)                                                                                          # creating DataFrame and specifying the index
                    D.set_index("date",inplace=True)                                                                           # setting Date column to be the index
                    D.sort_index(ascending=True,inplace=True)                                                                  # sorting the index
                    #D=D[self.start:self.end]                                                                                  # refining to selection
                    D=data_clean(D)                                                                                            # cleans the dataframe
                    file_path=f"AlphaVantage_Asset_Data/AV_{tick}_data.csv"                                                    # constructing file path to store data
                    D.to_csv(file_path)                                                                                        # saving DataFrame to CSV
            #When ticker is not BTC                 
                else:
                  #Defining API Query
                    query=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={tick}&outputsize=full&apikey={appkey}"
                    #query=f"https://www.alphavantage.co/query?"                                                               # base query
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
                    D=pd.DataFrame(D)                                                                                         # creating DataFrame and specifying the index
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
                    #query=f"https://www.alphavantage.co/query?"                                                              # base query
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
            D=pd.DataFrame(D)                                                                                                 # creating DataFrame and specifying the index
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
        googlenews.get_news(tick_map[self.ticker[0]])                                                                         # specifying the company
        
        D={}                                                                                                                  # initializing empty dictionary
        D['date']=[article['datetime'] for article in googlenews.results()]                                                   # storing dates of articles
        D['site']=[article['site'] for article in googlenews.results()]                                                       # storing sites of articles
        D['content']=[article['title']+" "+article['desc'] for article in googlenews.results()]                               # storing content of articles
        D=pd.DataFrame(D)
        D.set_index("date",inplace=True)                                                                                      # setting date column to be the index
        D.sort_index(ascending=True,inplace=True)                                                                             # sorting the dates
        D['site']=D['site'].apply(lambda title: title.lower())                                                                # makes titles lowercase
        #D=D[[D.site[i] in fin_sources for i in range(len(D.site))]]                                                          # filters out unwanted sources
        
        # Making time format %Y-%m-%d
        new_time_format=list(pd.Series(D.index).apply(lambda DATE :DATE.strftime("%Y-%m-%d")).values)                         # string form of new time format        
        new_time_format=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in new_time_format]                                      # datetime form of new time format
        D.index=new_time_format                                                                                               # apply new time format
        
        #collapsing information in duplicate entries
        duplicate_index=D.index[D.index.duplicated()]                                                                         # identify duplicate time entries
        collapsed_dates=list(duplicate_index.unique())                                                                        # collapsing duplicate dates
        sites=[", ".join(list(D.loc[collapsed_dates[i]].site.unique())) for i in range(len(collapsed_dates))]                 # collapsing sites for duplicate dates
        contents=[", ".join(list(D.loc[collapsed_dates[i]].content)) for i in range(len(collapsed_dates))]                    # collapsing titles for duplicate dates
        Dict={'date':collapsed_dates,'site':sites,'content':contents}                                                         # make dictionary of collapsed info
        Dict=pd.DataFrame(Dict).set_index("date")                                                                             # convert dictionary to DataFrame
        
        #Making new DataFrame without Duplicates
        D_new=D.loc[[D.index[i] not in duplicate_index for i in range(len(D.index))]].append(Dict,sort=False)                 # append DataFrame to non-duplicate DataFrame
        D_new.sort_index(ascending=True,inplace=True)                                                                         # sorting index of new DataFrame
        D_new['content']=D_new['content'].apply(lambda text: process_text(text))                                              # process text for sentiment
        return D_new                                                                                                          # return newly refined DataFrame
    
    
####################################     DATA COMPILE       #########################################                
    def data_compile(self,start='2019-03-29',end=datetime.now().strftime("%Y-%m-%d")):
        """Takes a given ticker symbol and combines data from AlphaVantage, Quandl and sentiment analysis"""
        start=datetime.strptime(start,"%Y-%m-%d")                                                                             # converting start time to datetime
        end=datetime.strptime(end,"%Y-%m-%d")                                                                                 # converting end time to datetime
        file_path=f"AlphaVantage_Asset_Data/AV_{self.ticker[0]}_data.csv"                                                     # Defining the file path
        AV_df=pd.read_csv(file_path,index_col='date',parse_dates=True,infer_datetime_format=True)                             # reading data from file path
        VIX_df=pd.read_csv('Quandl_VIX_Data/VIX_DAILY.csv',index_col='Trade Date',parse_dates=True,infer_datetime_format=True,usecols=['Close','Trade Date'])
        VIX_df.index.name='date'                                                                                              # adjusting index column name
        VIX_df.columns=['VIX close']                                                                                          # adjusting DataFrame column name
        combined_df=pd.concat([AV_df.loc[start:end],VIX_df.loc[start:end]],axis=1,join="inner")                               # joining DataFrames on common index
        return combined_df     
  

 ####################################     GET INDICATORS       ######################################### 
    def get_indicators(self,start='2019-03-29',end=datetime.now().strftime("%Y-%m-%d")):
        """Gets indicator data for specified stock/crypto symbol"""
        start=datetime.strptime(start,"%Y-%m-%d")                                                                             # converting start time to datetime
        end=datetime.strptime(end,"%Y-%m-%d")                                                                                 # converting end time to datetime
        file_path=f"AlphaVantage_Asset_Data/AV_{self.ticker[0]}_data.csv"                                                     # Defining the file path
        AV_df=pd.read_csv(file_path,index_col='date',parse_dates=True,infer_datetime_format=True,usecols=['date','close'])    # reading data from file paths
        AV_df=AV_df.loc[start:end]                                                                                            #slices the DataFrame
        
        try:
            RSI_query=f"https://www.alphavantage.co/query?function=RSI&symbol={self.ticker[0]}&interval=daily&time_period=10&series_type=close&apikey={appkey}"
            response=requests.get(RSI_query)                                                                                  # making a query to AlphaVantage
            data=response.json()                                                                                              # converting data in json object
        except:
            print('KeyError. Trying again in 60 seconds...\n\n',end='\r')
            time.sleep(60)                                                                                                    # sleep time 60s
            print('Resuming Execution...\n\n',end='\r')
            RSI_query=f"https://www.alphavantage.co/query?function=RSI&symbol={self.ticker[0]}&interval=daily&time_period=10&series_type=close&apikey={appkey}"
            response=requests.get(RSI_query)                                                                                  # making a query to AlphaVantage
            data=response.json()                                                                                              # converting data in json object
  ################ Continuing data extraction          
        D={}                                                                                                                  # initializing dictionary for DataFrame
        D["date"]=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data["Technical Analysis: RSI"].keys()]                     # storing the dates as keys
        D["RSI"]=[ float(data["Technical Analysis: RSI"][DATE]["RSI"]) for DATE in data["Technical Analysis: RSI"]]           # storing the RSI values
        ################   Manipulating Subsequent DataFrames
        D=pd.DataFrame(D)                                                                                                     # creating DataFrame and specifying the index
        D.set_index("date",inplace=True)                                                                                      # setting Date column to be the index
        D.sort_index(ascending=True,inplace=True)                                                                             # sorting the index
        D=D[start:end]                                                                                                        # refining to selection
        combined_df=pd.concat([AV_df,D],axis=1,join="inner")                                                                  # joining DataFrames on common index
        combined_df=data_clean(combined_df)                                                                                   # cleans the dataframe
        return combined_df
        
            
        
        
        
        #https://www.alphavantage.co/query?function=RSI&symbol=USDEUR&interval=weekly&time_period=10&series_type=open&apikey=demo
        
        
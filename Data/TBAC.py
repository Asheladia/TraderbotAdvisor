# Import libraries and dependencies
import numpy as np                                                        #for numpy
import pandas as pd                                                       #for pandas
import os    
from datetime import datetime,timedelta                                   #for working with datetimes and algebra on dates
import requests                                                           #for requests to urls
from dotenv import load_dotenv                                            #loading environment variables
import re                                                                 #for regular expressions
import time                                                               #used to delay execution of sequences; if necessary
from sqlalchemy import create_engine                                      #used to pull data from sql server



load_dotenv()                                                             #Load .env enviroment variables
appkey=os.getenv("ALPHA_KEY")                                             #storing API key for AL




#This will be useful if we decide to include additional features
#Prelim Dictionary : Keeps track of items in API Request
mk={"Date" : "fiscalDateEnding", "Symbol": "symbol", "Net Income" : "netIncome",'Short Term Debt':'shortTermDebt',
   'Long Term Debt':'longTermDebt',"Total Liabilities":"totalLiabilities","Total Share Holder Equity":"totalShareholderEquity","Free Cash Flow":"changeInCashAndCashEquivalents","Reported EPS":"reportedEPS","Estimated EPS":"estimatedEPS"}



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
    
    
# Altman Z-Score
# def AltZ(ratios):
 #   """ Computes Altman's Bankruptcy Z-score to see if company is in danger of 
 #   going bankrupt"""
 #   weights=[1,2,3,4,5,6] #gets the weights that are assigned to Altman Z-score
 #   Z=0.0; #computing the Altman Z-score
 #   return(Z)

    
##########################.            Assisting Functions            #######################################   
"""Functions that are used in the code to simplify certain tasks"""




###################################     KEYFIND       ######################################################
def keyfind(D,string):
    """Description: Searches through keys of a dictionary and looks for a match, after keys have been converted to lowercase format"""
    
    L=[key for key in D.keys()]                                                 #gets list of keys from dictionary
    I=L[[key.lower()==string for key in L].index(True)]                         #creates boolean index to locate dictionary key 
    return(I)                                                                   #returns the corresponding key from the dictionary
    

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
        
    
    
####################          DEFINING THE CLASS USED IN FINANCIAL ANALYSIS.       ##########################

class StockScrub:
    """ This class is for pulling financial information for specfic companies for a specific time range
        
     Attributes
        ticker=contains ticker symbols of specified companies
        fin_stat_items=items extracted from financial statements
        balance_sheet_items=items extracted from balance sheet statements
        fin_ratios_items=items extracted from ratios statements
        cash_flow_items=items extracted from cash flow statements
    """
###############    Initializing the Function
###############
    def __init__(self, ticker=["AAPL"],start='2019-03-29',end=datetime.now().strftime("%Y-%m-%d")):    #defining inputs for class 
                
###############     Checking for Errors
        if not isinstance(ticker,list):
            raise TypeError("ticker must be a list")
#Setting class attributes
        self.ticker=ticker
        self.start=start
        self.end=end
    
    
#############################                                               ##############################     
#############################           CLOSING PRICES AND VOLUME           ############################## 
#############################                                               ################################
    def get_data(self):
        """Description: This function is used to collect information from stocks on closing prices and volume"""
        stock_list=pd.DataFrame()                                                                                            #initialized DataFrame to hold company info
        for tick in self.ticker:                                                                                             #gets info for each stock ticker
###################   Initializing try instance
#############
########
####
            try:                                                                                                              #initializing try instance
            #Defining API Query
                query=f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={tick}&apikey={appkey}"
                #query=f"https://www.alphavantage.co/query?"                                                                  #base query
                response=requests.get(query)                                                                                  #Making request with parameters
                data=response.json()                                                                                          #converting data in json object
                D={}                                                                                                          #initialize dictionary             
##############         Collecting data from json object and putting it into a DataFrame
#############
############### Use of List Comprehensions to Collect Necessary Data: *** PRICE AND VOLUME VALUES MUST BE CONVERTED TO FLOATS.  ****
                D["date"]=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data['Weekly Adjusted Time Series']]
                D["symbol"]=[tick for DATE in data['Weekly Adjusted Time Series']]
                D["close"]=[ float(data['Weekly Adjusted Time Series'][DATE]['5. adjusted close']) for DATE in data['Weekly Adjusted Time Series']]
                D["volume"]=[ float(data['Weekly Adjusted Time Series'][DATE]['6. volume']) for DATE in data['Weekly Adjusted Time Series']]                       
#####                        
#########                       
#############                        
################# Specifying the error type                                    
            except KeyError:                                                                                                  #specifying error
                print('KeyError. Trying again in 60 seconds...\n\n')
                time.sleep(60)                                                                                                #sleep time 60s
                print('Resuming Execution...\n\n')
            #Defining API Query
                query=f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={tick}&apikey={appkey}"
                #query=f"https://www.alphavantage.co/query?"                                                                   #base query
                response=requests.get(query)                                                                                  #Making request with parameters
                data=response.json()                                                                                          #converting data in json object
                D={}                                                                                                          #initialize dictionary             
##############         Collecting data from json object and putting it into a DataFrame
#############
############### For Dates
                D["date"]=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data['Weekly Adjusted Time Series']]
                D["symbol"]=[tick for DATE in data['Weekly Adjusted Time Series']]
                D["close"]=[ float(data['Weekly Adjusted Time Series'][DATE]['5. adjusted close']) for DATE in data['Weekly Adjusted Time Series']]
                D["volume"]=[ float(data['Weekly Adjusted Time Series'][DATE]['6. volume']) for DATE in data['Weekly Adjusted Time Series']]                           
################   Manipulating Subsequent DataFrames
            D=pd.DataFrame(D)                                                                                                #creating DataFrame and specifying the idex
            D.set_index("date",inplace=True)                                                                                 #setting Date column to be the index
            D.sort_index(ascending=True,inplace=True)                                                                        #sorting the index
            D=D[self.start:self.end]                                                                                         #refining to selection
            D=data_clean(D)                                                                                                  #cleans the dataframe
            stock_list=pd.concat([stock_list,D])                                                                             #joins the  DataFrames
###############   Reformatting Final DataFrame
        stock_list.reset_index(inplace=True)                                                                                 #resetting index to make new index
        stock_list.set_index(['symbol','date'],inplace=True)                                                                 #defining new index
        del D, data                                                                                                          #deleting variables
        return stock_list                                                                                                    #returning the DataFrame
    
    
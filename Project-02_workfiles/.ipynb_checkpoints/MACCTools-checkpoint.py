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

### Pulling the Dictionary From SQL
#db_url = "postgresql://postgres:postgres@localhost:5432/agent_db"
#mk = pd.read_sql(query, engine)

#Prelim Dictionary : Keeps track of items in API Request
mk={"Date" : "fiscalDateEnding", "Symbol": "symbol", "Net Income" : "netIncome",'Short Term Debt':'shortTermDebt',
   'Long Term Debt':'longTermDebt',"Total Liabilities":"totalLiabilities","Total Share Holder Equity":"totalShareholderEquity","Free Cash Flow":"changeInCashAndCashEquivalents","Reported EPS":"reportedEPS","Estimated EPS":"estimatedEPS"}



#"""-----------------           MACC TOOLS !!!!           ---------------"""
#"""  Listed below are the functions that we will use to make the code more condense and clean"""



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



# Data Cleaning (Receives the Data for Cleaning)
# def data_clean(df):
#"""Cleans data: removes null/NA values and converts data to required forms, if necessary"""
    #checks if there are any NAs in the data
    #Removes NA
    # converts data into correct types
    
    
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

class AccountScrub:
    """ This class is for pulling financial records for specfic companies for a specified time range
        
     Attributes
        ticker=contains ticker symbols of specified companies
        fin_stat_items=items extracted from financial statements
        balance_sheet_items=items extracted from balance sheet statements
        fin_ratios_items=items extracted from ratios statements
        cash_flow_items=items extracted from cash flow statements
    """
###############    Initializing the Function
###############
    def __init__(self, ticker=["AAPL"],start=(datetime.now()-timedelta(days=1095)).strftime("%Y-%m-%d"),end=datetime.now().strftime("%Y-%m-%d")):
        
        
###############     Checking for Errors
        if not isinstance(ticker,list):
            raise TypeError("ticker must be a list")
#Setting class attributes
        self.ticker=ticker
        self.fin_stat_items=["Date","Symbol","Net Income"]
        self.balance_sheet_items=["Date","Symbol","Debt To Equity"]
        self.fin_ratios_items=["Date","Symbol","Reported EPS","Estimated EPS"]
        self.cash_flow_items=["Date","Symbol","Free Cash Flow"]
        self.start=start
        self.end=end

        
        
        
        
        
        
        
        
############################.                                                  ##############################
#############################           FINANCIAL STATEMENT FUNCTION           ##############################
#############################.                                                 ##############################
    def fin_stat(self):
        """Description: This function is used to collect information from items typically found on the income statement"""
        tags=self.fin_stat_items                                                #calls specific items to be pulled from financial statements in API
        stock_list=pd.DataFrame()                                               #initialized DataFrame to hold company information
        #lim=4*(int(datetime.strptime(self.end,"%Y-%m-%d").year)-int(datetime.strptime(self.start,"%Y-%m-%d").year))
        for tick in self.ticker:
            #query=f"https://fmpcloud.io/api/v3/income-statement-as-reported/{tick}?period=quarter&limit={lim}&apikey={appkey}"
            query=f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={tick}&apikey={appkey}"
            response=requests.get(query)                                       #Making the API query
            data=response.json()                                               #converting data in json object
            #data=d['quarterlyReports']                                        #accessing quarterly reports for company
            D={}                                                               #initialize dictionary 
            
            
            
            
            
            
##############         Collecting data from json object and putting it into a DataFrame
#############
########################.       For Dates
            for tag in tags:
                if(tag=="Date"):
                    D[tag]=[datetime.strptime(item[mk[tag]],"%Y-%m-%d") for item in data['quarterlyReports']]
##########################        For Symbols
                elif(tag=="Symbol"):
                    #D[tag]=[item[mapkey(tag)] for item in data]
                    D[tag]=[tick for item in data['quarterlyReports']]
                else:
                     D[tag]=[ float(item[keyfind(item,mapkey(tag))] if (not item[keyfind(item,mapkey(tag))].isalpha())   else 'nan') for item in data['quarterlyReports']]
################   Manipulating Subsequent DataFrames
            D=pd.DataFrame(D)                                                  #creating DataFrame and specifying the idex
            D.set_index("Date",inplace=True)                                   #setting Date column to be the index
            D.sort_index(ascending=True,inplace=True)                          #sorting the index
            D=D[self.start:self.end]                                           #refining to selection
            #stock_list.append(D)                                              #adds stock information to stock list
            stock_list=pd.concat([stock_list,D])                               #joins the  DataFrames
###############   Reformatting Final DataFrame
        #stock_list.reset_index(inplace=True)
        #stock_list.set_index(keys=["Symbol","Date"],inplace=True)
        stock_list.reset_index(inplace=True)
        stock_list.set_index(['Symbol','Date'],inplace=True)
        del D, data
        return stock_list                                                      #returning the DataFrame
            
        
        
        
        
        
        
        
        
#############################                                               ##############################     
#############################           BALANCE SHEET FUNCTION              ##############################  
#############################                                               ################################

    def balance_sheet(self):
        """Description: This function is used to collect information from items typically found on the balance sheet"""
        tags=self.balance_sheet_items                                       #calls specific items to be pulled from financial statements in API
        stock_list=pd.DataFrame()                                           #initialized DataFrame to hold company information
        for tick in self.ticker:
            #Defining API Query
            query=f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={tick}&apikey={appkey}"
        
            response=requests.get(query)                                    #Making the API query
            data=response.json()                                            #converting data in json object
            D={}                                                            #initialize dictionary 
            
##############         Collecting data from json object and putting it into a DataFrame
#############
            for tag in tags:
                if(tag=="Date"):                                            #special format for dates
                    D[tag]=[datetime.strptime(item[mk[tag]],"%Y-%m-%d") for item in data['quarterlyReports']]
###############  For Symbols
                elif(tag=="Symbol"):                                        #special format for symbols
                    D[tag]=[tick for item in data['quarterlyReports']]
                elif(tag=="Debt To Equity"):                                #conversion from string to float
                     D[tag]=[ float(float(item[keyfind(item,mapkey("Total Liabilities"))])/float(item[keyfind(item,mapkey("Total Shareholder Equity"))]) if 
                                    ( (not item[keyfind(item,mapkey("Total Liabilities"))].isalpha()) and ( not item[keyfind(item,mapkey("Total Shareholder Equity"))].isalpha() ) and float(item[keyfind(item,mapkey("Total Shareholder Equity"))])!=0 ) else 'nan') 
                             for item in data['quarterlyReports']]
                else:
                    D[tag]=[ float(item[keyfind(item,mapkey(tag))] if (not item[keyfind(item,mapkey(tag))].isalpha()) else 'nan') for item in data['quarterlyReports']]
################   Manipulating Subsequent DataFrames
            D=pd.DataFrame(D)                                               #creating DataFrame and specifying the idex
            D.set_index("Date",inplace=True)                                #setting Date column to be the index
            D.sort_index(ascending=True,inplace=True)                       #sorting the index
            D=D[self.start:self.end]                                        #refining to selection
            D=data_clean(D)                                                 #cleans the dataframe
            #stock_list.append(D)                                           #adds stock information to stock list
            stock_list=pd.concat([stock_list,D])                            #joins the  DataFrames
###############   Reformatting Final DataFrame
        stock_list.reset_index(inplace=True)
        stock_list.set_index(['Symbol','Date'],inplace=True)
        del D, data
        return stock_list                                                   #returning the DataFrame        
        

        

        
        
        
        
#############################                                               ##############################     
#############################           CASH FLOW STATEMENT FUNCTION        ############################## 
#############################                                               ################################

    def cf_stat(self):
        """Description: This function is used to collect information from items typically found on the cash flow statement"""
        tags=self.cash_flow_items                                          #items to be pulled from financial statements in API
        stock_list=pd.DataFrame()                                          #initialized DataFrame to hold company information
        for tick in self.ticker:
###################   Initializing try instance
#############
########
####
            try: ########***************
            #Defining API Query
                query=f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={tick}&apikey={appkey}"
                response=requests.get(query)                                   #Making the API query
                data=response.json()                                           #converting data in json object
                D={}                                                           #initialize dictionary             
##############         Collecting data from json object and putting it into a DataFrame
#############
############### For Dates
                for tag in tags:
                    if(tag=="Date"):                                           #special format for collecting the date
                        D[tag]=[datetime.strptime(item[mk[tag]],"%Y-%m-%d") for item in data['quarterlyReports']]
###############  For Symbols
                    elif(tag=="Symbol"):                                       #special format for collecting symbol for company
                        D[tag]=[tick for item in data['quarterlyReports']]
                    else:                                                      #converting figures to floats
                        D[tag]=[ float(item[mk[tag]] if (not item[mk[tag]].isalpha())  else 'nan') 
                            for item in data['quarterlyReports']]
                        
#####                        
#########                       
#############                        
################# Specifying the error type                                    
            except KeyError:
                print('KeyError. Trying again in 60 seconds...')
                time.sleep(60)                                                 #sleep time 60s

            #Defining API Query
                query=f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={tick}&apikey={appkey}"
                response=requests.get(query)                                   #Making the API query
                data=response.json()                                           #converting data in json object
                D={}                                                           #initialize dictionary             
##############         Collecting data from json object and putting it into a DataFrame
#############
############### For Dates
                for tag in tags:
                    if(tag=="Date"):                                           #special format for collecting the date
                        D[tag]=[datetime.strptime(item[mk[tag]],"%Y-%m-%d") for item in data['quarterlyReports']]
###############  For Symbols
                    elif(tag=="Symbol"):                                       #special format for collecting symbol for company
                        D[tag]=[tick for item in data['quarterlyReports']]
                    else:                                                      #converting figures to floats
                        D[tag]=[ float(item[mk[tag]] if (not item[mk[tag]].isalpha())  else 'nan') 
                            for item in data['quarterlyReports']]
                        
            
                                   
################   Manipulating Subsequent DataFrames
            D=pd.DataFrame(D)                                              #creating DataFrame and specifying the idex
            D.set_index("Date",inplace=True)                               #setting Date column to be the index
            D.sort_index(ascending=True,inplace=True)                      #sorting the index
            D=D[self.start:self.end]                                       #refining to selection
            D=data_clean(D)                                                #cleans the dataframe
            stock_list=pd.concat([stock_list,D])                           #joins the  DataFrames
                  
            
###############   Reformatting Final DataFrame
        stock_list.reset_index(inplace=True)                               #resetting index to make new index
        stock_list.set_index(['Symbol','Date'],inplace=True)               #defining new index
        del D, data                                                        #deleting variables
        return stock_list                                                  #returning the DataFrame  
    
            
    
    

    
    

    
    
    
    
    
   









    
    
        
#############################                                               ##############################     
#############################           CLOSING PRICES AND VOLUME           ############################## 
#############################                                               ################################

    def cf_stat(self):
        """Description: This function is used to collect information from stocks on closing prices and volume"""
        tags=self.stock_data                                          #items to be pulled from financial statements in API
        stock_list=pd.DataFrame()                                          #initialized DataFrame to hold company information
        for tick in self.ticker:
###################   Initializing try instance
#############
########
####
            try: ########***************
            #Defining API Query
                #query=f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={tick}&apikey={appkey}"
                query f"https://www.alphavantage.co/query?"                                                                   #base query
                response=requests.get(query,params={'function':'TIME_SERIES_MONTHLY_ADJUSTED','symbol':tick,'apikey':appkey}) #Making request with parameters
                data=response.json()                                                                                          #converting data in json object
                D={}                                                                                                          #initialize dictionary             
##############         Collecting data from json object and putting it into a DataFrame
#############
############### Use of List Comprehensions to Collect Necessary Data
                for DATE in data['Weekly Adjusted Time Series']:
                    D["Date"]=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data['Weekly Adjusted Time Series']]
                    D["Adj Close"]=[(stock['5. adjusted close'] for stock in DATE) for DATE in data['Weekly Adjusted Time Series']]
                    D["Adj Close"]=[(stock['6. volume'] for stock in DATE) for DATE in data['Weekly Adjusted Time Series']]                       
#####                        
#########                       
#############                        
################# Specifying the error type                                    
            except KeyError:
                print('KeyError. Trying again in 60 seconds...')
                time.sleep(60)                                                                                                #sleep time 60s
            #Defining API Query
                query f"https://www.alphavantage.co/query?"                                                                   #base query
                response=requests.get(query,params={'function':'TIME_SERIES_MONTHLY_ADJUSTED','symbol':tick,'apikey':appkey}) #Making request with parameters
                data=response.json()                                                                                          #converting data in json object
                D={}                                                                                                          #initialize dictionary             
##############         Collecting data from json object and putting it into a DataFrame
#############
############### For Dates
                for DATE in data['Weekly Adjusted Time Series']:
                    D["Date"]=[datetime.strptime(DATE,"%Y-%m-%d") for DATE in data['Weekly Adjusted Time Series']]
                    D["Adj Close"]=[(stock['5. adjusted close'] for stock in DATE) for DATE in data['Weekly Adjusted Time Series']]
                    D["Adj Close"]=[(stock['6. volume'] for stock in DATE) for DATE in data['Weekly Adjusted Time Series']]
                        
            
                                   
################   Manipulating Subsequent DataFrames
            D=pd.DataFrame(D)                                              #creating DataFrame and specifying the idex
            D.set_index("Date",inplace=True)                               #setting Date column to be the index
            D.sort_index(ascending=True,inplace=True)                      #sorting the index
            D=D[self.start:self.end]                                       #refining to selection
            D=data_clean(D)                                                #cleans the dataframe
            stock_list=pd.concat([stock_list,D])                           #joins the  DataFrames
                  
            
###############   Reformatting Final DataFrame
        stock_list.reset_index(inplace=True)                               #resetting index to make new index
        stock_list.set_index(['Symbol','Date'],inplace=True)               #defining new index
        del D, data                                                        #deleting variables
        return stock_list                                                  #returning the DataFrame  
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    
    

############################.                                                  ##############################
#############################           FINANCIAL RATIOS  FUNCTION              ##############################
#############################.                                                   ############################
    def fin_ratios(self):
        """Description: This function is used to collect figures on ratios found in financial statements"""
        tags=self.fin_ratios_items                                        #calls specific items to be pulled from financial statements in API
        stock_list=pd.DataFrame()                                         #initialized DataFrame to hold company information
        for tick in self.ticker:
            #Defining API Query
            query=f"https://www.alphavantage.co/query?function=EARNINGS&symbol={tick}&apikey={appkey}"
            response=requests.get(query)                                  #Making the API query
            data=response.json()                                          #converting data in json object                 
            D={}                                                          #initialize dictionary 
            
##############         Collecting data from json object and putting it into a DataFrame
            for tag in tags:
                if(tag=="Date"):                                          #special formatting to get date
                    D[tag]=[datetime.strptime(item[mk[tag]],"%Y-%m-%d") for item in data['quarterlyEarnings']]
##########################
                elif(tag=="Symbol"):                                      #special formatting for symbol
                    D[tag]=[tick for item in data['quarterlyEarnings']]
                else:                                                     #conversion of figures to floats
                    D[tag]=[ float(item[keyfind(item,mapkey(tag))] if (not item[keyfind(item,mapkey(tag))].isalpha()) else 'nan') for item in data['quarterlyEarnings']]
################   Manipulating Subsequent DataFrames
            D=pd.DataFrame(D)                                             #creating DataFrame and specifying the idex
            D.set_index("Date",inplace=True)                              #setting Date column to be the index
            D.sort_index(ascending=True,inplace=True)                     #sorting the index
            D=D[self.start:self.end]                                      #refining to selection
            stock_list=pd.concat([stock_list,D])                          #joins the  DataFrames
###############   Reformatting Final DataFrame
        #stock_list.reset_index(inplace=True)
        #stock_list.set_index(keys=["Symbol","Date"],inplace=True)
        stock_list.reset_index(inplace=True)
        stock_list.set_index(['Symbol','Date'],inplace=True)
        del D, data
        return stock_list                                                 #returning the DataFrame
                    
        
        
        
        
    
#############################                                               ##############################     
#############################           CASH FLOW STATEMENT FUNCTION            ############################## 
#############################                                               ################################

    def acc_summary(self):
        """Description: Gives an overview of the important financial measures from several financial statements. Would only work when premium access is purchased, allowing a trader to make more than 5 calls per 5 min"""
        fin_stat_df=self.fin_stat()                                      #gets fin_stat DataFrame
        time.sleep(1)
        balance_sheet_df=self.balance_sheet()                            #gets balance sheet DataFrame
        time.sleep(1)
        cf_stat_df=self.cf_stat()                                        #gets cash flow DataFrame
    
        #Change Index Columns to Date Column
        fin_stat_df.reset_index(inplace=True)    
        fin_stat_df.set_index("Date",inplace=True)
        
        
        balance_sheet_df.reset_index(inplace=True)
        balance_sheet_df.set_index("Date",inplace=True)
        
        cf_stat_df.reset_index(inplace=True)
        cf_stat_df.set_index("Date",inplace=True)
        
        #Combining the DataFrames
        combined_df=pd.concat([fin_stat_df,balance_sheet_df,cf_stat_df],axis="columns", join='inner') #performs inner join
        
        combined_df=combined_df.dropna()                                  #drops all rows containing na
        combined_df.set_index(['Symbol','Date'],inplace=True)             #resets index
        return combined_df                                                #returns combined df
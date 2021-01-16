"""
Program to provide generic parsing for all files in user-specified directory.
The program assumes the input files have been scrubbed,
  i.e., HTML, ASCII-encoded binary, and any other embedded document structures that are not
  intended to be analyzed have been deleted from the file.

Dependencies:
    Python:  Load_MasterDictionary.py
    Data:    LoughranMcDonald_MasterDictionary_XXXX.csv

The program outputs:
 X  1.  File name
 X  2.  File size (in bytes)
   3.  Number of words (based on LM_MasterDictionary 
   4.  Proportion of positive words (use with care - see LM, JAR 2016)
   5.  Proportion of negative words
   6.  Proportion of uncertainty words
   7.  Proportion of litigious words
   8.  Proportion of modal-weak words
   9.  Proportion of modal-moderate words
  10.  Proportion of modal-strong words
  11.  Proportion of constraining words (see Bodnaruk, Loughran and McDonald, JFQA 2015)
 X 12.  Number of alphanumeric characters (a-z, A-Z)
 X 13.  Number of digits (0-9)
 X 14.  Number of numbers (collections of digits)
 X 15.  Average number of syllables
  16.  Average word length
  17.  Vocabulary (see Loughran-McDonald, JF, 2015)

  ND-SRAF
  McDonald 2016/06 : updated 2018/03
"""

import csv
import re
import string
import time
import Load_MasterDictionary as LM                                                             # Loading the master dictionary file
import pandas as pd

MASTER_DICTIONARY_FILE = f'LoughranMcDonald_MasterDictionary_2018.csv'                         # User defined file pointer to LM dictionary

# Setup output:
OUTPUT_FIELDS = ['date', 'number of words', '% positive', '% negative',                        # columns for DataFrame of sentiment scores (12 total)
                '% uncertainty', '% litigious', '% modal-weak','% modal moderate',
                '% modal strong', '% constraining',
                'average word length', 'vocabulary']

lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, True)                         # load master dictionary into dictionary object
#print(lm_dictionary._stopwords())


def LM_sentiment(news_df):#be sure to set tick as an argument after testing
    """Takes in DataFrame and specified ticker to use LM dictionary to compute proportion of words representing differen types of sentiment"""
    OUTPUT_FILE = f'Sentiment_Data/test_file.csv'                                              # User defined output file to write data to
    L=[]
    #D.append(OUTPUT_FIELDS)
    
    for i in range(len(news_df)):                                                              # Uses date in DataFrame as indexing loop
        #print("Sources for this day are: "+news_df.loc[DATE]['Media'])                        # getting the news sources (Find better way of Collecting financial news)
        articles=news_df.iloc[i]['Article']                                                    # get articles from specified date
        articles= re.sub('(May|MAY)', ' ', articles)                                           # drop all May month references; avoid conflicting with "may" a modal word
        articles=articles.upper()                                                              # make everything uppercase
        output_data=get_data(articles)                                                         # returning sentiment scores from function as a list       
        output_data[0]=news_df.iloc[i].name                                                    # storing the date of articles as first entry of list 
        L.append(output_data)                                                                  # appending article info to list
    L=pd.DataFrame(L,columns=OUTPUT_FIELDS)                                                     # constructing DataFrame from article data
    L.set_index('date',inplace=True)                                                           # setting the index in place
    return L                                                                                   # returning the DataFrame
#####################################################################################################################################################################   
####################################################################################################################################################################### 
#Modified code
def get_data(articles):                                                                          # Here, the articles will be very long strings
    """Takes articles from specific data and computes sentiment scores using LM Dictionary"""
    vdictionary = {}                                                                             # dictionary for tokens that are found in dictionary
    _odata = [0] * 12                                                                            # list collecting everything except date; last number of words=index:0
    word_length = 0                                                                              # initializing the value of word length; will be updated via loop
    tokens = re.findall('\w+', articles)                                                         # Note that \w+ splits hyphenated words
    for token in tokens:                                                                         # Goes through generated tokens from articles
        if (not token.isdigit()) and (len(token) > 1) and (token in lm_dictionary.keys()):       # conditions for checking if token is in dictionary
            _odata[1] += 1                                                                       # updating word count 
            word_length += len(token)                                                            # updating word length
            if token not in vdictionary:                                                         # initial statement regarding steps for handling tokens not in the dictionary
                vdictionary[token] = 1                                                           # count of tokens in text that show up in dictionary
                
####### Keeping Track of Categorical Token Counts (Nonzero entry=True) also checks if word is stop word
            if lm_dictionary[token].positive and not lm_dictionary[token].stopword: _odata[2] += 1
            if lm_dictionary[token].negative and not lm_dictionary[token].stopword: _odata[3] += 1
            if lm_dictionary[token].uncertainty and not lm_dictionary[token].stopword: _odata[4] += 1
            if lm_dictionary[token].litigious and not lm_dictionary[token].stopword: _odata[5] += 1
            if lm_dictionary[token].weak_modal and not lm_dictionary[token].stopword: _odata[6] += 1
            if lm_dictionary[token].moderate_modal and not lm_dictionary[token].stopword: _odata[7] += 1
            if lm_dictionary[token].strong_modal and not lm_dictionary[token].stopword: _odata[8] += 1
            if lm_dictionary[token].constraining and not lm_dictionary[token].stopword: _odata[9] += 1
            #total_syllables += lm_dictionary[token].syllables                                   # interesting parameter to measure

    #_odata[12] = len(re.findall('[0-9]', doc))
    # drop punctuation within numbers for number count
    articles = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', articles)
    articles = articles.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    #_odata[13] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc))
   # _odata[14] = total_syllables / _odata[2]
    #print(_odata[1])
    _odata[10] = word_length / _odata[1]                                                        # computing average word length
    _odata[11] = len(vdictionary)                                                               # total vocab count
    
    # Convert counts to %
    for i in range(2, 9 + 1):                                                                   # specifying range of percentages
        try:
            _odata[i] = (_odata[i] / _odata[1]) * 100                                           # updating count to percent
        except:
            print("zero denominator")
    # Vocabulary
        
    return _odata                                                                               # returning the data
 


    

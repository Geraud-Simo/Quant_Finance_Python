#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from matplotlib import style
import yfinance as yf
import plotly.express as px


# In[2]:


style.use('ggplot')


# In[3]:


tickers = ['AAPL','AMZN', 'BABA','NVDA']
start = dt.datetime(2020,1,1)
end = dt.datetime.now()


# In[5]:


for ticker in tickers:
    data = yf.download(ticker, start, end)
    data = data.drop(columns = ['High', 'Low', 'Open', 'Close'] )
    
    data['SMA20'] = data['Adj Close'].rolling(20).mean()
    data['SMA120'] = data['Adj Close'].rolling(120).mean()

    data['EWM12'] = data['Adj Close'].ewm(span = 12, adjust = False).mean()
    data['EWM26'] = data['Adj Close'].ewm(span = 26, adjust = False).mean()


    data['Price_yesterday'] = data['Adj Close'].shift(1)
    data['Price_change'] = data['Adj Close'] / data['Price_yesterday']
    
    data['SMA_strategy'] = [ 1 if data.loc[i, 'SMA20'] > data.loc[i, 'SMA120']
                           else 0 for i in data.index]
    data['EWM_strategy'] = [ 1 if data.loc[i, 'EWM12'] > data.loc[i, 'EWM26']
                           else 0 for i in data.index]


    data['Buy_and_hold'] = np.cumprod(data['Price_change'])

    sma = data[data['SMA_strategy'] == 1]
    sma['Return'] = np.cumprod(sma['Price_change'])

    ewm = data[data['EWM_strategy'] == 1]
    ewm['Return'] = np.cumprod(ewm['Price_change'])

    print(ticker)
    print ('Buy and hold strategy return:' + str(data['Buy_and_hold'][-1]))
    print('SMA return:' + str(sma['Return'][-1]))
    print('EWM return:' + str(ewm['Return'][-1]))


# In[8]:


for ticker in tickers:

    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1, title = ticker)
    ##ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 2, colspan = 1, sharex = ax1)
    ax3 = plt.subplot2grid((10,1), (8,0), rowspan = 2, colspan = 1, sharex = ax1)

    ax1.plot(data['Adj Close'], label = 'Price')
    ax1.plot(data['SMA20'], label = 'SMA20')
    ax1.plot(data['SMA120'], label = 'SMA120')
    ax1.plot(data['EWM12'], label = 'EWM12')
    ax1.plot(data['EWM26'], label = 'EWM26')


    ##ax2.bar(data.index, data['Volume'], label = 'Volume')

    ax3.plot(data['Buy_and_hold'], label = 'Buy_and_hold')
    ax3.plot(sma['Return'], label = 'SMA Return')
    ax3.plot(ewm['Return'], label = 'EWM Return')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax3.set_xlabel('Date (Year-Month)')
    ax1.legend()
    ##ax2.legend()
    ax3.legend()
    plt.show()


# In[ ]:





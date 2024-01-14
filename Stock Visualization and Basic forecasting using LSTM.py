#!/usr/bin/env python
# coding: utf-8

# In[72]:


import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from matplotlib import style
import yfinance as yf
import plotly.express as px


# In[73]:


style.use('ggplot')


# In[74]:


tickers = ['AAPL','AMZN', 'BABA','NVDA']
start = dt.datetime(2020,1,1)
end = dt.datetime.now()


# In[75]:


##data = pd.read_csv ('CLS.JO.csv', parse_dates = True, index_col='Date')


# In[76]:


for ticker in tickers:
    data = yf.download(ticker, start, end)


# In[66]:


data.head()


# In[ ]:


# ax1 = plt.subplot2grid((9,1), (0,0), rowspan = 5, colspan = 1, title = ticker)
ax2 = plt.subplot2grid((9,1), (6,0), rowspan = 4, colspan = 1, sharex = ax1)

ax1.plot(data['Adj Close'], label = 'Price')
ax2.bar(data.index, data['Volume'], label = 'Volume')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))

ax2.set_xlabel('Date (Year-Month)')
ax1.legend()
ax2.legend()


# In[39]:


## Let us add some moving averages to gauge momentum shifts across the year


# In[77]:


data['SMA20'] = data['Adj Close'].rolling(20).mean()
data['SMA120'] = data['Adj Close'].rolling(120).mean()

data['EWM12'] = data['Adj Close'].ewm(span = 12, adjust = False).mean()
data['EWM26'] = data['Adj Close'].ewm(span = 26, adjust = False).mean()


data['Price_yesterday'] = data['Adj Close'].shift(1)
data['Price_change'] = data['Adj Close'] / data['Price_yesterday']
data['Percent_change'] = data['Price_change'] - 1
data = data.drop(columns = ['High', 'Low', 'Open','Close'])
data.head()


# In[41]:


## What happens if we buy ONLY when SMA20 > SMA120 and hold or do nothing otherwise ?
## Let's create a database that capturres everytime we make such trades and let us see what our potential returns could be.


# In[78]:


data['SMA_strategy'] = [ 1 if data.loc[i, 'SMA20'] > data.loc[i, 'SMA120']
                           else 0 for i in data.index]
data['EWM_strategy'] = [ 1 if data.loc[i, 'EWM12'] > data.loc[i, 'EWM26']
                           else 0 for i in data.index]


data['Buy_and_hold'] = np.cumprod(data['Price_change'])

sma = data[data['SMA_strategy'] == 1]
sma['Return'] = np.cumprod(sma['Price_change'])

ewm = data[data['EWM_strategy'] == 1]
ewm['Return'] = np.cumprod(ewm['Price_change'])


# In[ ]:





# In[ ]:


##ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1, title = ticker)
ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 2, colspan = 1, sharex = ax1)
ax3 = plt.subplot2grid((10,1), (8,0), rowspan = 2, colspan = 1, sharex = ax1)

ax1.plot(data['Adj Close'], label = 'Price')
ax1.plot(data['SMA20'], label = 'SMA20')
ax1.plot(data['SMA120'], label = 'SMA120')
ax1.plot(data['EWM12'], label = 'EWM12')
ax1.plot(data['EWM26'], label = 'EWM26')


ax2.bar(data.index, data['Volume'], label = 'Volume')

ax3.plot(data['Buy_and_hold'], label = 'Buy_and_hold')
ax3.plot(sma['Return'], label = 'Return')
ax3.plot(ewm['Return'], label = 'Return')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

ax3.set_xlabel('Date (Year-Month)')
ax1.legend()
ax2.legend()
plt.show()


# In[79]:


for ticker in tickers:
    
    data['SMA20'] = data['Adj Close'].rolling(20).mean()
    data['SMA120'] = data['Adj Close'].rolling(120).mean()

    data['EWM12'] = data['Adj Close'].ewm(span = 12, adjust = False).mean()
    data['EWM26'] = data['Adj Close'].ewm(span = 26, adjust = False).mean()
    
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


# In[ ]:


##How does the SMA approach compare to the EWM ?


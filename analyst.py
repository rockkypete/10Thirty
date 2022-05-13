import requests
import pandas as pd
from pandas import json_normalize
import sqlite3
import matplotlib.pyplot as plt


# declaring indicator 
# simple moving average
def SMA(data, ndays):
  SMA=pd.Series(pd.rolling_mean(data['Close'], ndays), name='SMA')
  data=data.join(SMA)
  return data

# commodity channel index
def CCI(data, ndays): 
  TP = (data['High'] + data['Low'] + data['Close']) / 3 
  CCI = pd.Series((TP - pd.rolling_mean(TP, ndays)) / (0.015*pd.rolling_std(TP, ndays)),
  name = 'CCI') 
  data = data.join(CCI) 
  return data

def ForceIndex(data, ndays):
  ForceIndex=pd.Series(data['Close'].diff(ndays)* data['Volume'], name='ForceIndex')
  data=data.join(ForceIndex)
  return data





# defining the analyst object
class Analyst:
  def __init__(self,credentials, indicators ):
    self.credentials = credentials
    self.indicators = indicators

  
  #method to get market data from exchange provider
  def fetchdata(self):
    url = "https://alpha-vantage.p.rapidapi.com/query"
    querystring = {"market":"USD","symbol":"BTC","function":"DIGITAL_CURRENCY_DAILY"}

    headers = {
      "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com",
      "X-RapidAPI-Key": self.credentials
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    marketData = response.json()['Time Series (Digital Currency Daily)']

    timestamps = list(marketData.keys())
    asset_price = list(marketData.values())

    #define DF structure and populate data
    pricesDict = {
      'date':[],
      'open': [],
      'high':  [],
      'low': [],
      'close': [],
      'volume': [],
      'marketCap': []
    } 

    for data in asset_price:
      pricesDict['date'].append(timestamps[asset_price.index(data)])
      pricesDict['open'].append(data['1a. open (USD)'])
      pricesDict['high'].append(data['2a. high (USD)'])
      pricesDict['low'].append(data['3a. low (USD)'])
      pricesDict['close'].append(data['4a. close (USD)'])
      pricesDict['volume'].append(data['5. volume'])
      pricesDict['marketCap'].append(data['6. market cap (USD)'])

    price_DataFrame = pd.DataFrame(pricesDict)

    #export dataFrame to csv file
    price_DataFrame.to_csv('crypto.csv', sep='-')
  


  #method to compute moving average
  def compute_MovingAverage(self, period):
    #read data from csv file
    data = pd.read_csv('crypto.csv')
    SMG=SMA(data, period)
    self.indicators[f'{period}SMA'] = SMG['SMA']
    SMG.to_csv('crypto.csv')

  #method to compute commodity channel index
  def compute_CCI(self, period):
    data = pd.read_csv('crypto.csv')
    cci_DF = CCI(data, period)
    self.indicators['CCI'] = cci_DF['CCI']
    cci_DF.to_csv('crypto.csv')

  #method to compute market pressure
  def compute_MarketPressure(self, period):
    data = pd.read_csv('crypto.csv')
    fi_DF = ForceIndex(data, period)
    self.indicators['ForceIndex'] = fi_DF['ForceIndex']
    fi_DF.to_csv('crypto.csv')


  #method to compute fibonacci retracement levels
  def compute_FibonacciLevels(self):
    pass
  #chart plotting method
  def plotChart(self):
    pass


    


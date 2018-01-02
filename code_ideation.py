# -*- coding: utf-8 -*-
# @Author: loopingleo | rubin777
# @Date:   2018-01-02
# @Last Modified by:   loopingleo
# @Last Modified time:

import pandas as pd

from intriniorealtime.client import IntrinioRealtimeClient
import os
import intrinio
import matplotlib.pyplot as plt

intrinio.client.username = ''
intrinio.client.password = ''

'''
def on_quote(quote, backlog):
    print("QUOTE: ", quote, "BACKLOG LENGTH: ", backlog)


options = {
    'username': '',
    'password': '',
    'provider': 'iex',
    'on_quote': on_quote
}

client = IntrinioRealtimeClient(options)
client.join(['AAPL', 'GE', 'MSFT'])
client.connect()
client.keep_alive()

'''



data_stock_prices = intrinio.prices('ATVI')#, start_date='2000-01-01')
data_financials = intrinio.financials('AAPL')

intrinio.companies('GOOG')



data_stock_prices.info()


atvi_adjclose = pd.Series(data_stock_prices.adj_close)
atvi_adjclose_norm = atvi_adjclose/atvi_adjclose[len(atvi_adjclose)-1]*100
atvi_adjclose_norm = atvi_adjclose_norm.rename("ATVI")


data_stock_prices = intrinio.prices('SPY', start_date='1993-10-25')
spy_adjclose = pd.Series(data_stock_prices.adj_close)
spy_adjclose_norm = spy_adjclose/spy_adjclose[len(spy_adjclose)-1]*100
spy_adjclose_norm = spy_adjclose_norm.rename("SPY")

value = pd.Series()
value["rollcorell"] = pd.rolling_corr(spy_adjclose_norm, atvi_adjclose_norm, 5)

plt.figure()
plt.plot(atvi_adjclose_norm)
plt.plot(spy_adjclose_norm)
plt.legend()

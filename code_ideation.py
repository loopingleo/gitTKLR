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
import matplotlib.gridspec as gridspec

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


spy_prices = intrinio.prices('SPY', start_date='1993-10-25')
spy_adjclose = pd.Series(spy_prices.adj_close)
spy_adjclose_norm = spy_adjclose/spy_adjclose[len(spy_adjclose)-1]*100
spy_adjclose_norm = spy_adjclose_norm.rename("SPY")

EA_prices = intrinio.prices('EA', start_date='1993-10-25')
ea_adjclose = pd.Series(EA_prices.adj_close)
ea_adjclose_norm = ea_adjclose/ea_adjclose[len(ea_adjclose)-1]*100
ea_adjclose_norm = ea_adjclose_norm.rename("EA")


sne_prices = intrinio.prices('SNE')
ea_adjclose = pd.Series(EA_prices.adj_close)
ea_adjclose_norm = ea_adjclose/ea_adjclose[len(ea_adjclose)-1]*100
ea_adjclose_norm = ea_adjclose_norm.rename("EA")

ea_adjclose_norm_11y = ea_adjclose[:"2007-01-03"]/ea_adjclose["2007-01-03"][0]*100
spy_adjclose_norm_11y = spy_adjclose[:"2007-01-03"]/spy_adjclose["2007-01-03"][0]*100
atvi_adjclose_norm_11y = atvi_adjclose[:"2007-01-03"]/atvi_adjclose["2007-01-03"][0]*100



ATVI_SPY_60corr = pd.rolling_corr(atvi_adjclose_norm, spy_adjclose_norm, 60)
ATVI_SPY_60corr.describe()

ATVI_SPY_15corr = pd.rolling_corr(atvi_adjclose_norm, spy_adjclose_norm, 15)
ATVI_SPY_15corr.describe()

ATVI_EA_15corr = pd.rolling_corr(atvi_adjclose_norm, ea_adjclose_norm, 15)
ATVI_EA_15corr.describe()


ATVI_EA_mtl_corr = pd.rolling_corr(atvi_adjclose_norm.resample("M").mean(),
                                   ea_adjclose_norm.resample("M").mean(), 3)
ATVI_EA_mtl_corr.describe()


ATVI_SPY_mtl_corr = pd.rolling_corr(atvi_adjclose_norm.resample("M").mean(),
                                   spy_adjclose_norm.resample("M").mean(), 6)
ATVI_SPY_mtl_corr.describe()



ATVI_EA_11y_mtl_corr = pd.rolling_corr(atvi_adjclose_norm_11y.resample("W").mean(),
                                   ea_adjclose_norm_11y.resample("W").mean(), 15)
ATVI_EA_11y_mtl_corr.describe()


ATVI_SPY_11y_mtl_corr = pd.rolling_corr(atvi_adjclose_norm_11y.resample("W").mean(),
                                   spy_adjclose_norm_11y.resample("W").mean(), 40)
ATVI_SPY_11y_mtl_corr.describe()



plt.figure()
plt.plot(atvi_adjclose_norm)
plt.plot(spy_adjclose_norm)
plt.plot(ea_adjclose_norm)
#plt.plot(ATVI_SPY_15corr)
plt.legend()



#plot von 1993

fig = plt.figure()
gs = gridspec.GridSpec(3, 1)# width_ratios=[3])
ax1 = plt.subplot2grid((3,1), (0,0), rowspan=2)
ax2 = plt.subplot2grid((3,1), (2,0), sharex=ax1)

spy_adjclose_norm.resample("W").mean().plot(ax=ax1, label="S&P500")
atvi_adjclose_norm.resample("W").mean().plot(ax=ax1, label="ATVI")
ea_adjclose_norm.resample("W").mean().plot(ax=ax1, label="EA")


ATVI_EA_mtl_corr.plot(ax=ax2, label="ATVI to EA 4 week correlation")
ATVI_SPY_mtl_corr.plot(ax=ax2, label="ATVI to S&P500 12 week correlation")

ax1.legend(loc=1)
ax2.legend()

plt.show()




#plot nur 11 jahre

fig = plt.figure()
gs = gridspec.GridSpec(3, 1)# width_ratios=[3])
ax1 = plt.subplot2grid((3,1), (0,0), rowspan=2)
ax2 = plt.subplot2grid((3,1), (2,0), sharex=ax1)

spy_adjclose_norm_11y.resample("W").mean().plot(ax=ax1, label="S&P500")
atvi_adjclose_norm_11y.resample("W").mean().plot(ax=ax1, label="ATVI")
ea_adjclose_norm_11y.resample("W").mean().plot(ax=ax1, label="EA")


ATVI_EA_11y_mtl_corr.plot(ax=ax2, label="ATVI to EA 12 week correlation")
ATVI_SPY_11y_mtl_corr.plot(ax=ax2, label="ATVI to S&P500 26 week correlation")

ax1.legend(loc=1)
ax2.legend()

plt.show()




#datahub data
import datapackage

data_url = "http://datahub.io/core/s-and-p-500/datapackage.json"

# to load Data Package into storage
storage = datapackage.push_datapackage(data_url, 'pandas')

# data frames available (corresponding to data files in original dataset)
storage.buckets

# you can access datasets inside storage, e.g. the first one:
storage[storage.buckets[1]]

spdata = pd.DataFrame(storage[storage.buckets[0]][["SP500","PE10"]])
spdata.index =(storage[storage.buckets[0]]["Date"])

plt.plot(spdata)
plt.plot(spdata.PE10)


#plt.close()
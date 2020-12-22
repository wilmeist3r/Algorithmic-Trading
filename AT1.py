import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
import numpy as np
import sys


def view():
    pd.set_option('max_colwidth', 1000)
    pd.set_option('display.width', 1000)

# Gets data from a symbol given a symbol name, a cahnnel, and a start/end date
def getSymbol(symbol, channel, startDate, endDate):
    symbol_data = data.DataReader(symbol, channel, startDate, endDate)
    symbol_data_signal = pd.DataFrame(index = symbol_data.index)
    symbol_data_signal['price'] = symbol_data['Adj Close']
    symbol_data_signal['daily_difference'] = symbol_data_signal['price'].diff()
    symbol_data_signal['signal'] = 0.0
    symbol_data_signal['signal'] = np.where(symbol_data_signal['daily_difference'] >= 0, 1.0, 0.0)
    symbol_data_signal['positions'] = symbol_data_signal['signal'].diff()

    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel = 'Symbol price in USD')
    symbol_data_signal['price'].plot(ax = ax1, color = 'r', lw = 2.)
    ax1.plot(symbol_data_signal.loc[symbol_data_signal.positions == 1.0].index,
           symbol_data_signal.price[symbol_data_signal.positions == 1.0],
           '^', markersize = 5, color = 'm')
    ax1.plot(symbol_data_signal.loc[symbol_data_signal.positions == -1.0].index,
           symbol_data_signal.price[symbol_data_signal.positions == -1.0],
           'v', markersize = 5, color = 'k')

    print(symbol_data)
    print(symbol_data_signal.head())
    plt.show()


print("Please enter a symbol, a channel, and a start and end date (YY-MM-DD) below: ")
view()
getSymbol(symbol = input(), channel = input(), startDate = input(), endDate = input())

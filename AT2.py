import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt


def get_data(symbol, channel, start_date, end_date):
    print('Downloading data for symbol...')
    symbol_data = data.DataReader(symbol, channel, start_date, end_date)

    symbol_data_signal = pd.DataFrame(index = symbol_data.index)
    symbol_data_signal['price'] = symbol_data['Adj Close']

    print(symbol_data)
    print(symbol_data_signal.head())
    trading_support_resistance(symbol_data_signal)
    visualize_data(symbol_data_signal)


def trading_support_resistance(data, bin_width = 20):
    data['sup_tolerance'] = pd.Series(np.zeros(len(data)))
    data['res_tolerance'] = pd.Series(np.zeros(len(data)))
    data['sup_count'] = pd.Series(np.zeros(len(data)))
    data['res_count'] = pd.Series(np.zeros(len(data)))
    data['sup'] = pd.Series(np.zeros(len(data)))
    data['res'] = pd.Series(np.zeros(len(data)))
    data['positions'] = pd.Series(np.zeros(len(data)))
    data['signal'] = pd.Series(np.zeros(len(data)))
    in_support = 0
    in_resistance = 0

    for x in range((bin_width - 1) + bin_width, len(data)):
        data_section = data[x - bin_width:x + 1]
        support_level = min(data_section['price'])
        resistance_level = max(data_section['price'])
        range_level = resistance_level-support_level
        data['res'][x] = resistance_level
        data['sup'][x] = support_level
        data['sup_tolerance'][x] = support_level + 0.2 * range_level
        data['res_tolerance'][x] = resistance_level - 0.2 * range_level

        if ((data['price'][x] >= data['res_tolerance'][x]) and (data['price'][x] <= data['res'][x])):
            in_resistance+=1
            data['res_count'][x]=in_resistance
        elif ((data['price'][x] <= data['sup_tolerance'][x]) and (data['price'][x] >= data['sup'][x])):
            in_support += 1
            data['sup_count'][x] = in_support
        else:
            in_support = 0
            in_resistance = 0
        if in_resistance > 2:
            data['signal'][x] = 1
        elif in_support > 2:
            data['signal'][x] = 0
        else:
            data['signal'][x] = data['signal'][x - 1]

    data['positions'] = data['signal'].diff()


def visualize_data(symbol_data_signal):
    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel = 'Symbol price in USD')
    symbol_data_signal['sup'].plot(ax = ax1, color = 'g', lw = 2.)
    symbol_data_signal['res'].plot(ax = ax1, color = 'b', lw = 2.)
    symbol_data_signal['price'].plot(ax = ax1, color = 'r', lw = 2.)
    ax1.plot(symbol_data_signal.loc[symbol_data_signal.positions == 1.0].index,
           symbol_data_signal.price[symbol_data_signal.positions == 1.0],
           '^', markersize = 7, color = 'k',label = 'buy')
    ax1.plot(symbol_data_signal.loc[symbol_data_signal.positions == -1.0].index,
           symbol_data_signal.price[symbol_data_signal.positions == -1.0],
           'v', markersize = 7, color = 'k',label = 'sell')
    plt.legend()
    plt.show()

def view():
    pd.set_option('max_colwidth', 1000)
    pd.set_option('display.width', 1000)

print("Please enter a symbol, a channel, and a start and end date (YY-MM-DD) below: ")
get_data(symbol = input(), channel = input(), start_date = input(), end_date = input())

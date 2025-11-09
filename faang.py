#! /usr/bin/env python


# faang.py
# Authored by: Stephen Kerr

# Imports
import yfinance as yf # importing yfinance to access stock data

import datetime # importing datetime to access dates & times

import os # importing os to handle file paths

import matplotlib.pyplot as plt # importing matplotlib to plot data

import pandas as pd # importing pandas to handle dataframes


# Get the Data
def get_data(tickers=None, period='5d', interval='1h', save_dir='data'):
    '''
    Download data from yfinance and saves it to a csv file.
    Defaults to FAANG stocks if tickers is not passed.
    Filename Format: 'YYYYMMDD-HHmmss.csv'
    Returns the filepath and dataframe.
    '''
    
    if tickers is None:
        tickers = ['META','AAPL','AMZN','NFLX','GOOG']  # default to FAANG stocks
    
    # download the data
    df = yf.download(tickers=tickers, period=period, interval=interval)

    # save the dataframe to a csv file titled 'YYYYMMDD-HHmmss.csv'
    # in a data folder (note name of file should be the creation date and time)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv'
    filepath = os.path.join(save_dir, filename)
    df.to_csv(filepath) # save to csv
    
    return filepath, df 



# Plot the Data
def plot_data(filepath):
    '''
    Pass the filepath of the Stock data CSV file.
    Plots the Close prices of the stocks in the dataframe and saves the plot to a plots folder.
    '''
    df = pd.read_csv(filepath, header=[0,1], index_col=0, parse_dates=True)
    
    # plot the Close prices
    close_df = df['Close']
    close_df.plot(title=f'Close Prices of Stocks {datetime.datetime.now().strftime("%Y-%m-%d")}', figsize=(10,6))
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend(title='Stocks')
    plt.grid()
    

    # save the plot to a plots folder
    plots_dir = 'plots'
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    plot_filename = os.path.splitext(os.path.basename(filepath))[0] + '_close_prices.png'
    plot_filepath = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_filepath)
    # plt.show()

    return plot_filepath


# Example Usage
if __name__ == '__main__':
    # get data and save to csv
    data_filepath, data_df = get_data()
    print(f'Data saved to {data_filepath}')
    
    # plot the data
    plot_filepath = plot_data(data_filepath)
    print(f'Plot saved to {plot_filepath}')




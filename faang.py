#! /usr/bin/env python


# faang.py
# Authored by: Stephen Kerr

# Imports
import yfinance as yf # importing yfinance to access stock data

import datetime # importing datetime to access dates & times

import os # importing os to handle file paths

import matplotlib.pyplot as plt # importing matplotlib to plot data

import pandas as pd # importing pandas to handle dataframes

import matplotlib.dates as mdates # importing matplotlib.dates to handle date formatting in plots


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
# function plotdata(): plots the Close prices of the stocks in the dataframe
# pasing the filepath to read the csv file back in

def plot_data():
    '''
    Opens the latest data file in the data folder.
    Plots the Close prices of the stocks in the dataframe and saves the plot to a plots folder.
    '''

    # get the latest file in the data folder
    data_dir = 'data'
    files = os.listdir(data_dir) # list all files in the data folder
    files = [f for f in files if f.endswith('.csv')] # only the csv files
             
    if not files:
        raise FileNotFoundError('No data files found in the data folder.')
    
    # get the latest file based on the filename format 'YYYYMMDD-HHmmss.csv'
    latest_file = max(files)

    # construct the full filepath
    filepath = os.path.join(data_dir, latest_file)



    df = pd.read_csv(filepath, header=[0,1], index_col=0, parse_dates=True)
    
    # plot the Close prices
    close_df = df['Close']

    fig, ax = plt.subplots(figsize=(12, 6))


    close_df.plot(ax=ax, linewidth=2)
    
    ax.set_title(f"Close Prices of Stocks {close_df.index.min().strftime('%Y-%m-%d')} "
                 f"to {close_df.index.max().strftime('%Y-%m-%d')}",
              fontsize=16, fontweight='bold', pad=15) 

    ax.set_xlabel('Date', fontsize=14, fontweight='bold')
    ax.set_ylabel('Close Price ($ - USD)', fontsize=14, fontweight='bold')
    
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # formating x-axis for better readability using mdates
    ax.xaxis.set_major_locator(mdates.DayLocator())  # Show every 1 day
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # "Month Day"

    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)

    plt.tight_layout()


    ax.legend(title='Stocks', loc='best', frameon=True, shadow=True, fontsize=10)

    # save the plot to a plots folder
    plots_dir = 'plots'
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    plot_filename = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.png'
    plot_filepath = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_filepath, dpi=300, bbox_inches='tight')
    plt.show()

    return plot_filepath

# Example Usage
if __name__ == '__main__':
    # get data and save to csv
    data_filepath, data_df = get_data()
    print(f'Data saved to {data_filepath}')
    
    # plot the data
    plot_filepath = plot_data()
    print(f'Plot saved to {plot_filepath}')




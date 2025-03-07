import yfinance as yf
import pandas as pd
import os
import glob
from datetime import datetime

# cache data after a single API call to Yahoo Finance
# avoid server block with custom user agent

ticker_strings = ['PLTR', 'TSLA', 'COIN', 'MSTR', 'BABA', 'BIDU', 'JD', 'PDD']
recent_tickers = {'PLTR', 'COIN', 'PDD'}
output_dir = 'stock_data'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for ticker in ticker_strings:
    if ticker not in recent_tickers:
        data = yf.download(ticker, start="2014-01-01", end="2021-12-31")
    else:
        data = yf.download(ticker, start="2018-01-01", end="2021-12-31")
    data['ticker'] = ticker
    data['Date'] = data.index
    data.set_index('Date', inplace=True)
    monthly_avg = data['Close'].resample('M').mean()
    monthly_avg.to_csv(f"{output_dir}/{ticker}_monthly_avg_price.csv", header=True)

def combine_stock_data():
    output_dir = 'utils/stock_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    stock_files = glob.glob(f"{output_dir}/*_monthly_avg_price.csv")
    
    all_stock_data = {} # Store all of the stock data
    
    # Create date range matching crypto data (108 months from Aug 2012 to Jul 2021)
    end_date = pd.Period('2021-07')
    start_date = end_date - 107  # to get 108 months total
    full_date_range = pd.period_range(start=start_date, end=end_date, freq='M')
    
    for file in stock_files:
        print(f"Processing {file}...")
        
        stock_name = os.path.basename(file).replace('_monthly_avg_price.csv', '')
        
        df = pd.read_csv(file)
        df.index = pd.to_datetime(df.index if 'Date' not in df.columns else df['Date'])
        df.index = df.index.to_period('M')
        
        full_df = pd.DataFrame(index=full_date_range)
        price_col = 'Close' if 'Close' in df.columns else df.columns[0]
        
        full_df = full_df.join(df[price_col]).fillna(0)
        
        all_stock_data[stock_name] = full_df[price_col]
    
    combined_df = pd.DataFrame(all_stock_data)
    
    output_file = f"{output_dir}/all_stocks_monthly.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\nCombined stock data saved to {output_file}")
    
    print("\nFirst few rows of combined data:")
    print(combined_df.head())
    print(f"\nTotal number of rows: {len(combined_df)}")

def download_stock_data():
    ticker_strings = ['PLTR', 'TSLA', 'COIN', 'MSTR', 'BABA', 'BIDU', 'JD', 'PDD']
    recent_tickers = {'PLTR', 'COIN', 'PDD'}
    output_dir = 'utils/stock_data'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for ticker in ticker_strings:
        if ticker not in recent_tickers:
            data = yf.download(ticker, start="2014-01-01", end="2021-12-31")
        else:
            data = yf.download(ticker, start="2018-01-01", end="2021-12-31")
        data['ticker'] = ticker
        data['Date'] = data.index
        data.set_index('Date', inplace=True)
        monthly_avg = data['Close'].resample('M').mean()
        monthly_avg.to_csv(f"{output_dir}/{ticker}_monthly_avg_price.csv", header=True)

if __name__ == "__main__":
    download_stock_data()
    combine_stock_data() # Combining into a single file
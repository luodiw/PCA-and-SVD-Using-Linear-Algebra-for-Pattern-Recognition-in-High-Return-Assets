import pandas as pd
import os
import glob
from datetime import datetime

def analyze_date_ranges(input_file):
    df = pd.read_csv(input_file)
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = df['Date'].min()
    end_date = df['Date'].max()
    num_months = len(df['Date'].dt.to_period('M').unique())
    coin_name = os.path.basename(input_file).replace('coin_', '').replace('.csv', '')
    print(f"{coin_name}:")
    print(f"  Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"  Number of months: {num_months}")
    print()

def convert_to_monthly_averages(input_file, is_dogecoin=False):
    df = pd.read_csv(input_file)
    df['Date'] = pd.to_datetime(df['Date'])

    df['Average_Price'] = df[['High', 'Low', 'Open', 'Close']].mean(axis=1)
    
    # multiply by 100000 since Dogecoin prices are too small
    if is_dogecoin:
        df['Average_Price'] = df['Average_Price'] * 100000
    
    # extract year and month
    df['YearMonth'] = df['Date'].dt.to_period('M')
    
    # month average price
    monthly_df = df.groupby('YearMonth').agg({
        'Average_Price': 'mean'
    })
    
    # round if it's Dogecoin
    if is_dogecoin:
        monthly_df = monthly_df.round(4)  
    else:
        monthly_df = monthly_df.round(2)
    
    end_date = pd.Period('2021-07')
    start_date = end_date - 107  # to get 108 months total
    full_date_range = pd.period_range(start=start_date, end=end_date, freq='M')
    
    full_df = pd.DataFrame(index=full_date_range)
    
    full_df = full_df.join(monthly_df).fillna(0)
    return full_df['Average_Price']

def process_all_crypto_files():
    crypto_files = glob.glob("crypto/data/coin_*.csv")
    crypto_files = [f for f in crypto_files if '_monthly' not in f]
    
    all_crypto_data = {}
    
    for file in crypto_files:
        print(f"Processing {file}...")
        is_dogecoin = 'Dogecoin' in file
        
        crypto_name = os.path.basename(file).replace('coin_', '').replace('.csv', '')
        
        prices = convert_to_monthly_averages(file, is_dogecoin)
        
        all_crypto_data[crypto_name] = prices
    
    combined_df = pd.DataFrame(all_crypto_data)
    
    output_file = "crypto/combined_crypto_data/all_crypto_monthly.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\nCombined data saved to {output_file}")
    
    print("\nFirst few rows of combined data:")
    print(combined_df.head())
    
    print(f"\nTotal number of rows: {len(combined_df)}")

if __name__ == "__main__":
    process_all_crypto_files()

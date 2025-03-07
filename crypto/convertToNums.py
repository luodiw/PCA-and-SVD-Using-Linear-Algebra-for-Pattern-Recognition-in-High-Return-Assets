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
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate average price for each day first
    df['Average_Price'] = df[['High', 'Low', 'Open', 'Close']].mean(axis=1)
    
    # For Dogecoin, multiply by 100000 to make numbers more readable
    if is_dogecoin:
        df['Average_Price'] = df['Average_Price'] * 100000
    
    # Extract year and month from the date
    df['YearMonth'] = df['Date'].dt.to_period('M')
    
    # Calculate monthly averages for the average price
    monthly_df = df.groupby('YearMonth').agg({
        'Average_Price': 'mean'
    })
    
    # Round based on whether it's Dogecoin or not
    if is_dogecoin:
        monthly_df = monthly_df.round(4)  # Keep more decimal places for Dogecoin
    else:
        monthly_df = monthly_df.round(2)
    
    # Create a date range for exactly 108 months (9 years), ending at July 2021
    end_date = pd.Period('2021-07')
    start_date = end_date - 107  # to get 108 months total
    full_date_range = pd.period_range(start=start_date, end=end_date, freq='M')
    
    # Create a new DataFrame with all months
    full_df = pd.DataFrame(index=full_date_range)
    
    # Merge with our data, filling missing values with 0
    full_df = full_df.join(monthly_df).fillna(0)
    
    return full_df['Average_Price']

def process_all_crypto_files():
    # Get all original cryptocurrency CSV files (excluding monthly files)
    crypto_files = glob.glob("crypto/data/coin_*.csv")
    crypto_files = [f for f in crypto_files if '_monthly' not in f]
    
    # Create a dictionary to store each cryptocurrency's data
    all_crypto_data = {}
    
    # Process each cryptocurrency
    for file in crypto_files:
        print(f"Processing {file}...")
        is_dogecoin = 'Dogecoin' in file
        
        # Get the cryptocurrency name from the filename
        crypto_name = os.path.basename(file).replace('coin_', '').replace('.csv', '')
        
        # Get the price data
        prices = convert_to_monthly_averages(file, is_dogecoin)
        
        # Store in dictionary
        all_crypto_data[crypto_name] = prices
    
    # Combine all data into a single DataFrame
    combined_df = pd.DataFrame(all_crypto_data)
    
    output_file = "crypto/combined_crypto_data/all_crypto_monthly.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\nCombined data saved to {output_file}")
    
    # Print the first few rows to verify
    print("\nFirst few rows of combined data:")
    print(combined_df.head())
    
    # Verify number of rows
    print(f"\nTotal number of rows: {len(combined_df)}")

if __name__ == "__main__":
    process_all_crypto_files()

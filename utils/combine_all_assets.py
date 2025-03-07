import pandas as pd

def combine_all_assets():
    crypto_file = "crypto/combined_crypto_data/all_crypto_monthly.csv"
    stocks_file = "utils/stock_data/combined_stocks_2013_2021.csv"
    
    crypto_df = pd.read_csv(crypto_file)
    stocks_df = pd.read_csv(stocks_file)
    
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date']).dt.strftime('%Y-%m')
    stocks_df.set_index('Date', inplace=True)
    
    combined_df = pd.DataFrame(index=stocks_df.index)
    
    for column in crypto_df.columns:
        combined_df[f"crypto_{column}"] = crypto_df[column].values[-len(stocks_df):]
    
    for column in stocks_df.columns:
        combined_df[f"stock_{column}"] = stocks_df[column]
    
    combined_df = combined_df.fillna(0)
    
    combined_df.reset_index(names=['Date'], inplace=True)
    
    output_file = "combined_assets_2013_2021.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"Combined asset data saved to {output_file}")
    print("\nFirst few rows of combined data:")
    print(combined_df.head())
    print(f"\nTotal columns: {len(combined_df.columns)}")
    print("\nColumns:", list(combined_df.columns))

if __name__ == "__main__":
    combine_all_assets() 
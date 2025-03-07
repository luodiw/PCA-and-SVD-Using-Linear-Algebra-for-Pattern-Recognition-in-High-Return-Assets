import pandas as pd

def combine_all_assets_no_dates():
    # Crypto and stocks data files
    crypto_file = "crypto/combined_crypto_data/all_crypto_monthly.csv"
    stocks_file = "utils/stock_data/combined_stocks_2013_2021.csv"
    
    crypto_df = pd.read_csv(crypto_file)
    stocks_df = pd.read_csv(stocks_file)
    
    # new combined dataframe
    combined_data = {}
    
    for column in crypto_df.columns:
        combined_data[f"crypto_{column}"] = crypto_df[column].values[-len(stocks_df):]
    
    stocks_df.set_index('Date', inplace=True)
    for column in stocks_df.columns:
        combined_data[f"stock_{column}"] = stocks_df[column].values
    
    # NaN == 0
    combined_df = pd.DataFrame(combined_data)
    combined_df = combined_df.fillna(0)
    
    output_file = "combined_assets_no_dates.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"Combined asset data (without dates) saved to {output_file}")
    print("\nFirst few rows of combined data:")
    print(combined_df.head())
    print(f"\nTotal columns: {len(combined_df.columns)}")
    print("\nColumns:", list(combined_df.columns))
    print(f"\nTotal rows: {len(combined_df)}")

if __name__ == "__main__":
    combine_all_assets_no_dates() 

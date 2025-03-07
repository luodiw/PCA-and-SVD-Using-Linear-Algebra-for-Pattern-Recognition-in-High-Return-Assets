import pandas as pd

def combine_all_assets_no_dates():
    # Read the crypto and stock data
    crypto_file = "crypto/combined_crypto_data/all_crypto_monthly.csv"
    stocks_file = "utils/stock_data/combined_stocks_2013_2021.csv"
    
    # Read both files
    crypto_df = pd.read_csv(crypto_file)
    stocks_df = pd.read_csv(stocks_file)
    
    # Create new DataFrame for combined data
    combined_data = {}
    
    # Add crypto data first
    for column in crypto_df.columns:
        # Take only the last values to match stock data length
        combined_data[f"crypto_{column}"] = crypto_df[column].values[-len(stocks_df):]
    
    # Add stock data (excluding the Date column)
    stocks_df.set_index('Date', inplace=True)
    for column in stocks_df.columns:
        combined_data[f"stock_{column}"] = stocks_df[column].values
    
    # Create DataFrame and fill any NaN values with 0
    combined_df = pd.DataFrame(combined_data)
    combined_df = combined_df.fillna(0)
    
    # Save the combined data without dates
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
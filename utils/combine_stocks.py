import pandas as pd
import glob
import os

def combine_stock_data():
    date_range = pd.date_range(start='2013-04-01', end='2021-12-31', freq='M')
    
    combined_df = pd.DataFrame(index=date_range)
    combined_df.index = combined_df.index.strftime('%Y-%m')  # Format dates as YYYY-MM
    
    stock_files = glob.glob("utils/stock_data/*_monthly_avg_price.csv")
    
    for file in stock_files:
        stock_symbol = os.path.basename(file).replace('_monthly_avg_price.csv', '')
        
        stock_data = pd.read_csv(file)
        stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.strftime('%Y-%m')
        stock_data.set_index('Date', inplace=True)
        
        combined_df[stock_symbol] = stock_data.iloc[:, 0]
    
    combined_df = combined_df.fillna(0)
    
    combined_df.reset_index(names=['Date'], inplace=True)
    
    output_file = "utils/stock_data/combined_stocks_2013_2021.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"Combined stock data saved to {output_file}")
    print("\nFirst few rows of combined data:")
    print(combined_df.head())
    
if __name__ == "__main__":
    combine_stock_data() 
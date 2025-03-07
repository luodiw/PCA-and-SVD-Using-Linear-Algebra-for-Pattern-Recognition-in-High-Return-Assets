import pandas as pd
import numpy as np

# Read the CSV files
interest_rates = pd.read_csv('interest_rates.csv')
assets = pd.read_csv('combined_assets_no_dates.csv')

# Create a date range that matches the assets data
# Since we know the data starts from April 2013 and goes monthly
date_range = pd.date_range(start='2013-04-01', periods=len(assets), freq='ME')

assets['Date'] = date_range
assets['Month'] = assets['Date'].dt.strftime('%B')
assets['Year'] = assets['Date'].dt.year

combined_data = pd.merge(assets, interest_rates, on=['Month', 'Year'], how='left')
combined_data = combined_data.drop('Date', axis=1)

combined_data = combined_data.rename(columns={
    'Federal Reserve Midpoint (%)': 'US_Fed_Rate',
    'ECB Main Refi Rate (%)': 'European_Central_Bank_Rate',
    'PBOC Rate (%)': 'China_Central_Bank_Rate'
})

rate_cols = ['US_Fed_Rate', 'European_Central_Bank_Rate', 'China_Central_Bank_Rate']
asset_cols = [col for col in combined_data.columns if col not in ['Month', 'Year'] + rate_cols]

# Function to calculate relative change considering zero values as starting points
def calculate_relative_change(series):
    changes = []
    last_valid = None
    
    for i in range(len(series)):
        current = series.iloc[i]
        
        if i == 0 or (last_valid is None and current != 0):
            changes.append(0)
            if current != 0:
                last_valid = current
        else:
            if last_valid is None:
                changes.append(0)
            else:
                change = current - last_valid
                changes.append(change)
            if current != 0:
                last_valid = current
                
    return changes

# Calculate relative changes for all columns
all_cols = rate_cols + asset_cols
change_cols = []

for col in all_cols:
    change_col = f'{col}_change'
    change_cols.append(change_col)
    combined_data[change_col] = calculate_relative_change(combined_data[col])

# Organize columns with original values first, then changes
final_columns = all_cols + change_cols
combined_data = combined_data[final_columns]

combined_data.to_csv('combined_assets_with_rates.csv', index=False)

print("Data has been combined and saved to 'combined_assets_with_rates.csv' with monthly changes")
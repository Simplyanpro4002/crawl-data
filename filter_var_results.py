import pandas as pd
import json

# Read the zero volume stocks
with open('zero_volume_counts.json', 'r') as f:
    zero_volume_stocks = json.load(f)

# Read the VAR results
var_df = pd.read_csv('historical_var_95_results.csv')

# Filter out stocks that are in zero_volume_stocks
filtered_df = var_df[~var_df['stock_code'].isin(zero_volume_stocks.keys())]

# Save the filtered results
filtered_df.to_csv('filtered_historical_var_95_results.csv', index=False)

print(f"Original number of stocks: {len(var_df)}")
print(f"Number of stocks after filtering: {len(filtered_df)}")
print(f"Number of stocks removed: {len(var_df) - len(filtered_df)}") 
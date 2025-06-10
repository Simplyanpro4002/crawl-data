import json
import pandas as pd

# Load VaR values
var_df = pd.read_csv('filtered_historical_var_95_results.csv').set_index('stock_code')

# Load bins summary
with open('var_bins_summary.json', 'r') as f:
    bins = json.load(f)

# Sort stocks in each bin by their VaR value
for bin_info in bins:
    stocks = bin_info['stocks']
    # Get (stock, var) pairs and sort
    stock_vars = [(stock, var_df.loc[stock, 'historical_var_95']) for stock in stocks if stock in var_df.index]
    stock_vars_sorted = sorted(stock_vars, key=lambda x: x[1])
    # Replace with sorted stock codes
    bin_info['stocks'] = [s for s, v in stock_vars_sorted]

# Save the updated bins summary
with open('var_bins_summary.json', 'w') as f:
    json.dump(bins, f, indent=2)

print('Stocks in each bin have been sorted by VaR value (ascending).') 
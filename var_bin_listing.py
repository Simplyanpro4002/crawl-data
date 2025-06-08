import pandas as pd
import numpy as np

# Read the VaR data
var_df = pd.read_csv('historical_var_95_results.csv')

# Define bins (same as in the plot)
bins = np.linspace(var_df['historical_var_95'].min(), var_df['historical_var_95'].max(), 31)  # 30 bins
labels = [f"{bins[i]:.4f} - {bins[i+1]:.4f}" for i in range(len(bins)-1)]

# Assign each stock to a bin
var_df['bin'] = pd.cut(var_df['historical_var_95'], bins=bins, labels=labels, include_lowest=True)

# Group by bin and list stocks
bin_groups = var_df.groupby('bin')['stock_code'].apply(list)
frequencies = var_df['bin'].value_counts().sort_index()

# Output the results
for bin_label in labels:
    stocks_in_bin = bin_groups.get(bin_label, [])
    freq = frequencies.get(bin_label, 0)
    print(f"Range: {bin_label} | Frequency: {freq}")
    if stocks_in_bin:
        print(f"  Stocks: {', '.join(stocks_in_bin)}")
    else:
        print("  Stocks: None")
    print('-' * 60) 
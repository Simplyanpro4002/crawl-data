import pandas as pd
from pathlib import Path

def main():
    # Read the original VaR results
    var_df = pd.read_csv('var_results/var_results.csv')
    
    # Select only stock_code and historical_var_95 columns
    historical_var_df = var_df[['stock_code', 'historical_var_95']]
    
    # Sort by historical_var_95 in descending order
    historical_var_df = historical_var_df.sort_values('historical_var_95', ascending=False)
    
    # Save to new file
    output_file = Path('historical_var_95_results.csv')
    historical_var_df.to_csv(output_file, index=False)
    
    # Print summary statistics
    print("\nSummary of 95% Historical VaR:")
    print(historical_var_df['historical_var_95'].describe())
    
    # Print top 5 stocks with highest VaR
    print("\nTop 5 stocks with highest 95% Historical VaR:")
    print(historical_var_df.head())

if __name__ == "__main__":
    main() 
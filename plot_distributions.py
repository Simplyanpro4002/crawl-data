import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

def plot_stock_distribution(returns, var_results, stock_code, output_dir):
    """
    Create a plot showing the distribution of monthly returns and VaR levels
    """
    plt.figure(figsize=(12, 6))
    
    # Plot the distribution of returns
    sns.histplot(data=returns, x='log_return', bins=30, kde=True)
    
    # Add vertical lines for VaR levels
    plt.axvline(x=-var_results['parametric_var_95'], color='red', linestyle='--', 
                label='95% Parametric VaR')
    plt.axvline(x=-var_results['historical_var_95'], color='green', linestyle='--', 
                label='95% Historical VaR')
    plt.axvline(x=-var_results['parametric_var_99'], color='orange', linestyle='--', 
                label='99% Parametric VaR')
    plt.axvline(x=-var_results['historical_var_99'], color='purple', linestyle='--', 
                label='99% Historical VaR')
    
    # Add labels and title
    plt.title(f'Distribution of Monthly Returns and VaR for {stock_code}')
    plt.xlabel('Monthly Log Return')
    plt.ylabel('Frequency')
    plt.legend()
    
    # Save the plot
    output_file = output_dir / f'{stock_code}_var_distribution.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Create output directory
    output_dir = Path('plot')
    output_dir.mkdir(exist_ok=True)
    
    # Read VaR results
    var_df = pd.read_csv('var_results/var_results.csv')
    
    # Process each stock
    for stock_code in var_df['stock_code']:
        print(f"Plotting distribution for {stock_code}...")
        
        try:
            # Read monthly returns
            returns_file = Path('monthly_returns') / f'monthly_returns_{stock_code}.csv'
            returns = pd.read_csv(returns_file, index_col=0, parse_dates=True)
            
            # Get VaR results for this stock
            var_results = var_df[var_df['stock_code'] == stock_code].iloc[0]
            
            # Create the plot
            plot_stock_distribution(returns, var_results, stock_code, output_dir)
            
        except Exception as e:
            print(f"Error processing {stock_code}: {str(e)}")

if __name__ == "__main__":
    main() 
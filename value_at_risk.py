import numpy as np
from scipy import stats
import pandas as pd
import json
import os

import matplotlib.pyplot as plt

def calculate_log_returns(stock_data):
    """
    Calculate daily log returns from adjusted close prices
    
    Parameters:
    stock_data (DataFrame): DataFrame containing 'ClosePriceAdjusted' column
    
    Returns:
    array: log_returns array
    """
    # Remove entries where ClosePriceAdjusted is 0
    stock_data = stock_data[stock_data['ClosePriceAdjusted'] != 0].copy()

    # Calculate log returns
    log_returns = np.log(stock_data['ClosePriceAdjusted'] / stock_data['ClosePriceAdjusted'].shift(1)).dropna()
    
    return log_returns


def calculate_var(returns, confidence_level=0.95, initial_investment=1000000):
    """
    Calculate Value at Risk (VaR) for a given set of returns
    
    Parameters:
    returns (array-like): Array of historical returns
    confidence_level (float): Confidence level for VaR calculation (default: 0.95)
    initial_investment (float): Initial investment amount (default: 1000000)
    
    Returns:
    float: Value at Risk
    """
    # Convert returns to numpy array if needed
    returns = np.array(returns)
    
    # Calculate VaR
    var_percentile = 1 - confidence_level
    var = np.percentile(returns, var_percentile * 100)
    
    # Convert to monetary value
    var_amount = initial_investment * abs(var)
    
    return var_amount

def calculate_monthly_var(daily_returns, confidence_level=0.95, initial_investment=1000000):
    """
    Calculate 1-month Value at Risk (VaR) from daily returns
    
    Parameters:
    daily_returns (array-like): Array of daily returns
    confidence_level (float): Confidence level for VaR calculation (default: 0.95)
    initial_investment (float): Initial investment amount (default: 1000000)
    
    Returns:
    float: 1-month Value at Risk
    """
    # Convert returns to numpy array if needed
    daily_returns = np.array(daily_returns)
    
    # Calculate monthly volatility (assuming 21 trading days)
    monthly_vol = np.std(daily_returns) * np.sqrt(21)
    
    # Calculate monthly VaR using parametric method
    z_score = stats.norm.ppf(1 - confidence_level)
    monthly_var = initial_investment * (z_score * monthly_vol)
    
    return monthly_var

def plot_var_distribution(returns, confidence_level=0.95, initial_investment=1000000, filename='var_distribution.png'):
    """
    Plot a histogram of returns and save VaR plot to file
    
    Parameters:
    returns (array-like): Array of historical returns
    confidence_level (float): Confidence level for VaR calculation (default: 0.95)
    initial_investment (float): Initial investment amount (default: 1000000)
    filename (str): Output filename for the plot (default: 'var_distribution.png')
    """
    # Calculate VaR
    var = calculate_var(returns, confidence_level, initial_investment)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot histogram of returns
    plt.hist(returns, bins=50, alpha=0.7, color='blue')
    
    # Add VaR line
    var_percentile = np.percentile(returns, (1 - confidence_level) * 100)
    plt.axvline(x=var_percentile, color='red', linestyle='--')
    
    # Add labels and title
    plt.title(f'Return Distribution and VaR at {confidence_level*100}% Confidence Level')
    plt.xlabel('Returns')
    plt.ylabel('Count')
    
    # Add VaR annotation
    plt.text(var_percentile, plt.ylim()[1]*0.9, 
             f'VaR: ${var:,.2f}',
             rotation=90,
             verticalalignment='top')
    
    plt.grid(True, alpha=0.3)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Get all JSON files in the results folder
    json_files = [f for f in os.listdir('results') if f.endswith('.json')]

    for json_file in json_files:
        stock_code = json_file.replace('stock_price_', '').replace('.json', '')
        print(f"\nProcessing {stock_code}...")

        # Read the JSON file
        with open(os.path.join('results', json_file), 'r') as file:
            data = json.load(file)

        # Convert to DataFrame
        stock_price_df = pd.DataFrame(data)
        print(f"Total records fetched for {stock_code}: {len(stock_price_df)}")

        # Convert TradingDate to datetime
        stock_price_df['TradingDate'] = pd.to_datetime(stock_price_df['TradingDate'], format='%d/%m/%Y')

        # Convert ClosePriceAdjusted to float
        stock_price_df['ClosePriceAdjusted'] = stock_price_df['ClosePriceAdjusted'].astype(float)

        # Sort by date
        stock_price_df = stock_price_df.sort_values('TradingDate')

        # Calculate log returns
        log_returns = calculate_log_returns(stock_price_df)

        # Calculate monthly VaR
        monthly_var = calculate_monthly_var(log_returns, confidence_level=0.95, initial_investment=1000000)
        print(f"{stock_code} Monthly Value at Risk: ${monthly_var:,.2f}")

        # Plot and save the VaR distribution
        plot_var_distribution(log_returns, confidence_level=0.95, initial_investment=1000000, 
                            filename=f'{stock_code.lower()}_var_distribution.png')
        
   
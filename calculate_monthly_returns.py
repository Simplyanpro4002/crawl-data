import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

def calculate_monthly_returns(file_path):
    # Read JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Convert TradingDate to datetime
    df['TradingDate'] = pd.to_datetime(df['TradingDate'], format='%d/%m/%Y')
    
    # Convert ClosePriceAdjusted to float
    df['ClosePriceAdjusted'] = pd.to_numeric(df['ClosePriceAdjusted'])
    
    # Sort by date
    df = df.sort_values('TradingDate')
    
    # Calculate daily log returns
    df['log_return'] = np.log(df['ClosePriceAdjusted'] / df['ClosePriceAdjusted'].shift(1))
    
    # Calculate monthly returns
    monthly_returns = df.set_index('TradingDate')['log_return'].resample('M').sum()
    
    return monthly_returns

def main():
    # Directory containing the JSON files
    results_dir = Path('results')
    
    # Create output directory if it doesn't exist
    output_dir = Path('monthly_returns')
    output_dir.mkdir(exist_ok=True)
    
    # Process each JSON file
    for file_path in results_dir.glob('stock_price_*.json'):
        stock_code = file_path.stem.split('_')[-1]
        print(f"Processing {stock_code}...")
        
        try:
            monthly_returns = calculate_monthly_returns(file_path)
            
            # Save to CSV
            output_file = output_dir / f'monthly_returns_{stock_code}.csv'
            monthly_returns.to_csv(output_file)
            
        except Exception as e:
            print(f"Error processing {stock_code}: {str(e)}")

if __name__ == "__main__":
    main() 
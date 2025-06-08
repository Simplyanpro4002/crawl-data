import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

def calculate_var(returns, confidence_levels=[0.95, 0.99]):
    """
    Calculate Value at Risk using different methods:
    1. Parametric (Normal) VaR
    2. Historical VaR
    """
    results = {}
    
    # Parametric (Normal) VaR
    mean = returns.mean()
    std = returns.std()
    
    for conf_level in confidence_levels:
        # Parametric VaR
        z_score = stats.norm.ppf(1 - conf_level)
        parametric_var = -(mean + z_score * std)
        
        # Historical VaR
        historical_var = -np.percentile(returns, (1 - conf_level) * 100)
        
        results[f'parametric_var_{int(conf_level*100)}'] = parametric_var
        results[f'historical_var_{int(conf_level*100)}'] = historical_var
    
    return results

def main():
    # Directory containing the monthly returns
    returns_dir = Path('monthly_returns')
    output_dir = Path('var_results')
    output_dir.mkdir(exist_ok=True)
    
    # Store all VaR results
    all_var_results = []
    
    # Process each returns file
    for file_path in returns_dir.glob('monthly_returns_*.csv'):
        stock_code = file_path.stem.split('_')[-1]
        print(f"Calculating VaR for {stock_code}...")
        
        try:
            # Read monthly returns
            returns = pd.read_csv(file_path, index_col=0, parse_dates=True)
            returns = returns['log_return']  # Get the returns series
            
            # Calculate VaR
            var_results = calculate_var(returns)
            
            # Add stock code to results
            var_results['stock_code'] = stock_code
            
            # Add to list of results
            all_var_results.append(var_results)
            
        except Exception as e:
            print(f"Error processing {stock_code}: {str(e)}")
    
    # Convert results to DataFrame
    var_df = pd.DataFrame(all_var_results)
    
    # Save results
    output_file = output_dir / 'var_results.csv'
    var_df.to_csv(output_file, index=False)
    
    # Print summary statistics
    print("\nVaR Summary Statistics:")
    print(var_df.describe())

if __name__ == "__main__":
    main() 
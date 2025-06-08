import pandas as pd
import numpy as np
from pathlib import Path

def calculate_var_std():
    # Read the historical VaR results
    var_df = pd.read_csv('historical_var_95_results.csv')
    
    # Calculate standard deviation
    std_var = var_df['historical_var_95'].std()
    
    # Print results
    print(f"\nStandard Deviation of 95% Historical VaR: {std_var:.4f}")
    print(f"This means the VaR values typically deviate by {std_var:.4f} from the mean")
    
    # Additional statistics
    print("\nAdditional Statistics:")
    print(f"Mean VaR: {var_df['historical_var_95'].mean():.4f}")
    print(f"Min VaR: {var_df['historical_var_95'].min():.4f}")
    print(f"Max VaR: {var_df['historical_var_95'].max():.4f}")
    print(f"Range: {var_df['historical_var_95'].max() - var_df['historical_var_95'].min():.4f}")

if __name__ == "__main__":
    calculate_var_std() 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def plot_var_distribution():
    # Create output directory
    output_dir = Path('var_analysis')
    output_dir.mkdir(exist_ok=True)
    
    # Read the VaR data
    var_df = pd.read_csv('historical_var_95_results.csv')
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Plot histogram with KDE
    sns.histplot(data=var_df, x='historical_var_95', bins=30, kde=True)
    
    # Add vertical lines for mean and standard deviation
    mean_var = var_df['historical_var_95'].mean()
    std_var = var_df['historical_var_95'].std()
    
    plt.axvline(x=mean_var, color='red', linestyle='--', 
                label=f'Mean VaR: {mean_var:.4f}')
    plt.axvline(x=mean_var + std_var, color='green', linestyle='--', 
                label=f'+1 Std Dev: {mean_var + std_var:.4f}')
    plt.axvline(x=mean_var - std_var, color='green', linestyle='--', 
                label=f'-1 Std Dev: {mean_var - std_var:.4f}')
    
    # Add labels and title
    plt.title('Distribution of 95% Historical VaR Values\n(Standard Deviation: {:.4f})'.format(std_var))
    plt.xlabel('95% Historical VaR')
    plt.ylabel('Frequency')
    plt.legend()
    
    # Add text box with statistics
    stats_text = f'Statistics:\nMean: {mean_var:.4f}\nStd Dev: {std_var:.4f}\nMin: {var_df["historical_var_95"].min():.4f}\nMax: {var_df["historical_var_95"].max():.4f}'
    plt.text(0.95, 0.95, stats_text,
             transform=plt.gca().transAxes,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Save the plot
    output_file = output_dir / 'var_distribution.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    plot_var_distribution() 
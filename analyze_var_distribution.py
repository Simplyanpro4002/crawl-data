import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

# Create output directory for plots
output_dir = Path('var_analysis')
output_dir.mkdir(exist_ok=True)

# Read the filtered VAR results
var_df = pd.read_csv('filtered_historical_var_95_results.csv')

# Calculate standard deviation
std_dev = var_df['historical_var_95'].std()
mean = var_df['historical_var_95'].mean()

# Create the distribution plot
plt.figure(figsize=(12, 6))
sns.histplot(data=var_df, x='historical_var_95', bins=30, kde=True)

# Add mean and standard deviation lines
plt.axvline(mean, color='red', linestyle='--', label=f'Mean: {mean:.4f}')
plt.axvline(mean + std_dev, color='green', linestyle='--', label=f'+1 Std Dev: {mean + std_dev:.4f}')
plt.axvline(mean - std_dev, color='green', linestyle='--', label=f'-1 Std Dev: {mean - std_dev:.4f}')

# Customize the plot
plt.title('Distribution of Monthly VaR (95%) Values')
plt.xlabel('VaR Value')
plt.ylabel('Frequency')
plt.legend()

# Add text box with statistics
stats_text = f'Standard Deviation: {std_dev:.4f}\nMean: {mean:.4f}'
plt.text(0.95, 0.95, stats_text,
         transform=plt.gca().transAxes,
         verticalalignment='top',
         horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Save the plot
plt.savefig(output_dir / 'var_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"Standard Deviation of Monthly VaR: {std_dev:.4f}")
print(f"Mean of Monthly VaR: {mean:.4f}")
print(f"Plot saved to: {output_dir / 'var_distribution.png'}") 
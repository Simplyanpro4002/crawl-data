import json
from pathlib import Path
import pandas as pd

def count_zero_volumes():
    # Directory containing the stock price JSON files
    results_dir = Path('results')
    
    # Dictionary to store results
    zero_volume_counts = {}
    
    # Process each JSON file
    for file_path in results_dir.glob('stock_price_*.json'):
        stock_code = file_path.stem.split('_')[-1]
        print(f"Processing {stock_code}...")
        
        try:
            # Read JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Count occurrences of "TotalMatchVol": "0"
            zero_count = sum(1 for item in data if item.get('TotalMatchVol') == '0')
            
            # Store result
            zero_volume_counts[stock_code] = zero_count
            
        except Exception as e:
            print(f"Error processing {stock_code}: {str(e)}")
    
    # Convert to DataFrame for better visualization
    df = pd.DataFrame(list(zero_volume_counts.items()), columns=['Stock', 'ZeroVolumeCount'])
    df = df.sort_values('ZeroVolumeCount', ascending=False)
    
    # Filter stocks with more than 100 zero volumes
    high_zero_volume_stocks = df[df['ZeroVolumeCount'] > 100]
    
    # Save results to JSON
    output_file = 'zero_volume_counts.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(zero_volume_counts, f, indent=4)
    
    # Print summary of stocks with high zero volumes
    print("\nStocks with more than 100 zero volume entries:")
    print(high_zero_volume_stocks)
    print(f"\nTotal number of stocks with >100 zero volumes: {len(high_zero_volume_stocks)}")
    print(f"\nFull results saved to {output_file}")

if __name__ == "__main__":
    count_zero_volumes() 
import json
import os
from ssi_fc_data import fc_md_client, model
import config
from datetime import datetime, timedelta
import time
from constants import *

client = fc_md_client.MarketDataClient(config)

def save_to_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def md_get_stock_price(ticker):
    # Check if file already exists
    filename = f'results/stock_price_{ticker}.json'
    if os.path.exists(filename):
        print(f"File {filename} already exists. Skipping.")
        return

    all_data = []
    start_date = datetime.strptime('07/06/2022', '%d/%m/%Y')
    end_date = datetime.strptime('07/06/2025', '%d/%m/%Y')
    
    while start_date < end_date:
        # Calculate chunk end date (30 days from start or final end date, whichever is earlier)
        chunk_end = min(start_date + timedelta(days=29), end_date)
        
        # Convert dates to required string format
        start_str = start_date.strftime('%d/%m/%Y')
        end_str = chunk_end.strftime('%d/%m/%Y')
        
        page_index = 1
        while True:
            req = model.daily_stock_price(ticker, start_str, end_str, page_index, 1000)
            data = client.daily_stock_price(config, req)

            print(f"Fetching data for {ticker} from {start_str} to {end_str}, page {page_index}")

            if data['data'] is None:
                print(f"No more data available for {start_str} to {end_str}, page {page_index}. Stopping.")
                break

            all_data.extend(data['data'])
            page_index += 1
            time.sleep(0.7)  # Add 700ms delay between API calls

        # Move to next chunk
        start_date = chunk_end + timedelta(days=1)
        time.sleep(0.7)  # Add 700ms delay between date chunks

    if len(all_data) == 0:
        print(f"No data found for {ticker} in the specified date range.")
    else:
        print(f"Total records fetched for {ticker}: {len(all_data)}")
        save_to_json_file(f'results/stock_price_{ticker}.json', all_data)


if __name__ == "__main__":
    for ticker in tickers:
        print(f"Fetching stock price for {ticker}")
        max_attempts = 10
        attempt = 1
        while attempt <= max_attempts:
            try:
                md_get_stock_price(ticker)
                break  # Success, exit the retry loop
            except Exception as e:
                if attempt == max_attempts:
                    print(f"Failed to fetch data for {ticker} after {max_attempts} attempts. Error: {e}")
                else:
                    print(f"Attempt {attempt} failed for {ticker}. Retrying... Error: {e}")
                    time.sleep(2)  # Wait 500 milliseconds before retrying
                attempt += 1
                
               
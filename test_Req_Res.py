import json
from ssi_fc_data import fc_md_client, model
import config
from datetime import datetime, timedelta
import time
from constants import tickers

client = fc_md_client.MarketDataClient(config)

def save_to_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def md_access_token():
    data = client.access_token(model.accessToken(config.consumerID, config.consumerSecret))
    save_to_json_file('access_token.json', data)

def md_get_securities_list():
    req = model.securities('HNX', 1, 100)
    data = client.securities(config, req)
    save_to_json_file('securities_list.json', data)

def md_get_securities_details():
    req = model.securities_details('HNX', 'ACB', 1, 100)
    data = client.securities_details(config, req)
    save_to_json_file('securities_details.json', data)

def md_get_index_components():
    data = client.index_components(config, model.index_components('vn100', 1, 100))
    save_to_json_file('index_components.json', data)

def md_get_index_list():
    data = client.index_list(config, model.index_list('hnx', 1, 100))
    save_to_json_file('index_list.json', data)

def md_get_daily_OHLC():
    data = client.daily_ohlc(config, model.daily_ohlc('ssi', '15/10/2020', '15/10/2020', 1, 100, True))
    save_to_json_file('daily_ohlc.json', data)

def md_get_intraday_OHLC():
    data = client.intraday_ohlc(config, model.intraday_ohlc('fpt', '15/10/2020', '15/10/2020', 1, 100, True, 1))
    save_to_json_file('intraday_ohlc.json', data)

def md_get_daily_index():
    data = client.daily_index(config, model.daily_index('123', 'VN100', '15/10/2020', '15/10/2020', 1, 100, '', ''))
    save_to_json_file('daily_index.json', data)

def md_get_stock_price(ticker, exchange):
    all_data = []
    start_date = datetime.strptime('06/07/2022', '%d/%m/%Y')
    end_date = datetime.strptime('06/07/2025', '%d/%m/%Y')
    
    while start_date < end_date:
        # Calculate chunk end date (30 days from start or final end date, whichever is earlier)
        chunk_end = min(start_date + timedelta(days=29), end_date)
        
        # Convert dates to required string format
        start_str = start_date.strftime('%d/%m/%Y')
        end_str = chunk_end.strftime('%d/%m/%Y')
        
        page_index = 1
        while True:
            req = model.daily_stock_price(ticker, start_str, end_str, page_index, 1000, exchange)
            data = client.daily_stock_price(config, req)
            print(f"Fetching data from {start_str} to {end_str}, page {page_index}")
            
            if data['data'] is None:
                print(f"No more data available for {start_str} to {end_str}, page {page_index}. Stopping.")
                break

            all_data.extend(data['data'])
            page_index += 1
            time.sleep(0.5)  # Add 500ms delay between API calls
        
        # Move to next chunk
        start_date = chunk_end + timedelta(days=1)
        time.sleep(1)  # Add 1 second delay between date chunks

    save_to_json_file(f'stock_price_{ticker}_{exchange}.json', all_data)

def main():
    while True:
        print('11  - Securities List')
        print('12  - Securities Details')
        print('13  - Index Components')
        print('14  - Index List')
        print('15  - Daily OHLC')
        print('16  - Intraday OHLC')
        print('17  - Daily index')
        print('18  - Stock price')
        value = input('Enter your choice: ')

        if value == '11':
            md_get_securities_list()
        elif value == '12':
            md_get_securities_details()
        elif value == '13':
            md_get_index_components()
        elif value == '14':
            md_get_index_list()
        elif value == '15':
            md_get_daily_OHLC()
        elif value == '16':
            md_get_intraday_OHLC()
        elif value == '17':
            md_get_daily_index()
        elif value == '18':
            md_get_stock_price()

if __name__ == '__main__':
    main()
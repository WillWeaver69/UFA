import requests
import pandas as pd
from datetime import datetime


def convert_timestamp(timestamp_ms):
    """Convert Unix timestamp in milliseconds to a human-readable date-time format."""
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

def fetch_data(url, start_date, limit=500):
    # Convert start_date to Unix timestamp in milliseconds
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp()) * 1000
    # Set initial end_timestamp to current time
    end_timestamp = int(datetime.now().timestamp()) * 1000

    column_names = ['symbol','sumOpenInterest','sumOpenInterestValue','timestamp']
    df = pd.DataFrame(columns = column_names)
    all_data = []
    while True:
        # Update the URL with the current start and end times
        current_url = f"{url}&startTime={start_timestamp}&endTime={end_timestamp}&limit={limit}"
        response = requests.get(current_url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            all_data.extend(data)
            print(f"Loaded {len(data)} rows, total rows: {len(all_data)}")
            temp_df = pd.DataFrame(data)
            df = pd.concat([df, temp_df], ignore_index=True)
            
            temp_df = pd.DataFrame(data)
            temp_df['timestamp'] = temp_df['timestamp'].apply(convert_timestamp)
            df = pd.concat([df, temp_df], ignore_index=True)

            print(df.tail(5))

            print(f"Current end_timestamp: {end_timestamp}")
            earliest_timestamp = data[-1]['timestamp']
            print(f"Earliest timestamp in batch: {earliest_timestamp}")
            if earliest_timestamp <= start_timestamp:
                print("Reached start_timestamp, breaking loop")
                break
            end_timestamp = earliest_timestamp - (500 * 300000)
            print(f"Updated end_timestamp for next request: {end_timestamp}")
        else:
            print(f"Request failed with status code {response.status_code}")
            print(f"Failed URL: {current_url}")
            break

    return all_data

# URL for the Binance API
url = "https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=5m"

# Define the start date
start_date = "2023-11-14"

# Fetch data
data = fetch_data(url, start_date)

# Create DataFrame and convert timestamp
if data:
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    print(f"Total rows retrieved: {len(df)}")
else:
    print("No data retrieved.")

import requests, csv
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = 'AFG1UCT1UGMCYXJ8'

time_str_lower = '01/03/2022' # Desired starting date
time_obj_lower = datetime.strptime(time_str_lower, '%d/%m/%Y') # Assign time to datetime object
time_str_formatted_lower = time_obj_lower.strftime('%Y-%m-%d') # Alpha Vantage timestamp pattern conversion

time_str_upper = '01/10/2022' # Desired ending date
time_obj_upper = datetime.strptime(time_str_upper, '%d/%m/%Y') # Assign time to datetime object 
time_str_formatted_upper = time_obj_upper.strftime('%Y-%m-%d') # Alpha Vantage timestamp pattern conversion

STOCK_NAME = 'AAPL' # Apple stock name

history_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={STOCK_NAME}&apikey={API_KEY}&datatype=csv'

response = requests.get(history_url) # API call

if response.status_code == 200: # Call successful
    content = response.content.decode('utf-8') # Decode API response content
    reader = csv.DictReader(content.splitlines()) # Read the csv

    data = [row for row in reader] # Save all stock data in a list
    filtered_data = [row for row in data if time_str_formatted_lower <= row['timestamp'] <= time_str_formatted_upper] # Stock date filtration

    with open("./filtered_stock.csv", "w", newline='') as stock: # Save the filtered stock data in a local csv file
        fieldnames = ['timestamp', 'open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount']
        writer = csv.DictWriter(stock, fieldnames=fieldnames) # Write to csv
        writer.writeheader() # 1st row will contain the 'fieldnames'
        writer.writerows(filtered_data) # Write the filtered list data accordingly
    
    print(filtered_data, end="\n\n")
    print(f"Filtered {len(filtered_data)}/{len(data)} total '{STOCK_NAME}' stock data between {time_str_lower} - {time_str_upper}.")
else: # Call unsuccessful
    print(f'Request failed with status code {response.status_code}')

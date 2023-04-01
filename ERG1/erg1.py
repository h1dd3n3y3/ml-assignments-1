import requests, csv
from datetime import datetime

API_KEY = 'AFG1UCT1UGMCYXJ8'

time_str_lower = '01/03/2022' # Desired starting date
time_obj_lower = datetime.strptime(time_str_lower, '%d/%m/%Y')
time_str_formatted_lower = time_obj_lower.strftime('%Y-%m-%d') # Alpha Vantage timestamp pattern standard conversion

time_str_upper = '01/10/2022' # Desired ending date
time_obj_upper = datetime.strptime(time_str_upper, '%d/%m/%Y')
time_str_formatted_upper = time_obj_upper.strftime('%Y-%m-%d') # Alpha Vantage timestamp pattern standard conversion

STOCK_NAME = 'AAPL' # Apple stock name

history_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={STOCK_NAME}&apikey={API_KEY}&datatype=csv'

response = requests.get(history_url) # API call

if response.status_code == 200: # Call successful
    content = response.content.decode('utf-8') # Response content decoding
    
    reader = csv.DictReader(content.splitlines()) # Read the csv
    data = [row for row in reader] # Save it in a list
    filtered_data = [row for row in data if time_str_formatted_lower <= row['timestamp'] <= time_str_formatted_upper] # Date filtration
    
    print(filtered_data)
    print("\nFiltered {len(filtered_data)} total {STOCK_NAME} stock data between {time_str_lower} - {time_str_upper}.")
else: # Call unsuccessful
    print(f'Request failed with status code {response.status_code}')

import requests, csv
from datetime import datetime

api_key = 'AFG1UCT1UGMCYXJ8'

time_str_lower = '01/03/2022'
time_obj_lower = datetime.strptime(time_str_lower, '%d/%m/%Y')
time_str_formatted_lower = time_obj_lower.strftime('%Y-%m-%d')

time_str_upper = '01/10/2022'
time_obj_upper = datetime.strptime(time_str_upper, '%d/%m/%Y')
time_str_formatted_upper = time_obj_upper.strftime('%Y-%m-%d')

STOCK_NAME = 'AAPL' # Apple stock name

history_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={STOCK_NAME}&apikey={api_key}&datatype=csv'

response = requests.get(history_url) # API call

if response.status_code == 200: # Request code check
    content = response.content.decode('utf-8') # Response content decoding
    
    reader = csv.DictReader(content.splitlines()) # Read the csv
    data = [row for row in reader] # Save it in a list
    
    # Filter the data to only include the date/time range
    filtered_data = [row for row in data if time_str_formatted_lower <= row['timestamp'] <= time_str_formatted_upper]
    
    print(filtered_data)
    print("\nFiltered {} total {} stock data between {} - {}.".format(len(filtered_data), STOCK_NAME, time_str_lower, time_str_upper))
else:
    # Print an error message if the request was not successful
    print(f'Request failed with status code {response.status_code}')

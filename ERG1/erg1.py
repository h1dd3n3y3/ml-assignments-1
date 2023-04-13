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

    # Define x and y axis references
    x = [data['timestamp'] for data in filtered_data]
    y_high = [float(data['high']) for data in filtered_data]
    y_low = [float(data['low']) for data in filtered_data]

    # Create plot
    fig, ax = plt.subplots()
    ax.plot(x, y_high, label='High')
    ax.plot(x, y_low, label='Low')

    # Set labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Stock Value')
    ax.set_title('Stock High and Low Values over Time')

    plt.xticks(rotation=20) # Rotate x-axis labels for better visibility
    fig.subplots_adjust(bottom=0.19) # Adjust spacing between subplots to make horizontal axis label visible

    ax.legend() # Element to define line colours and labels
    plt.show() # Display the plot
else: # Call unsuccessful
    print(f'Request failed with status code {response.status_code}')

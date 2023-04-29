import requests, csv, numpy as np, matplotlib.pyplot as plt
from datetime import datetime

def calc_regression_coef(x, y):
    n = np.size(x) # number of observations/points

    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # calculating cross-deviation of y and x and the sum of squared deviations of x
    SS_xy = np.sum(x * y) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return (b_0, b_1)

def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color="m", marker="o", s=30)

    # predicted response vector
    y_pred = b[0] + b[1] * x

    # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    plt.xlabel('Month lapse')
    plt.ylabel(f'{STOCK_NAME} stock value')

    # function to show plot
    plt.show()

API_KEY = 'AFG1UCT1UGMCYXJ8' # Alpha Vantage API Key
STOCK_NAME = 'AAPL' # Apple stock name
DATASET_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={STOCK_NAME}&apikey={API_KEY}&datatype=csv' # Alpha Vantage monthly adjusted url

time_str_lower = '01/03/2021' # Desired starting date
time_obj_lower = datetime.strptime(time_str_lower, '%d/%m/%Y') # Assign time to datetime object
time_str_formatted_lower = time_obj_lower.strftime('%Y-%m-%d') # Alpha Vantage timestamp pattern conversion

time_str_upper = '01/03/2023' # Desired ending date
time_obj_upper = datetime.strptime(time_str_upper, '%d/%m/%Y') # Assign time to datetime object 
time_str_formatted_upper = time_obj_upper.strftime('%Y-%m-%d') # Alpha Vantage timestamp pattern conversion

response = requests.get(DATASET_URL) # API call

if response.status_code == 200: # Call successful
    content = response.content.decode('utf-8') # Decode API response content
    reader = csv.DictReader(content.splitlines()) # Read the decoded csv response content

    data = [row for row in reader] # Save all stock data in a list
    filtered_data = [row for row in data if time_str_formatted_lower <= row['timestamp'] <= time_str_formatted_upper] # Stock date filtration
    filtered_data.reverse() # Reverse alpha vantage api request list (originally returns data from present(or future) to past datetimes)

    #! optional
    with open("./filtered_stock.csv", "w", newline='') as stock: # Save the filtered stock data in a local csv file
        fieldnames = ['timestamp', 'open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount']
        writer = csv.DictWriter(stock, fieldnames=fieldnames) # Write to csv
        writer.writeheader() # 1st row will contain the 'fieldnames'
        writer.writerows(filtered_data) # Write the filtered list data accordingly
    
    print(filtered_data, end="\n\n")
    print(f"Filtered {len(filtered_data)}/{len(data)} total '{STOCK_NAME}' stock data between {time_str_lower} - {time_str_upper}.")

    # Define x and y axis references
    date = [data['timestamp'] for data in filtered_data]
    print("date:", date)
    x = [int(month[5:7]) for month in date]
    print("x:", x)

    high = [float(data['high']) for data in filtered_data]
    print("high:", high)
    low = [float(data['low']) for data in filtered_data]
    print("low:", low)
    y = [round(high[i] + low[i] / 2, 2) for i in range(len(high))] # Keep the 2 decimal digits because python is stupid
    print("y:",y)

    b = calc_regression_coef(np.array(x), np.array(y))
    print("Estimated coefficients:\nb_0 = {}\nb_1 = {}".format(b[0], b[1]))

    plot_regression_line(np.array(x), np.array(y), b) # Plot regression line
else: # Call unsuccessful
    print(f'Request failed with status code {response.status_code}')

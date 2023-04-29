import requests, csv, numpy as np, matplotlib.pyplot as plt, os
from datetime import datetime

def calc_regression_coef(x, y):
    n = np.size(x) # Number of observations/points

    # Mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # Calculating cross-deviation of y and x and the sum of squared deviations of x
    SS_xy = np.sum(x * y) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # Calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return (round(b_0, 2), round(b_1, 2)) # 2 decimal digit limitation

def plot_regression_line(x, y, b):
    plt.scatter(x, y, color="m", marker="o", s=30) # Plotting the actual points as scatter plot
    y_pred = b[0] + b[1] * x # Predicted response vector
    plt.plot(x, y_pred, color="g") # Plotting the regression line

    # Putting labels
    plt.xlabel('Month lapse')
    plt.ylabel(f'{STOCK_NAME} Stock value')

    plt.show() # Show plot

def alpha_vantage_date_format_convertion(d_m_y_format):
    date_obj = datetime.strptime(d_m_y_format, '%d/%m/%Y') # Assign time to datetime object

    return date_obj.strftime('%Y-%m-%d'), d_m_y_format # Alpha Vantage timestamp pattern conversion

def stock_prediction_formula(b_0, b_1, x_i):
    return round(b_0 + b_1 * x_i, 2) # 2 decimal digit limitation

API_KEY = 'AFG1UCT1UGMCYXJ8' # Alpha Vantage API Key
STOCK_NAME = 'AAPL' # Apple stock name
DATASET_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={STOCK_NAME}&apikey={API_KEY}&datatype=csv' # Alpha Vantage monthly adjusted url

# Desired date limits for the data set (old data)
date_lower_0 = alpha_vantage_date_format_convertion('01/01/2020') # Starting date
date_upper_0 = alpha_vantage_date_format_convertion('01/01/2021') # Ending date

while 1:
    # Desired date limits for future prediction (currently present)
    date_lower_1 = alpha_vantage_date_format_convertion("01/11/2022") # Starting date >= past ending date
    date_upper_1 = alpha_vantage_date_format_convertion("01/04/2023") # Ending date <= 1 month before the current program execution month

    response = requests.get(DATASET_URL) # API call

    if response.status_code == 200: # Call successful
        content = response.content.decode('utf-8') # Decode API response content
        reader = csv.DictReader(content.splitlines()) # Read decoded csv response content
        data = [row for row in reader] # Save all stock data in a list


        # Setting up the data set base
        filtered_past_data = [row for row in data if date_lower_0[0] <= row['timestamp'] <= date_upper_0[0]] # Stock date filtration
        filtered_past_data.reverse() # Reverse alpha vantage api request list (originally returns data from present(or future) to past datetimes)

        print(filtered_past_data, end="\n\n")
        print(f"Filtered {len(filtered_past_data)}/{len(data)} total '{STOCK_NAME}' stock data between {date_lower_0[1]} - {date_upper_0[1]}.")

        # Define x and y axis references
        date_past = [data['timestamp'] for data in filtered_past_data]
        print("date_past:", date_past)
        month_past = [int(month[5:7]) for month in date_past]
        print("month_past:", month_past)

        # Calculate stock's value using stock's 'high' & 'low' mean
        high_old = [float(data['high']) for data in filtered_past_data]
        print("high_old:", high_old)
        low_old = [float(data['low']) for data in filtered_past_data]
        print("low_old:", low_old)
        stock_value_old = [round(high_old[i] + low_old[i] / 2, 2) for i in range(len(high_old))] # Keep the 2 decimal digits because pstock_value_oldthon is stupid
        print("stock_value_old:", stock_value_old)

        b = calc_regression_coef(np.array(month_past), np.array(stock_value_old)) # Calculate b_0 & b_1 regression coefficients
        print("Estimated coefficients:\nb_0 = {}\nb_1 = {}".format(b[0], b[1]), end="\n\n")

        plot_regression_line(np.array(month_past), np.array(stock_value_old), b) # Plot regression line


        # Setting up the 'future' data set reference
        filtered_future_data = [row for row in data if date_lower_1[0] <= row['timestamp'] <= date_upper_1[0]] # Stock date filtration
        filtered_future_data.reverse() # Reverse alpha vantage api request list (originally returns data from present(or future) to past datetimes)

        print(filtered_future_data, end="\n\n")
        print(f"Filtered {len(filtered_future_data)}/{len(data)} total '{STOCK_NAME}' stock data between {date_lower_1[1]} - {date_upper_1[1]}.")
        
        date_future = [data['timestamp'] for data in filtered_future_data]
        print("date_future:", date_future)
        month_future = [int(month[5:7]) for month in date_future]
        print("month_future:", month_future)

        # Calculate stock's value using stock's 'high' & 'low' mean
        high_new = [float(data['high']) for data in filtered_past_data]
        print("high_new:", high_new)
        low_new = [float(data['low']) for data in filtered_past_data]
        print("low_new:", low_new)
        stock_value_new = [round(high_new[i] + low_new[i] / 2, 2) for i in range(len(high_new))] # Keep the 2 decimal digits because pstock_value_oldthon is stupid
        print("stock_value_old:", stock_value_new)

        predicted_stock_values = []
        for m in range(len(month_future)):
            predicted_stock_values.append(stock_prediction_formula(b[0], b[1], m)) # Predict stock values

        print("Predicted stock values:", predicted_stock_values, end="\n\n")

        common_months = []
        for month in month_future:
            if month in month_past:
                common_months.append(month)

        for j in common_months: # Print error between real and predicted stock value
            print(f'Prediction error for {date_future[common_months.index(j)]}: {round(abs(stock_value_old[month_past.index(j)] - predicted_stock_values[month_future.index(j)]), 2)}') # 2 decimal digit limitation
        
        while (ans := input("Continue predictions for new dates? (yes/no): ")) not in ["yes", "no"]:
            print("Wrong input: choose between 'yes' and 'no':")

        if ans == "no":
            break

        os.system("cls") # Clear windows terminal content
    else: # Call unsuccessful
        print(f'Request failed with status code {response.status_code}')

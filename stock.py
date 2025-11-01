import mplfinance as mpf
import yfinance as yf 
import pandas as pd
import os

# Define the stock symbol if available in yfinance
while True:
    stock_ticker = input("Ticker ").upper()
# Identify the ticker that is inputed
    ticker = yf.Ticker(stock_ticker)
    checker = ticker.history(period="5d")
# Check if the dataFrame is empty in the ticker being called by user
    if checker.empty:
        print(f"❌ The ticker {stock_ticker} is NOT available on Yahoo Finance 📊. Try again")
    else:
        break

# Include the date range for the stock data
start_date = input("What start time (year-month-day): ")
end_date = input("What end time (year-month-day): ")

# Quick testing dates
# start_date = "2025-01-04"
# end_date = "2025-02-03"

# Clearing csv files in data folder for organization purposes
file = "/Users/fengs/Downloads/Programming-folder/stock-tracker/data/"+ stock_ticker + ".csv"
folder_path = "/Users/fengs/Downloads/Programming-folder/stock-tracker/data/"

# Checking out the file in the folder path if there is file in there and deleting
# it if it's a file or a symbolic link
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Load historical data
stock_data = yf.download(stock_ticker, start=start_date, end=end_date)

# Load your stock data, skipping row 1,2 and replacing 'Price' with 'Date'
# in order to run matplot candle stick grapth
stock_data.to_csv(file, index_label='Date')
stock_data = pd.read_csv(file, skiprows=(1,2))
stock_data.rename(columns={stock_data.columns[0]: "Date"}, inplace=True)

# # Convert to datetime and set index
stock_data['Date'] = pd.to_datetime(stock_data['Date'])
stock_data.set_index('Date', inplace=True)

# # Ensure numeric columns, safety pin to test if they are integers or float value
cols = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in cols:
    stock_data[col] = pd.to_numeric(stock_data[col], errors='coerce')

stock_data.dropna(subset=cols, inplace=True)

# Plot graph and show data in terminal
print(stock_data)
mpf.plot(stock_data, type='candle')

import mplfinance as mpf
import yfinance as yf 
import pandas as pd

# Define the stock symbol and date range
stock_symbol = "AAPL"
start_date = "2022-01-01"
end_date = "2022-01-07"

#clearing files
file = "/Users/fengs/Downloads/Programming-folder/stock-tracker/data/"+ stock_symbol + ".csv"

# Load historical data
stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
# Load your stock data
stock_data.to_csv('data/test.csv', index_label='Date')
stock_data = pd.read_csv('data/test.csv', skiprows=(1,2))
stock_data.rename(columns={stock_data.columns[0]: "Date"}, inplace=True)

# # Convert to datetime and set index
stock_data['Date'] = pd.to_datetime(stock_data['Date'])
stock_data.set_index('Date', inplace=True)

# # Ensure numeric columns, safety pin to test if they are integers or float value
cols = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in cols:
    stock_data[col] = pd.to_numeric(stock_data[col], errors='coerce')

stock_data.dropna(subset=cols, inplace=True)

# Plot
mpf.plot(stock_data, type='candle')
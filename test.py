import yfinance as yf 
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas_ta as ta
# import plotly.express as px
import os

# # Define the stock symbol if available in yfinance
# while True:
#     stock_ticker = input("Ticker ").upper()
# # Identify the ticker that is inputed
#     ticker = yf.Ticker(stock_ticker)
#     checker = ticker.history(period="5d")
# # Check if the dataFrame is empty in the ticker being called by user
#     if checker.empty:
#         print(f"❌ The ticker {stock_ticker} is NOT available on Yahoo Finance 📊. Try again")
#     else:
#         break

stock_ticker = "aapl"

# Include the date range for the stock data
# start_date = input("What start time (year-month-day): ")
# end_date = input("What end time (year-month-day): ")

# Quick testing dates
start_date = "2024-1-04"
end_date = "2025-1-20"

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
rsi = stock_data.ta.rsi()
if isinstance(rsi, pd.DataFrame):
    rsi = rsi.iloc[:, 0]
stock_data["RSI"] = rsi

rsi_plot = mpf.make_addplot(
    stock_data["RSI"], 
    panel = 1,      # 0 = main panel (the candle graph chart), 1 = new lower panel (by itself)
    color = 'purple',
    ylabel = 'RSI'
)
binance_dark = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "#3dc985", "down": "#ef4f60"},  
        "edge": {"up": "#3dc985", "down": "#ef4f60"},  
        "wick": {"up": "#3dc985", "down": "#ef4f60"},  
        "ohlc": {"up": "green", "down": "red"},
        "volume": {"up": "#247252", "down": "#82333f"},  
        "vcedge": {"up": "green", "down": "red"},  
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("#D3AF37", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#ffffff",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "binance-dark",
}

# stock = mpf.plot(
#     stock_data,
#     type='candle',
#     style=binance_dark,
#     title=f"{stock_ticker} with RSI",
#     addplot=rsi_plot,
#     volume=True,
#     panel_ratios=(3.,1),     # main panel : RSI panel height ratio
#     tight_layout=False, 
#     mav=(2, 4, 6),
#     figscale=1.2
# )

fig, axes = mpf.plot(
    stock_data,
    type='candle',
    style=binance_dark,
    title=f"{stock_ticker} with RSI",
    addplot=rsi_plot,
    volume=True,
    panel_ratios=(3.,1),
    tight_layout=False, 
    mav=(2, 4, 6),
    figscale=1.2,
    returnfig=True 
)



orig_limits = {a: a.get_xlim() for a in axes}
base_scale = 1.1

def zoom(event):
    ax = event.inaxes
    if ax is None:
        return
    # scale
    if event.button == "up":      # zoom in
        scale_factor = 1 / base_scale
    elif event.button == "down":  # zoom out
        scale_factor = base_scale
    else:
        return

    # get current limits
    x_left, x_right = ax.get_xlim()
    xdata = event.xdata
    if xdata is None:
        return

    # compute new limits
    new_left  = xdata - (xdata - x_left) * scale_factor
    new_right = xdata + (x_right - xdata) * scale_factor

    # ---- LIMITER: prevent zooming out beyond the original full range ----
    orig_left, orig_right = orig_limits[ax]

    # Clamp values so they don’t go outside the original
    if new_left < orig_left:
        new_left = orig_left
    if new_right > orig_right:
        new_right = orig_right

    # Also prevent flipping limits if user tries extreme zoom-out
    if (new_right - new_left) >= (orig_right - orig_left):
        new_left, new_right = orig_left, orig_right

    ax.set_xlim(new_left, new_right)
    fig.canvas.draw_idle()

# Connect the event
fig.canvas.mpl_connect("scroll_event", zoom)

plt.show()
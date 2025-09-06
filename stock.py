import yfinance as yf
import os


# Make sure data folder exists
os.makedirs("data", exist_ok=True)

# Download stock data (Apple as example)
data = yf.download("AAPL", start="2025-09-05")
print(data.head())

# Save to CSV
data.to_csv("data/AAPL_2022_2024.csv")
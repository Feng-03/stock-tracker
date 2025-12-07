from scipy import stats
import pandas as pd
import yfinance as yf 
import numpy as np
import datetime as dt
import glob
import os

stock_count = int(input("Enter the number of stocks in your portfolio: "))
folder_path = "/Users/fengs/Downloads/Programming-folder/stock-tracker/data/"

# Ask for tickers and download data
for i in range(stock_count):
    while True:
        stock_ticker = input(f"Ticker {i+1}: ").upper()
        ticker = yf.Ticker(stock_ticker)
        checker = ticker.history(period="5d")
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        if checker.empty:
            print(f"❌ The ticker {stock_ticker} is NOT available on Yahoo Finance. Try again.")
        else:
            file = folder_path + stock_ticker + ".csv"
            start_date = dt.datetime.now() - dt.timedelta(days=800)
            end_date = dt.datetime.now()
            
            stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
            stock_data.to_csv(file, index_label='Date')
            print(f"✅ {stock_ticker} data downloaded and saved.")
            break


time_horizon = int(input("Enter how long stock(s) is placed for in day(s): "))
alpha_interval = float(input("Enter the confidence level (example: 5 for 95% VaR): "))
initial_investment = float(input("Enter the initial investment amount ($): "))


def getData(folder, start, end):
    stockData = pd.DataFrame()
    csv_files = glob.glob(f"{folder}/*.csv")

    for file in csv_files:
        ticker = file.split("/")[-1].replace(".csv", "").upper()
        df = pd.read_csv(file)

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date")
            df = df.loc[start:end]

        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        stockData[ticker] = df["Close"]

    returns = stockData.pct_change().dropna()
    meanReturns = returns.mean()
    covMatrix = returns.cov()

    return returns, meanReturns, covMatrix


def portfolioPerformance(weights, meanReturns, covMatrix, time_horizon):
    returns = np.sum(meanReturns * weights) * time_horizon
    std = np.sqrt(np.dot(weights.T, np.dot(covMatrix, weights))) * np.sqrt(time_horizon)
    return returns, std


def historicalVaR(returns, alpha):
    if isinstance(returns, pd.Series):
        return np.percentile(returns, alpha)
    return returns.aggregate(historicalVaR, alpha=alpha)


def historicalCVaR(returns, alpha):
    if isinstance(returns, pd.Series):
        var = historicalVaR(returns, alpha)
        belowVaR = returns <= var
        return returns[belowVaR].mean()
    return returns.aggregate(historicalCVaR, alpha=alpha)


startDate = dt.datetime.now() - dt.timedelta(days=800)
endDate = dt.datetime.now()

returns, meanReturns, covMatrix = getData(folder_path, startDate, endDate)
returns = returns.dropna()

# Random portfolio weights
weights = np.random.random(len(returns.columns))
weights /= np.sum(weights)

# Portfolio returns
returns["portfolio"] = returns.dot(weights)

# VaR & CVaR
hVaR = -historicalVaR(returns["portfolio"], alpha_interval) * np.sqrt(time_horizon)
hCVaR = -historicalCVaR(returns["portfolio"], alpha_interval) * np.sqrt(time_horizon)

# Expected portfolio return & std deviation
pRet, pStd = portfolioPerformance(weights, meanReturns, covMatrix, time_horizon)


print("\n--- Portfolio Risk Analysis ---")
print("Expected Portfolio Return:      $", round(initial_investment * pRet, 2))
print("Value at Risk (VaR):            $", round(initial_investment * hVaR, 2))
print("Conditional VaR (CVaR):         $", round(initial_investment * hCVaR, 2))

# Daily portfolio returns
portfolio_returns = returns["portfolio"]

# Perform one-sample t-test against mean = 0
t_stat, p_value = stats.ttest_1samp(portfolio_returns, 0)

print("\n--- Hypothesis Test on Portfolio Returns ---")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4e}")

if p_value < 0.05:
    print("Conclusion: Reject the null hypothesis — portfolio returns differ significantly from zero.")
else:
    print("Conclusion: Fail to reject the null hypothesis — no significant evidence of non-zero portfolio returns.")
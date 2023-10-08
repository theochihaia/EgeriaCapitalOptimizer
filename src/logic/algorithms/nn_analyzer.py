#from src.third_party.yahoo_finance import pull_general_data, pull_pricing_data

import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import concurrent.futures

import requests_cache
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
from pandas_datareader import data as pdr

# from src.common.configuration.metric_config import get_variance, get_income_growth


"""
    TODO: PUT THIS IN COMMON

    Current Issues:
    RMSE is too high
    Target prediction is not what is needed. We want to predict equities that would perform well over 10 years
    The Egeria rank is used as a sorting mechanism not a target. NN isn't approriate here
    Likley should create a manual portfolio, rank by manual labels
    Use this to generate model
    Need paralelization of pulling data.
"""

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


session = CachedLimiterSession(
    limiter=Limiter(
        RequestRate(10, Duration.SECOND * 2)
    ),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache", expire_after=86400),# 1 day
)

session = requests_cache.CachedSession("yfinance.cache")
session.headers["User-agent"] = "my-program/1.0"

yf.pdr_override()


def get_ticker(symbol: str):
    return yf.Ticker(symbol, session=session)

def pull_general_data(symbol_list: list):
    data = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_ticker, symbol): symbol for symbol in symbol_list}
        for future in concurrent.futures.as_completed(futures):
            symbol = futures[future]
            try:
                data[symbol] = future.result()
            except Exception as e:
                print(f"Failed to pull data for {symbol}. Reason: {e}")
    return data


def get_income_growth(ticker: yf.Ticker, data_point: str):
    data = []
    for key, value in ticker.get_income_stmt().items():
        data.append(value.get(data_point))

    if len(data) < 2:
        return None

    avgGrowthRate = 0
    for i in range(len(data) - 1):
        if data[i + 1] is None or data[i] is None:
            continue
        avgGrowthRate += (data[i] - data[i + 1]) / data[i + 1]

    avgGrowthRate /= len(data) - 1
    return avgGrowthRate * 100


def get_n_day_returns(data_close, days):
    five_day_returns = []
    for i in range(0, len(data_close) - days, days):
        if (
            data_close.iloc[i + days] is None
            or data_close.iloc[i] is None
            or data_close.iloc[i] == 0
        ):
            continue
        five_day_returns.append(
            (data_close.iloc[i + days] - data_close.iloc[i]) / data_close.iloc[i]
        )
    return five_day_returns


def get_variance(ticker: yf.Ticker, period: str):
    data = ticker.history(period=period)
    day_period = 10
    data_close = data["Close"]
    if data.empty:
        return

    n_day_returns = get_n_day_returns(data_close, day_period)
    if len(n_day_returns) == 0:
        return None

    variance = np.var(n_day_returns)
    return variance * 100


def get_return(ticker: yf.Ticker, period: str):
    data = ticker.history(period=period)
    if data.empty:
        return

    latest_price = data["Close"].iloc[-1]
    initial_price = data["Close"].iloc[0]
    return (latest_price - initial_price) / initial_price * 100

def get_data_frame(data: list):
    return pd.DataFrame(
        data,
        columns=[
            "P/E",
            "P/S",
            "Quick Ratio",
            "Beta",
            "Dividend Yield",
            "EBITDA Margin",
            "Trailing P/E",
            "P/B",
            "5 Year Variance",
            "10 Year Variance",
            "3 Year EBITDA Growth",
            "3 Year Revenue Growth",
            "5 Year Return",
            "10 Year Return",
        ])

def fetch_stock_data(tickers: list):
    all_stock_data = []
    data = pull_general_data(tickers)
    for sym, yf_data in data.items():
        stock = yf_data
        info = stock.get_info()
        all_stock_data.append([
            info.get("forwardPE") or None,
            info.get("priceToSalesTrailing12Months") or None,
            info.get("quickRatio") or None,
            info.get("beta") or None,
            info.get("fiveYearAvgDividendYield") or None,
            info.get("ebitdaMargins") or None,
            info.get("trailingPE") or None,
            info.get("priceToBook") or None,
            get_variance(stock, "5y") or None,
            get_variance(stock, "10y") or None,
            get_income_growth(stock, "NormalizedEBITDA") or None,
            get_income_growth(stock, "TotalRevenue") or None,
            get_return(stock, "5y") or None,
            get_return(stock, "10y") or None,
        ])

    return all_stock_data

# Data Collection
dir = f"src/common/portfolios/scores/sp500.txt"
with open(dir) as f:
    score_input = f.read().splitlines()
    symbols = [ticker.split(",")[0] for ticker in score_input]


# ['AAPL', 'GOOGL', 'MSFT']  # Add your tickers here
data = fetch_stock_data(symbols)

df = get_data_frame(data)

# Generate your targets here (the ranks). This is a placeholder:
df["Target"] = [ticker.split(",")[1] for ticker in score_input]  # Or however you want to rank them
df.dropna(inplace=True)

# Data Preprocessing
X = df.drop("Target", axis=1)
y = df["Target"]

print(X.shape)
print(X.head())


# Impute missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.3, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Neural Network Design and Training
model = MLPRegressor(hidden_layer_sizes=(500, 500), max_iter=3000, activation='relu', solver='adam', alpha=0.0003, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Predictions for new data (here we're just using X_test as an example)
predictions = model.predict(X_test)

for ticker, pred, actual in zip(symbols, predictions, y_test):
    print(f"Ticker: {ticker}, Prediction: {pred}, Actual: {actual}")


# Generate Predictions for new data

dir = f"src/common/portfolios/fid_folio_v2.txt"
with open(dir) as f:
    new_symbols = f.read().splitlines()

new_data = []
new_data = fetch_stock_data(new_symbols)

new_df = get_data_frame(new_data)

# Handle missing values
new_data_imputed = imputer.transform(new_df)

# Scale the data
new_data_scaled = scaler.transform(new_data_imputed)

new_predictions = model.predict(new_data_scaled)

for ticker, prediction in zip(new_symbols, new_predictions):
    print(f"Ticker: {ticker}, Prediction: {prediction}")


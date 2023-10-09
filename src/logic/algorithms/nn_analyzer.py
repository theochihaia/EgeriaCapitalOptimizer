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
    backend=SQLiteCache("yfinance.cache", expire_after=432000), # 5 days
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
            "auditRisk",
            "boardRisk",
            "compensationRisk",
            "shareHolderRightsRisk",
            "overallRisk",
            "governanceEpochDate",
            "compensationAsOfEpochDate",
            "maxAge",
            "priceHint",
            "previousClose",
            "open",
            "dayLow",
            "dayHigh",
            "regularMarketPreviousClose",
            "regularMarketOpen",
            "regularMarketDayLow",
            "regularMarketDayHigh",
            "dividendRate",
            "dividendYield",
            "exDividendDate",
            "payoutRatio",
            "fiveYearAvgDividendYield",
            "beta",
            "trailingPE",
            "forwardPE",
            "volume",
            "regularMarketVolume",
            "averageVolume",
            "averageVolume10days",
            "averageDailyVolume10Day",
            "bid",
            "ask",
            "bidSize",
            "askSize",
            "marketCap",
            "fiftyTwoWeekLow",
            "fiftyTwoWeekHigh",
            "priceToSalesTrailing12Months",
            "fiftyDayAverage",
            "twoHundredDayAverage",
            "trailingAnnualDividendRate",
            "trailingAnnualDividendYield",
            "enterpriseValue",
            "profitMargins",
            "floatShares",
            "sharesOutstanding",
            "sharesShort",
            "sharesShortPriorMonth",
            "sharesShortPreviousMonthDate",
            "dateShortInterest",
            "sharesPercentSharesOut",
            "heldPercentInsiders",
            "heldPercentInstitutions",
            "shortRatio",
            "shortPercentOfFloat",
            "impliedSharesOutstanding",
            "bookValue",
            "priceToBook",
            "lastFiscalYearEnd",
            "nextFiscalYearEnd",
            "mostRecentQuarter",
            "earningsQuarterlyGrowth",
            "netIncomeToCommon",
            "trailingEps",
            "forwardEps",
            "pegRatio",
            "lastSplitDate",
            "enterpriseToRevenue",
            "enterpriseToEbitda",
            "52WeekChange",
            "SandP52WeekChange",
            "lastDividendValue",
            "lastDividendDate",
            "firstTradeDateEpochUtc",
            "currentPrice",
            "targetHighPrice",
            "targetLowPrice",
            "targetMeanPrice",
            "targetMedianPrice",
            "recommendationMean",
            "numberOfAnalystOpinions",
            "totalCash",
            "totalCashPerShare",
            "ebitda",
            "totalDebt",
            "quickRatio",
            "currentRatio",
            "totalRevenue",
            "debtToEquity",
            "revenuePerShare",
            "returnOnAssets",
            "returnOnEquity",
            "grossProfits",
            "freeCashflow",
            "operatingCashflow",
            "earningsGrowth",
            "revenueGrowth",
            "grossMargins",
            "ebitdaMargins",
            "operatingMargins",
            "trailingPegRatio",
            "5yrGrowth",
            "10yrGrowth",
            #"NormalizedEBITDA",
            #"TotalRevenue"
        ])

def fetch_stock_data(tickers: list):
    all_stock_data = []
    data = pull_general_data(tickers)
    for sym, yf_data in data.items():
        stock = yf_data
        info = stock.get_info()
        all_stock_data.append([
            info.get("auditRisk", None),
            info.get("boardRisk", None),
            info.get("compensationRisk", None),
            info.get("shareHolderRightsRisk", None),
            info.get("overallRisk", None),
            info.get("governanceEpochDate", None),
            info.get("compensationAsOfEpochDate", None),
            info.get("maxAge", None),
            info.get("priceHint", None),
            info.get("previousClose", None),
            info.get("open", None),
            info.get("dayLow", None),
            info.get("dayHigh", None),
            info.get("regularMarketPreviousClose", None),
            info.get("regularMarketOpen", None),
            info.get("regularMarketDayLow", None),
            info.get("regularMarketDayHigh", None),
            info.get("dividendRate", None),
            info.get("dividendYield", None),
            info.get("exDividendDate", None),
            info.get("payoutRatio", None),
            info.get("fiveYearAvgDividendYield", None),
            info.get("beta", None),
            info.get("trailingPE", None),
            info.get("forwardPE", None),
            info.get("volume", None),
            info.get("regularMarketVolume", None),
            info.get("averageVolume", None),
            info.get("averageVolume10days", None),
            info.get("averageDailyVolume10Day", None),
            info.get("bid", None),
            info.get("ask", None),
            info.get("bidSize", None),
            info.get("askSize", None),
            info.get("marketCap", None),
            info.get("fiftyTwoWeekLow", None),
            info.get("fiftyTwoWeekHigh", None),
            info.get("priceToSalesTrailing12Months", None),
            info.get("fiftyDayAverage", None),
            info.get("twoHundredDayAverage", None),
            info.get("trailingAnnualDividendRate", None),
            info.get("trailingAnnualDividendYield", None),
            info.get("enterpriseValue", None),
            info.get("profitMargins", None),
            info.get("floatShares", None),
            info.get("sharesOutstanding", None),
            info.get("sharesShort", None),
            info.get("sharesShortPriorMonth", None),
            info.get("sharesShortPreviousMonthDate", None),
            info.get("dateShortInterest", None),
            info.get("sharesPercentSharesOut", None),
            info.get("heldPercentInsiders", None),
            info.get("heldPercentInstitutions", None),
            info.get("shortRatio", None),
            info.get("shortPercentOfFloat", None),
            info.get("impliedSharesOutstanding", None),
            info.get("bookValue", None),
            info.get("priceToBook", None),
            info.get("lastFiscalYearEnd", None),
            info.get("nextFiscalYearEnd", None),
            info.get("mostRecentQuarter", None),
            info.get("earningsQuarterlyGrowth", None),
            info.get("netIncomeToCommon", None),
            info.get("trailingEps", None),
            info.get("forwardEps", None),
            info.get("pegRatio", None),
            info.get("lastSplitDate", None),
            info.get("enterpriseToRevenue", None),
            info.get("enterpriseToEbitda", None),
            info.get("52WeekChange", None),
            info.get("SandP52WeekChange", None),
            info.get("lastDividendValue", None),
            info.get("lastDividendDate", None),
            info.get("firstTradeDateEpochUtc", None),
            info.get("currentPrice", None),
            info.get("targetHighPrice", None),
            info.get("targetLowPrice", None),
            info.get("targetMeanPrice", None),
            info.get("targetMedianPrice", None),
            info.get("recommendationMean", None),
            info.get("numberOfAnalystOpinions", None),
            info.get("totalCash", None),
            info.get("totalCashPerShare", None),
            info.get("ebitda", None),
            info.get("totalDebt", None),
            info.get("quickRatio", None),
            info.get("currentRatio", None),
            info.get("totalRevenue", None),
            info.get("debtToEquity", None),
            info.get("revenuePerShare", None),
            info.get("returnOnAssets", None),
            info.get("returnOnEquity", None),
            info.get("grossProfits", None),
            info.get("freeCashflow", None),
            info.get("operatingCashflow", None),
            info.get("earningsGrowth", None),
            info.get("revenueGrowth", None),
            info.get("grossMargins", None),
            info.get("ebitdaMargins", None),
            info.get("operatingMargins", None),
            info.get("trailingPegRatio", None),
            get_return(stock, "5y") or None,
            get_return(stock, "10y") or None,
            #all_stock_data.append(get_income_growth(stock, "NormalizedEBITDA") or None),
            #all_stock_data.append(get_income_growth(stock, "TotalRevenue") or None)
        ])

    return all_stock_data

# Data Collection
dir = f"src/common/portfolios/scores/sp500.txt"
with open(dir) as f:
    score_input = f.read().splitlines()
    symbols = [ticker.split(",")[1] for ticker in score_input]


# ['AAPL', 'GOOGL', 'MSFT']  # Add your tickers here
data = fetch_stock_data(symbols)

df = get_data_frame(data)

# Generate your targets here (the ranks). This is a placeholder:
df["Target"] = [ticker.split(",")[2] for ticker in score_input]  # Or however you want to rank them
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
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Neural Network Design and Training
model = MLPRegressor(hidden_layer_sizes=(700, 700), max_iter=4000, activation='relu', solver='adam', alpha=0.03, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
#mse = mean_squared_error(y_test, y_pred)
#print(f"Mean Squared Error: {mse}")

# Predictions for new data (here we're just using X_test as an example)
predictions = model.predict(X_test)

for ticker, pred, actual in zip(symbols, predictions, y_test):
    print(f"Ticker: {ticker}, Prediction: {pred}, Actual: {actual}")


# Generate Predictions for new data

dir = f"src/common/portfolios/ijh_mid_cap.txt"
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
    print(f"Ticker,{ticker},Prediction,{prediction}")


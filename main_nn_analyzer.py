import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

from src.common.utils.ticker_util import get_symbols, get_income_growth, get_n_day_returns, get_return, get_std
from src.third_party.yahoo_finance import pull_general_data
from src.logic.algorithms.analyzers import analyze_tickers_concurrent
from src.common.configuration.app_config import *


FIELDS = [
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
    #"NormalizedEBITDA",
    #"TotalRevenue"
]

def get_data_frame(data: list):
    # Add calculated fields
    fields = FIELDS
    #fields.append("5yrGrowth")
    #fields.append("10yrGrowth")

    return pd.DataFrame(
        data,
        columns=fields)

def fetch_stock_data(data: dict):
    all_stock_data = []
    for sym, yf_data in data.items():
        stock = yf_data
        info = stock.get_info()

        # Append calculated fields
        row_data = [info.get(field, None) for field in FIELDS]
        #row_data.append(get_income_growth(stock, 5))
        #row_data.append(get_income_growth(stock, 10))
        all_stock_data.append(row_data)

    return all_stock_data

# Data Collection
symbols = get_symbols([Portfolio.FID_FOLIO])
buy_symbols = set(get_symbols([Portfolio.FID_FOLIO_V3])) #symbols to set target to 1
data_general = pull_general_data(symbols)
training_data = fetch_stock_data(data_general)
analysis = analyze_tickers_concurrent(data_general, ACTIVE_METRICS)

df = get_data_frame(training_data)

# Add all high egeria score symbols to buy list
for result in analysis:
    if result.egeria_score > 20:
        buy_symbols.add(result.symbol)

df["Target"] = [1 if symbol in buy_symbols else 0 for symbol in symbols] # Train on vetted symbols
#df.dropna(inplace=True)

# Print Empty Data
print(df[df.isna().any(axis=1)])


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
model = MLPRegressor(hidden_layer_sizes=(700, 700), max_iter=4000, activation='relu', solver='adam', alpha=0.03, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
y_pred = np.round(y_pred)
mse = mean_squared_error(y_test, y_pred)

mask = y_test != np.round(y_pred)
percent_error = ((y_test[mask] - y_pred[mask]) / y_test[mask]) * 100
print(f"Mean Squared Error: {mse}")
print(f"Percent Error: {percent_error}")

# Predictions for new data (here we're just using X_test as an example)
predictions = model.predict(X_test)
predictions = np.round(predictions)

for ticker, pred, actual in zip(symbols, predictions, y_test):
    print(f"Ticker: {ticker}, Prediction: {pred}, Actual: {actual}")


# Generate Predictions for new data

# new_symbols = get_symbols([Portfolio.IJH_MID_CAP])
# new_data_general = pull_general_data(symbols)
# new_data = fetch_stock_data(new_data_general)

# new_df = get_data_frame(new_data)
# new_df.dropna(inplace=True)

# # Handle missing values
# new_data_imputed = imputer.transform(new_df)

# # Scale the data
# new_data_scaled = scaler.transform(new_data_imputed)

# new_predictions = model.predict(new_data_scaled)

# for ticker, prediction in zip(new_symbols, new_predictions):
#     print(f"Ticker,{ticker},Prediction,{prediction}")


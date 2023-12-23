import yfinance as yf
import numpy as np
import pandas as pd
from src.common.configuration.app_config import STD_PERIOD_DAYS

from src.common.enums.portfolio import Portfolio

def get_return(ticker: yf.Ticker, period: str):
    data = ticker.history(period=period)
    if data.empty:
        return

    latest_price = data["Close"].iloc[-1]
    initial_price = data["Close"].iloc[0]
    return (latest_price - initial_price) / initial_price * 100


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
        if data_close.iloc[i + days] is None or data_close.iloc[i] is None or data_close.iloc[i] == 0:
            continue
        five_day_returns.append((data_close.iloc[i + days] - data_close.iloc[i]) / data_close.iloc[i])
    return five_day_returns


def get_std(ticker: yf.Ticker, period: str):
    data = ticker.history(period=period)
    day_period = STD_PERIOD_DAYS
    data_close = data["Close"]
    if data.empty:
        return

    n_day_returns = get_n_day_returns(data_close, day_period)
    if len(n_day_returns) == 0:
        return None
    
    variance = np.std(n_day_returns)
    return variance * 100


def get_symbols(symbol_set: Portfolio):
    symbols = set()
    for symbol in symbol_set:
        dir = f"src/common/portfolios/{symbol.value}.txt"
        with open(dir) as f:
            symbols.update(f.read().splitlines())
    return list(symbols)

def get_quick_ratio(ticker: yf.Ticker):
    #if(ticker.info):
    #    return ticker.info.get("quickRatio")

    latest_data = ticker.balance_sheet.iloc[:, 0]

    cash_equivalents = latest_data.get("Cash Cash Equivalents And Short Term Investments")
    accounts_receivable = latest_data.get("Receivables")
    current_liabilities = latest_data.get("Current Liabilities")

    quick_assets = float(cash_equivalents) + float(accounts_receivable)
    current_liabilities = float(current_liabilities)

    # Calculate the quick ratio
    quick_ratio = quick_assets / current_liabilities
    return quick_ratio

def get_debt_to_equity_ratio(ticker: yf.Ticker):
    #if ticker.info:
    #    return ticker.info.get("debtToEquity")

    latest_data = ticker.balance_sheet.iloc[:, 0]

    # Fetch total liabilities and total shareholder's equity
    total_liabilities = latest_data.get("Total Liabilities Net Minority Interest")
    total_shareholder_equity = latest_data.get("Stockholders Equity")  # This could also be "Stockholders Equity" depending on the data

    # Check for missing data
    if total_liabilities is None or total_shareholder_equity is None:
        print(f"Missing data for debt to equity calculation for {ticker.ticker}")
        return None

    # Convert to float and calculate Debt to Equity ratio
    debt_to_equity_ratio = float(total_liabilities) / float(total_shareholder_equity)
    return debt_to_equity_ratio

def get_pe_ratio(ticker: yf.Ticker):
    net_income = ticker.quarterly_income_stmt.loc["Net Income"][:4].sum()

    # TODO: This is likely the wrong value, but it's close
    diluted_average_shares = ticker.quarterly_income_stmt.loc["Diluted Average Shares"].iloc[0]

    eps = float(net_income) / float(diluted_average_shares)

    # Fetch current stock price using get_return function
    current_price = get_latest_price(ticker)

    # Calculate P/E ratio
    pe_ratio = float(current_price) / eps
    return pe_ratio

def get_ps_ratio(ticker: yf.Ticker):
    net_sales = ticker.quarterly_income_stmt.loc["Total Revenue"][:4].sum()

    # TODO: This is likely the wrong value, but it's close
    diluted_average_shares = ticker.quarterly_income_stmt.loc["Diluted Average Shares"].iloc[0]

    ips = float(net_sales) / float(diluted_average_shares)

    # Fetch current stock price using get_return function
    current_price = get_latest_price(ticker)

    # Calculate P/E ratio
    ps_ratio = float(current_price) / ips
    return ps_ratio

def get_ebidta_margin(ticker: yf.Ticker):
    net_sales = ticker.quarterly_income_stmt.loc["Total Revenue"][:4].sum()
    ebidta = ticker.quarterly_income_stmt.loc["EBITDA"][:4].sum()

    ebidta_margin = float(ebidta) / float(net_sales)
    return ebidta_margin

def get_beta(stock_ticker, market_ticker='VOO', period='2y', interval='1d'):
    # Fetch historical data for the stock and the market
    stock_data = yf.download(stock_ticker, period=period, interval=interval)['Close']
    market_data = yf.download(market_ticker, period=period, interval=interval)['Close']

    # Ensure both data frames have the same dates
    data = pd.concat([stock_data, market_data], axis=1).dropna()
    data.columns = [stock_ticker, market_ticker]

    # Calculate daily returns
    returns = data.pct_change().dropna()

    # Conduct the regression to find beta
    covariance = returns.cov().iloc[0,1]
    market_variance = returns[market_ticker].var()

    beta = covariance / market_variance
    return beta

def get_latest_price(ticker):
    data = ticker.history(period="1d")
    if data.empty:
        return None
    return data["Close"].iloc[-1]

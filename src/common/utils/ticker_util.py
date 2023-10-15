import yfinance as yf
import numpy as np

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
    day_period = 10
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

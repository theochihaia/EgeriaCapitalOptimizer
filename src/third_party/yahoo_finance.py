import yfinance as yf
import requests_cache
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
from pandas_datareader import data as pdr
import requests


from src.common.configuration.app_config import YF_CACHE_TIMEOUT, YF_DURATION, YF_REQUEST_RATE

"""
Relevant objects for symbol:
- info
- history (requires parameter e.g., period="1mo")
- history_metadata
- actions
- dividends
- splits
- capital_gains (only for mutual funds & etfs)
- get_shares_full (requires parameters e.g., start="2000-01-01", end=None)
- income_stmt
- quarterly_income_stmt
- balance_sheet
- quarterly_balance_sheet
- cashflow
- quarterly_cashflow
- major_holders
- institutional_holders
- mutualfund_holders
- earnings_dates
- isin (experimental)
- options
- news
"""


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

session = CachedLimiterSession(
    limiter=Limiter(
        RequestRate(YF_REQUEST_RATE, YF_DURATION)
    ),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache", expire_after=YF_CACHE_TIMEOUT), # 5 days
)

session = requests_cache.CachedSession("yfinance.cache")
session.headers["User-agent"] = "my-program/1.0"

yf.pdr_override()

'''
import yfinance as yf

tickers = yf.Tickers('msft aapl goog')

# access each ticker using (example)
tickers.tickers['MSFT'].info
tickers.tickers['AAPL'].history(period="1mo")
tickers.tickers['GOOG'].actions
'''
# Pull data from Yahoo Finance given a list of symbols
def pull_general_data(symbol_list: list):
    data = {}
    ticker_dict = yf.Tickers(symbol_list, session=session)
    for symbol in symbol_list:
        try:
            ticker = ticker_dict.tickers[symbol]
            #info = ticker.get_info()
            moredata = pdr.get_data_yahoo(symbol, period="1yr", session=session,  threads=False) 

            data[symbol] = ticker
        except Exception as e:
            print(f"Failed to pull data for {symbol}. Reason: {e}")
    return data

def pull_pricing_data(symbol_list: list, period: str = "1yr"):
    return {symbol: pdr.get_data_yahoo(symbol, period=period, session=session) for symbol in symbol_list}


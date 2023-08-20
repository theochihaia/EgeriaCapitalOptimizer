import yfinance as yf
import requests_cache
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
from pandas_datareader import data as pdr

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'

yf.pdr_override()


symbols = [
    "AAPL", "ACN", "AMZN", "ATO", "CL", "COST", "CRM", "CTAS", "DE", "GD",
    "GOOGL", "HES", "HRL", "JNJ", "JPM", "LCID", "LIN", "LLY", "MDT", "MSFT",
    "NEE", "NUE", "NVDA", "NVO", "PEP", "PG", "PXD", "ROP", "TGT", "TMO",
    "V", "WMT"
]

'''
Strategies:

Configuration file for parameters: STD Range
    Calculate standard deviation and mean of x Time Period
        Create alert if above or below threshold
    Generate X Week Max and Low
    Generate trend line and STD for income, create alert log if beyond line
    Generate trend line and STD for debt, create alert log if beyond line
    Generate output displaying top P/E of each equity
    Create portfolio optimizer of each portfolio input
    Allow import of portfolio, create a tool to generate the buy/sell calcualtions 
        -> This probably can be done via count of shares in Excel
    
        
    ---------------------
    Need a tool that will alert if P/E is outside range, if income has changed, debt has changed
    A tool, given shares that it will help rebalance amounts
    A tool that generates a portfolio based variation and backtests performance
    

'''





ticker_string = ' '.join(symbols[:3])

data = pdr.get_data_yahoo(ticker_string, period="1yr", session=session)

#print(data)

for symbol in symbols:
    results = yf.Ticker(symbol)
    print(results.info)


def pull_data(symbol: str):
    msft = yf.Ticker(symbol)

    # get all stock info
    msft.info

    # get historical market data
    hist = msft.history(period="1mo")

    # show meta information about the history (requires history() to be called first)
    msft.history_metadata

    # show actions (dividends, splits, capital gains)
    msft.actions
    msft.dividends
    msft.splits
    msft.capital_gains  # only for mutual funds & etfs

    # show share count
    msft.get_shares_full(start="2000-01-01", end=None)

    # show financials:
    # - income statement
    msft.income_stmt
    msft.quarterly_income_stmt

    # - balance sheet
    msft.balance_sheet
    msft.quarterly_balance_sheet
    # - cash flow statement
    msft.cashflow
    msft.quarterly_cashflow
    # see `Ticker.get_income_stmt()` for more options

    # show holders
    msft.major_holders
    msft.institutional_holders
    msft.mutualfund_holders

    # Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default. 
    # Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
    msft.earnings_dates

    # show ISIN code - *experimental*
    # ISIN = International Securities Identification Number
    msft.isin

    # show options expirations
    msft.options

    # show news
    msft.news

    # get option chain for specific expiration
    #opt = msft.option_chain('YYYY-MM-DD')
    # data available via: opt.calls, opt.puts
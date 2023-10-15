from src.common.enums.equity_data_category import EquityDataCategory
from src.common.enums.metric import Metric
from src.common.enums.portfolio import Portfolio

# Portfolio Symbols
SYMBOLS = [
    #Portfolio.TESTING,
    Portfolio.FID_FOLIO,
    #Portfolio.FID_FOLIO_V2,
    #Portfolio.NOBL,
    #Portfolio.SP500,
    #Portfolio.IJR_SMALL_CAP,
    #Portfolio.IJH_MID_CAP,
    #Portfolio.IYW_TECHNOLOGY,
    #Portfolio.IYK_CONSUMER_STAPLES,
    #Portfolio.IYF_FINANCIAL,
]

# Generation Settings
DIRECTORY = "src/storage/data"
IS_SAVE_DATA_ACTIVE = False
IS_CLEAR_HISTORY_ACTIVE = True and IS_SAVE_DATA_ACTIVE
IS_GET_MONTHLY_ACTIVE = False
IS_GENERATE_CVS_ACTIVE = True
IS_GENERATIE_PORTFOLIO_ACTIVE = True


DATA_CATEGORIES = [
    EquityDataCategory.INFO,
    EquityDataCategory.INCOME_STMT,
    EquityDataCategory.BALANCE_SHEET,
    EquityDataCategory.QUARTERLY_INCOME_STMT,
]

ACTIVE_METRICS = [
    Metric.PRICE_TO_EARNINGS,
    Metric.PRICE_TO_BOOK,
    Metric.PRICE_TO_SALES,
    Metric.BETA,
    Metric.YIELD,
    Metric.QUICK_RATIO,
    Metric.DEBT_TO_EQUITY,
    Metric.EBIDTA_MARGIN,
    Metric.RETURN_ON_EQUITY,
    Metric.RETURN_ON_ASSETS,
    Metric.STD_FIVE_YEAR,
    Metric.STD_TEN_YEAR,
    Metric.EBIDTA_AVG_GROWTH_RATE,
    Metric.REVENUE_AVG_GROWTH_RATE,
    Metric.RETURN_FIVE_YEAR,
    Metric.RETURN_TEN_YEAR,
]


# Analyzer Configuration
MIN_TRADING_DAYS = 2500
MAX_PORTFOLIO_SIZE = 30
LOG_BASE = 4


# Yahoo Finance Configuration
YF_CACHE_TIMEOUT = 60 * 60 * 24 * 7 # 1 week
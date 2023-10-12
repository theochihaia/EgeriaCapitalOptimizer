from typing import List
import yfinance as yf


from src.common.enums.symbols import SymbolSet
from src.common.utils.ticker_util import get_symbols
from src.third_party.yahoo_finance import pull_general_data
from src.storage.datastore import save_data, clear_directory, save_data_parallel
from src.common.enums.equity_data_category import EquityDataCategory
from src.common.enums.metric import Metric
from src.logic.algorithms.file_generator import generate_files

from src.logic.algorithms.analyzers import analyze_tickers_concurrent, generate_portfolio
from src.logic.algorithms.monthly_returns import get_monthly


"""
TODO: Build Fidelity Folio V2 with Small Cap, Mid Cap and well rouded sectors
"""


"""
python3 -m venv newenv
source newenv/bin/activate
pip install -r requirements.txt
"""

# ------------------------------------------------------------#
# Parameters
# ------------------------------------------------------------#

symbol_set = [
    #SymbolSet.TESTING,
    SymbolSet.FID_FOLIO,
    #SymbolSet.NOBL,
    #SymbolSet.SP500,
    #SymbolSet.IJR_SMALL_CAP,
    #SymbolSet.IJH_MID_CAP,
    #SymbolSet.IYW_TECHNOLOGY,
    #SymbolSet.IYK_CONSUMER_STAPLES,
    #SymbolSet.IYF_FINANCIAL,
]


DIRECTORY = "src/storage/data"
IS_SAVE_DATA_ACTIVE = False
IS_CLEAR_HISTORY_ACTIVE = True and IS_SAVE_DATA_ACTIVE
IS_GET_MONTHLY_ACTIVE = False
IS_GENERATE_CVS_ACTIVE = True
IS_GENERATIE_PORTFOLIO_ACTIVE = True


data_categories = [
    EquityDataCategory.INFO,
    EquityDataCategory.INCOME_STMT,
    EquityDataCategory.BALANCE_SHEET,
    EquityDataCategory.QUARTERLY_INCOME_STMT,
]

metrics = [
    Metric.PRICE_TO_EARNINGS,
    Metric.PRICE_TO_BOOK,
    Metric.PRICE_TO_SALES,
    Metric.BETA,
    Metric.YIELD,
    Metric.QUICK_RATIO,
    Metric.DEBT_TO_EQUITY,
    Metric.FIVE_YEAR_VARIANCE,
    Metric.TEN_YEAR_VARIANCE,
    Metric.EBIDTA_MARGIN,
    Metric.EBIDTA_AVG_GROWTH_RATE,
    Metric.REVENUE_AVG_GROWTH_RATE,
    Metric.FIVE_YEAR_RETURN,
    Metric.TEN_YEAR_RETURN,
]
# ------------------------------------------------------------#
# Helpers
# ------------------------------------------------------------#
# Clear Directory
def clear_directorires():
    if IS_CLEAR_HISTORY_ACTIVE:
        clear_directory(DIRECTORY)


# Save Data
def save_data(data: dict):
    if IS_SAVE_DATA_ACTIVE:
        for symbol, ticker in data.items():
            save_data_parallel(symbol, ticker, data_categories, DIRECTORY)


def generate_analysis(data: dict):
    # Analyze Tickers   
    analysis = analyze_tickers_concurrent(data, metrics)

    portfolio_proposal = generate_portfolio(analysis)

    # Generate File
    generate_files(analysis, DIRECTORY + "/output", portfolio_proposal, IS_GENERATE_CVS_ACTIVE, symbol_set, metrics)



# ------------------------------------------------------------#
# Main
# ------------------------------------------------------------#
# Get Symbols
symbols = get_symbols(symbol_set)

# Pull data from Yahoo Finance
print("Pulling data from Yahoo Finance")

# Get Monthly Returns
if IS_GET_MONTHLY_ACTIVE:
    monthly = get_monthly("2000-01-01", "2023-09-04")
    print(monthly)

data_general = pull_general_data(symbols)

clear_directorires()

save_data(data_general)

generate_analysis(data_general)

print("Processing Complete")

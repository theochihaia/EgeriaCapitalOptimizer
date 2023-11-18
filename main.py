from typing import List
import yfinance as yf
from datetime import datetime, timedelta

from src.common.configuration.app_config import *
from src.common.utils.ticker_util import get_symbols
from src.third_party.yahoo_finance import pull_general_data
from src.storage.file_store import save_data, clear_directory, save_data_parallel
from src.storage.file_generator import generate_files

from src.logic.algorithms.analyzers import analyze_tickers, generate_portfolio
from src.logic.algorithms.monthly_returns import get_monthly_stats


"""
TODO: 
    Test for 3 year period. For N-3 years, select the companies based on earnings during that time period.
    Compare that portfolio return for the subsequent 3 years and compare performance.
"""


"""
python3 -m venv newenv
source newenv/bin/activate
pip install -r requirements.txt
"""

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
            save_data_parallel(symbol, ticker, DATA_CATEGORIES, DIRECTORY)


def generate_analysis(data: dict):
    # Analyze Tickers   
    analysis = analyze_tickers(data, ACTIVE_METRICS, IS_CONCURRENT)

    portfolio_proposal = generate_portfolio(analysis)

    # Generate File
    generate_files(analysis, DIRECTORY + "/output", portfolio_proposal, IS_GENERATE_CVS_ACTIVE, SYMBOLS, ACTIVE_METRICS)


# ------------------------------------------------------------#
# Main
# ------------------------------------------------------------#
# Get Symbols
symbols = get_symbols(SYMBOLS)

# Pull data from Yahoo Finance
print("Pulling data from Yahoo Finance")

# Get Monthly Returns
if IS_GET_MONTHLY_ACTIVE:
    current_date = datetime.now().date()
    start_date = current_date - timedelta(days=10*365.25)  # Approximate, considering leap years

    monthly = get_monthly_stats("VOO", start_date, current_date)
    monthly = get_monthly_stats("BLV", start_date, current_date)

data_general = pull_general_data(symbols)

clear_directorires()

save_data(data_general)

generate_analysis(data_general)

print("Processing Complete")

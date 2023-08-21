from src.common.symbols import get_symbols, SymbolSet
from src.utilities.third_party.yahoo_finance import pull_data
from src.storage.datastore import save_data, clear_directory
from src.common.equity_data_category import EquityDataCategory

'''
python3 -m venv newenv
source newenv/bin/activate
pip install -r requirements.txt
'''

# Get the list of symbols
symbols = get_symbols(SymbolSet.TESTING)
directory = "src/storage/data"
clear_history = True

# Pull data from Yahoo Finance
data = pull_data(symbols)

# Clear Directory
if clear_history:
     clear_directory(directory)

# Example usage:
data_categories = [
     EquityDataCategory.INFO,
     EquityDataCategory.INCOME_STMT,
     EquityDataCategory.BALANCE_SHEET
]
for symbol, data_for_symbol in data.items():
     save_data(symbol, data_for_symbol, data_categories, directory)
from src.common.symbols import get_symbols, SymbolSet
from src.utilities.third_party.yahoo_finance import pull_data


'''
python3 -m venv newenv
source newenv/bin/activate
pip install -r requirements.txt
'''

# Get the list of symbols
symbols = get_symbols(SymbolSet.ROBINHOOD)

# Pull data from Yahoo Finance
data = pull_data(symbols)

# Print the data
print(data)

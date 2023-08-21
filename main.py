from typing import List

from src.common.enums.symbols import get_symbols, SymbolSet
from src.common.models.AnalysisResult import AnalysisResult
from src.utilities.third_party.yahoo_finance import pull_data
from src.storage.datastore import save_data, clear_directory, save_data_parallel
from src.common.enums.equity_data_category import EquityDataCategory
from src.common.enums.metric import Metric, MetricResult
from src.utilities.algorithms.analyzers import analyze



'''
python3 -m venv newenv
source newenv/bin/activate
pip install -r requirements.txt
'''

#------------------------------------------------------------#
# Parameters
symbols = get_symbols(SymbolSet.ROBINHOOD)
directory = "src/storage/data"
is_save_data_active = False
is_clear_history_active = True and is_save_data_active

data_categories = [
     EquityDataCategory.INFO,
     EquityDataCategory.INCOME_STMT,
     EquityDataCategory.BALANCE_SHEET
]

metrics = [
     Metric.PRICE_TO_EARNINGS,
     Metric.PRICE_TO_BOOK,
     #Metric.STANDARD_DEVIATION
]
#------------------------------------------------------------#

# Pull data from Yahoo Finance
print("Pulling data from Yahoo Finance")
data = pull_data(symbols)

# Clear Directory
if is_clear_history_active:
     clear_directory(directory)

# Save Data
if is_save_data_active:
     for symbol, data_for_symbol in data.items():
          save_data_parallel(symbol, data_for_symbol, data_categories, directory)

# Generate Analysis
analysis: List[AnalysisResult] = []
for symbol, data_for_symbol in data.items():
     analysis.extend(analyze(symbol, data_for_symbol, metrics))

for result in analysis:
     print(result)

print("Processing Complete")
from typing import List

from src.common.enums.symbols import get_symbols, SymbolSet
from src.common.models.AnalysisResult import AnalysisResult
from src.utilities.third_party.yahoo_finance import pull_data
from src.storage.datastore import save_data, clear_directory, save_data_parallel
from src.common.enums.equity_data_category import EquityDataCategory
from src.common.enums.metric import Metric, MetricResult
from src.utilities.algorithms.analyzers import analyze
from src.utilities.algorithms.generate_egeria_score import EgeriaScore
from src.utilities.algorithms.monthly_returns import get_monthly


'''
python3 -m venv newenv
source newenv/bin/activate
pip install -r requirements.txt
'''

#------------------------------------------------------------#
# Parameters
#------------------------------------------------------------#

symbols = get_symbols(SymbolSet.ROBINHOOD)
directory = "src/storage/data"
is_save_data_active = False
is_clear_history_active = True and is_save_data_active
is_get_monthly_active = False
metric_result_filter = MetricResult.NEGATIVE

data_categories = [
     EquityDataCategory.INFO,
     EquityDataCategory.INCOME_STMT,
     EquityDataCategory.BALANCE_SHEET
]

metrics = [
     Metric.PRICE_TO_EARNINGS,
     Metric.PRICE_TO_BOOK,
     Metric.PRICE_TO_SALES,
     Metric.BETA,
     #Metric.EBIDTA_DEVIATION,
     #Metric.EGERIA_SCORE,
     #Metric.STANDARD_DEVIATION
]
#------------------------------------------------------------#
# Helpers
#------------------------------------------------------------#

#Clear Directory
def clear_directory():
     if is_clear_history_active:
          clear_directory(directory)

# Save Data
def save_data(data: dict):
     if is_save_data_active:
          for symbol, ticker in data.items():
               save_data_parallel(symbol, ticker, data_categories, directory)

# Generate Analysis
def generate_analysis(data: dict):
     analysis: List[AnalysisResult] = []
     for symbol, ticker in data.items():
          analysis.extend(analyze(ticker, metrics))
     for result in analysis:
          if(metric_result_filter is not None):
               if(result.metric_result == metric_result_filter):
                    print(result)
          else:
               print(result)

#------------------------------------------------------------#
# Main
#------------------------------------------------------------#

# Pull data from Yahoo Finance
print("Pulling data from Yahoo Finance")

#Get Monthly Returns
if(is_get_monthly_active):
     monthly = get_monthly("2000-01-01", "2023-09-04")
     print(monthly)

data = pull_data(symbols)

clear_directory()

save_data(data)

generate_analysis(data)

'''
egeriaScores = []
for symbol, ticker in data.items():
     eg_score = EgeriaScore(ticker, metrics)
     egeriaScores.append(eg_score)
     print(eg_score)
'''

print("Processing Complete")

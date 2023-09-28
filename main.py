from collections import defaultdict
from typing import List
import concurrent.futures

from src.common.enums.symbols import get_symbols, SymbolSet
from src.common.models.AnalysisResult import AnalysisResult
from src.common.models.AnalysisResultGroup import AnalysisResultGroup
from src.utilities.third_party.yahoo_finance import pull_general_data, pull_pricing_data
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

symbols = get_symbols(SymbolSet.FID_FOLIO)
directory = "src/storage/data"
is_save_data_active = True
is_clear_history_active = True and is_save_data_active
is_get_monthly_active = False

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
     Metric.NORMALIZED_EBIDTA_DEVIATION,
     Metric.TOTAL_REVENUE_DEVIATION,
     Metric.QUICK_RATIO,
     Metric.DEBT_TO_EQUITY,
     Metric.FIVE_YEAR_RETURN,
     Metric.TEN_YEAR_RETURN,
     #Metric.STANDARD_DEVIATION
     #Metric.EGERIA_SCORE,

]
#------------------------------------------------------------#
# Helpers
#------------------------------------------------------------#

#Clear Directory
def clear_directorires():
     if is_clear_history_active:
          clear_directory(directory)

# Save Data
def save_data(data: dict):
     if is_save_data_active:
          for symbol, ticker in data.items():
               save_data_parallel(symbol, ticker, data_categories, directory)

def generate_analysis(data: dict):
    analysis: List[AnalysisResultGroup] = []

    for ticker in data.values():
        results = analyze(ticker, metrics)
        analysis.append(results)  # Ensure we don't include None results

     # Sort the analysis list by the egeria_score attribute in descending order
    sorted_analysis = sorted(analysis, key=lambda x: x.egeria_score, reverse=True)

     # Display the sorted results
    for analysis_result in sorted_analysis:
        print(analysis_result)

#------------------------------------------------------------#
# Main
#------------------------------------------------------------#

# Pull data from Yahoo Finance
print("Pulling data from Yahoo Finance")

#Get Monthly Returns
if(is_get_monthly_active):
     monthly = get_monthly("2000-01-01", "2023-09-04")
     print(monthly)

data_general = pull_general_data(symbols)
#data_prices = pull_pricing_data(symbols, "1yr")

clear_directorires()

save_data(data_general)

generate_analysis(data_general)

'''
egeriaScores = []
for symbol, ticker in data.items():
     eg_score = EgeriaScore(ticker, metrics)
     egeriaScores.append(eg_score)
     print(eg_score)
'''

print("Processing Complete")

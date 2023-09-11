from typing import List
import concurrent.futures

from src.common.enums.symbols import get_symbols, SymbolSet
from src.common.models.AnalysisResult import AnalysisResult
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
     Metric.NORMALIZED_EBIDTA_DEVIATION,
     Metric.TOTAL_REVENUE_DEVIATION,
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

# Generate Analysis
def generate_analysis(data: dict):
    analysis: List[AnalysisResult] = []

    # Parallelize the analysis using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(parallel_analysis, data.values()))
        
    for result_set in results:
        analysis.extend(result_set)

    for result in analysis:
        if(metric_result_filter is not None):
            if(result.metric_result == metric_result_filter):
                print(result)
        else:
            print(result)

def parallel_analysis(ticker):
    return analyze(ticker, metrics)

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

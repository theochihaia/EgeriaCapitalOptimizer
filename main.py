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
from src.common.configuration.sector_statistics import SECTOR_METRIC_STATISTICS_STR
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

symbol_set = SymbolSet.FID_FOLIO
directory = "src/storage/data"
is_save_data_active = False
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
     Metric.YIELD,
     Metric.NORMALIZED_EBIDTA_DEVIATION,
     Metric.TOTAL_REVENUE_DEVIATION,
     Metric.QUICK_RATIO,
     Metric.DEBT_TO_EQUITY,
     Metric.FIVE_YEAR_RETURN,
     Metric.TEN_YEAR_RETURN,

     #Metric.STANDARD_DEVIATION


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
    
    # Define a helper function for parallel execution
    def analyze_ticker(ticker):
        return analyze(ticker, metrics)

    # Use ThreadPoolExecutor to parallelize the analysis
    with concurrent.futures.ThreadPoolExecutor() as executor:
        analysis.extend(executor.map(analyze_ticker, data.values()))

    # Filter out None results if any
    analysis = [result for result in analysis if result]

    # Sort the analysis list by the egeria_score attribute in descending order
    sorted_analysis = sorted(analysis, key=lambda x: x.egeria_score, reverse=True)

    result_file_path = f"src/storage/output/results_{symbol_set.value}.txt"

    # Now, write to the file
    with open(result_file_path, 'w') as file:
        file.write("-----------------------------------------------------\n")
        file.write("                        Stats                        \n")
        file.write("-----------------------------------------------------\n")
        
        file.write(SECTOR_METRIC_STATISTICS_STR + "\n")

        file.write("-----------------------------------------------------\n")
        file.write("                       Ranking                       \n")
        file.write("-----------------------------------------------------\n")
        file.write("\n")

        ix = 0
        for analysis_result in sorted_analysis:
            ix += 1
            file.write(f"{ix:02}|{analysis_result.symbol}" + '\n')

        file.write("\n")
        file.write("-----------------------------------------------------\n")
        file.write("                       Details                       \n")
        file.write("-----------------------------------------------------\n")
        file.write("\n")

        for analysis_result in sorted_analysis:
            file.write(str(analysis_result) + '\n')

    # Print the results to the console
    with open(result_file_path, 'r') as file:
        print(file.read())
#------------------------------------------------------------#
# Main
#------------------------------------------------------------#
# Get Symbols
symbols = get_symbols(symbol_set)

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

print("Processing Complete")

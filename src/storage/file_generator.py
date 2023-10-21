import os

from src.common.enums.portfolio import Portfolio
from src.common.utils.ticker_util import get_return, get_std
from src.common.models.AnalysisResult import AnalysisResult
from src.common.models.AnalysisResultGroup import AnalysisResultGroup
from src.common.configuration.sector_statistics import SECTOR_METRIC_STATISTICS
from src.logic.algorithms.analyzers import calculate_weighted_portfolio_returns, calculate_weighted_fn

def generate_files(sorted_analysis: [AnalysisResultGroup], dir: str, portfolio_proposal: [], is_generate_csv_active: bool, generate_composite: Portfolio, metrics: [str]):
    result_file_path = (
        f"{dir}/portfolio_composite"
        if len(generate_composite) > 1
        else f"{dir}/portfolio_{generate_composite[0].value}"
    )

    # Ensure the directory exists
    ensure_dir(result_file_path)


    # Generate File
    with open(f"{result_file_path}.txt", "w", encoding='utf-8') as file:
        file.write(get_header("Metric Stats"))
        stats = SECTOR_METRIC_STATISTICS.get("Default")
        metrics_set = {metric.name for metric in metrics}
        file.write(f"{'Metric':<30} | {'Avg':>10} | {'Std':>10} | {'Is Active':>5}\n")
        for key, value in stats.items():
            is_active = "Yes" if key in metrics_set else "No"
            file.write(f"{key:<30} | {value[0]:>10} | {value[1]:>10} | {is_active:>5}\n")

        file.write(get_header("Portfolio Proposal"))
        file.write("\n")  # New line for spacing
        file.write(f"{'Symbol':<10} | {'Name':<50} | {'Weight':>7}\n")
        file.write("-" * 72 + "\n")  # Add a separator line
        for result in portfolio_proposal:
            symbol, name, weight = result.symbol, result.ticker.get_info().get('longName'), result.weight
            if weight > 0:
                file.write(f"{symbol:<10} | {name:<50} | {round(weight,2):>7.2f}%\n")

        five_yr_return = calculate_weighted_fn(portfolio_proposal,5, get_return)
        five_yr_std = calculate_weighted_fn(portfolio_proposal,5, get_std)
        
        file.write(f"\n\n")
        file.write(f"Weighted Return (5yrs): {round(five_yr_return,2):>5.2f}\n")
        file.write(f"Weighted Std    (5yrs): {round(five_yr_std,2):>5.2f}\n")

        file.write(get_header("Details"))
        for analysis_result in sorted_analysis:
            file.write(str(analysis_result or None) + "\n")


        print(f"Results written to {result_file_path}.txt")

        invalid_tickers = [result for result in sorted_analysis if result.is_disqualified]
        if(len(invalid_tickers) > 0):
            print("Unprocessable Tickers: " + ", ".join([result.symbol for result in invalid_tickers]))

        if is_generate_csv_active:
            generate_csv(sorted_analysis, result_file_path, metrics, portfolio_proposal)



# Ensure the directory exists
def ensure_dir(dir: str):
    directory = os.path.dirname(dir)
    if not os.path.exists(directory):
        os.makedirs(directory)


# Generate CSV
def generate_csv(analysis: [AnalysisResultGroup], result_file_path: str, metrics: [str], portfolio_proposal: []):
    csv_file_path = f"{result_file_path}.csv"

    with open(csv_file_path, "w") as file:
            column_headers = " Norm,".join(metrics.value for metrics in metrics)
            column_headers += " Norm"
            file.write(f"Index,Symbol,Name,EgeriaScore,PortfolioWeight,YearlyReturn5YrAvg,{column_headers}\n")  # Write CSV header
            ix = 0
            for analysis_result in analysis:
                ix += 1
                metric_output = ",".join(
                        str(metric_result.normalized_value) if (metric_result is not None and metric_result is not None) else ""
                        for metric_result in analysis_result.results
                    )
                file.write(f"{ix:03},{analysis_result.symbol},\"{analysis_result.ticker.get_info().get('longName')}\",{analysis_result.egeria_score},{round(analysis_result.weight,2)},{round(get_return(analysis_result.ticker,'5y')/5,2)},{metric_output}\n")
    print("CSV written to " + csv_file_path)

# Get Header
def get_header(header_label: str):
    return f"""
\n
--------------------------------------------------------------------------
                              {header_label}                       
--------------------------------------------------------------------------
"""

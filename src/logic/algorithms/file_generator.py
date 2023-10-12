import os

from src.common.enums.symbols import SymbolSet
from src.common.utils.ticker_util import get_symbols
from src.common.models.AnalysisResult import AnalysisResult
from src.common.models.AnalysisResultGroup import AnalysisResultGroup
from src.common.configuration.sector_statistics import SECTOR_METRIC_STATISTICS_STR

def generate_files(sorted_analysis: [AnalysisResultGroup], dir: str, portfolio_proposal: [], is_generate_csv_active: bool, generate_composite: SymbolSet, metrics: [str]):
    result_file_path = (
        f"{dir}/results_composite.txt"
        if len(generate_composite) > 1
        else f"{dir}/results_{generate_composite[0].value}.txt"
    )

    # Ensure the directory exists
    ensure_dir(result_file_path)

    # Generate File
    with open(result_file_path, "w", encoding='utf-8') as file:
        file.write(get_header("Stats"))
        file.write(SECTOR_METRIC_STATISTICS_STR + "\n")

        file.write(get_header("Metrics"))
        for metric in metrics:
            file.write(metric.value + "\n")


        file.write(get_header("Portfolio Proposal"))
        file.write("\n")  # New line for spacing
        file.write(f"{'Symbol':<10} | {'Name':<50} | {'Weight':>7}\n")
        file.write("-" * 72 + "\n")  # Add a separator line
        for result in portfolio_proposal:
            symbol, name, weight = result
            file.write(f"{symbol:<10} | {name:<50} | {weight:>7.2f}%\n")


        file.write(get_header("Details"))
        for analysis_result in sorted_analysis:
            file.write(str(analysis_result or None) + "\n")


        print("Results written to " + result_file_path)

        invalid_tickers = [result for result in sorted_analysis if result.is_disqualified]
        if(len(invalid_tickers) > 0):
            print("Unprocessable Tickers: " + ", ".join([result.symbol for result in invalid_tickers]))

        if is_generate_csv_active:
            generate_csv(sorted_analysis, dir, metrics)



# Ensure the directory exists
def ensure_dir(dir: str):
    directory = os.path.dirname(dir)
    if not os.path.exists(directory):
        os.makedirs(directory)


# Generate CSV
def generate_csv(analysis: [AnalysisResultGroup], dir: str, metrics: [str]):
    csv_file_path = f"{dir}/results_composite.csv"
    print("CSV written to " + csv_file_path)
    with open(csv_file_path, "w") as file:
            column_headers = " Norm,".join(metrics.value for metrics in metrics)
            column_headers += " Norm"
            file.write(f"Index,Symbol,Name,Egeria_Score,{column_headers}\n")  # Write CSV header
            ix = 0
            for analysis_result in analysis:
                ix += 1
                metric_output = ",".join(
                        str(metric_result.normalized_value) if (metric_result is not None and metric_result is not None) else ""
                        for metric_result in analysis_result.results
                    )
                file.write(f"{ix:03},{analysis_result.symbol},\"{analysis_result.ticker.get_info().get('longName')}\",{analysis_result.egeria_score},{metric_output}\n")


# Get Header
def get_header(header_label: str):
    return f"""
-----------------------------------------------------
                    {header_label}                       
-----------------------------------------------------
"""

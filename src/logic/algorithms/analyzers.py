import yfinance as yf
from collections import defaultdict
import concurrent.futures
from typing import List
from typing import Optional
import pandas as pd
from datetime import datetime

from src.common.models.MetricConfig import MetricConfig
from src.common.configuration.sector_statistics import SECTOR_METRIC_STATISTICS
from src.common.configuration.metric_config import METRIC_CONFIG
from src.common.enums.metric import Metric, MetricResult
from src.common.models.AnalysisResult import AnalysisResult
from src.common.models.AnalysisResultGroup import AnalysisResultGroup
from src.logic.algorithms.range_normalizer import RangeAnalysisConfig, range_normalizer

MIN_TRADING_DAYS = 2500

def analyze_tickers_concurrent(data: dict, metrics: [Metric]):
    analysis: List[AnalysisResultGroup] = []

    # Define a helper function for parallel execution
    def analyze_ticker(symbol, ticker):
        if not valid_ticker(ticker):
            print(f"Validation Error. Could not process symbol: {symbol}")
            return AnalysisResultGroup(symbol, [], 0.0, ticker, True)
        return analyze(symbol, ticker, metrics)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(analyze_ticker, symbol, ticker)
            for symbol, ticker in data.items()
        ]
        analysis = [
            future.result()
            for future in concurrent.futures.as_completed(futures)
            if future.result()
        ]

    # Filter out None results if any
    analysis = [result for result in analysis if result]

    # Sort the analysis list by the egeria_score attribute in descending order
    sorted_analysis = sorted(analysis, key=lambda x: x.egeria_score, reverse=True)
    return sorted_analysis


def analyze(symbol: str, ticker: yf.Ticker, metrics: [Metric]) -> [AnalysisResult]:
    results: List[AnalysisResult] = []
    for metric in metrics:
        # Check if configuration exists for metric
        metric_config = METRIC_CONFIG.get(metric)
        if not metric_config:
            raise ValueError(f"No configuration for metric: {metric}")

        results.append(analyze_metric(symbol, metric, metric_config, ticker))

    # Generate grouped results
    try:
        egeria_score = generate_egeria_score(results)
    except ValueError as e:
        # Handle the exception here
        print(f"Error for symbol {symbol} :", e)

    
    grouped_results = AnalysisResultGroup(symbol, results, egeria_score, ticker)

    return grouped_results


def get_sector_statistics(ticker: yf.Ticker, metric_key):
    sector = "Default"
    
    #sector = ticker.info.get("sector", "Default")
    return SECTOR_METRIC_STATISTICS.get(sector, {}).get(metric_key, (None, None))


def analyze_metric(symbol: str, metric: Metric, metric_config: MetricConfig, ticker: yf.Ticker):
    avg, std = get_sector_statistics(ticker, metric_config.stat_key)

    if avg is None or std is None:
        print(f"Could not find sector statistics for metric: {metric} for ticker: {ticker.info['symbol']}")
        return None

    config = RangeAnalysisConfig(
        metric=metric,
        avg=avg,
        std=std,
        fetch_data=metric_config.data_fetcher,
    )

    return range_normalizer(symbol, ticker, config, invert=metric_config.is_inverted)


def generate_egeria_score(results: [AnalysisResult]) -> float:
    if(results is None or len(results) == 0):
        return 0.0
    
    # Get Sector
    #sector = results[0].ticker.info.get("sector", "Default")
    sector = "Default"

    # Get Sector Statistics
    sector_statistics = SECTOR_METRIC_STATISTICS.get(sector, {})
    
    # Calculate Egeria Score
    sum = 0.0
    for result in results:
        if result is not None:
            metric_config = METRIC_CONFIG.get(result.metric)
            weight = metric_config.metric_weight if metric_config else 1
            sum += result.normalized_value * weight
    return round(sum,3);


def valid_ticker(ticker: yf.Ticker) -> bool:
    history10yr = ticker.history(period="10y").values
    if ticker is None:
        return False
    if ticker.info is None:
        return False
    if ticker.info.get("symbol") is None:
        return False
    if len(history10yr) < MIN_TRADING_DAYS:
        return False
    return True

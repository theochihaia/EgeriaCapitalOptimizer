from typing import List
from typing import Optional


import yfinance as yf
from src.common.enums.metric import Metric, MetricResult
from src.common.models.AnalysisResult import AnalysisResult
from src.utilities.algorithms.range_analyzer import RangeAnalysisConfig, range_analyzer

# Constants
PE_THRESHOLD_HIGH = 30
PE_THRESHOLD_LOW = 10
PB_THRESHOLD_HIGH = 9
PB_THRESHOLD_LOW = 1

def analyze(ticker: yf.Ticker, metrics: [Metric]) -> [AnalysisResult]:
    analyzers = {
        Metric.PRICE_TO_EARNINGS: analyze_price_to_earnings,
        Metric.PRICE_TO_BOOK: analyze_price_to_book,
        Metric.PRICE_TO_SALES: analyze_price_to_sales,
        Metric.PRICE_TO_CASHFLOW: analyze_price_to_cashflow,
        Metric.STANDARD_DEVIATION: analyze_standard_deviation,
        Metric.BETA: analyze_beta,
        Metric.BOLLINGER_BANDS: analyze_bollinger_bands,
    }

    results: List[AnalysisResult] = []
    for metric in metrics:
        analysis_function = analyzers.get(metric)
        if not analysis_function:
            raise ValueError(f"No Analyzer for metric: {metric}")

        analysis = analysis_function(ticker)
        if analysis and analysis.metric_result != MetricResult.NEUTRAL:
            results.append(analysis)

    return results

def analyze_egeria_score(
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_egeria_score not implemented")


def analyze_price_to_earnings(
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    config = RangeAnalysisConfig(
        metric=Metric.PRICE_TO_EARNINGS,
        threshold_high=PE_THRESHOLD_HIGH,
        threshold_low=PE_THRESHOLD_LOW,
        fetch_data=lambda ticker: ticker.info.get("trailingPE") or ticker.info.get("forwardPE")
    )
    return range_analyzer(ticker, config)


def analyze_price_to_book(    
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    config = RangeAnalysisConfig(
        metric=Metric.PRICE_TO_BOOK,
        threshold_high=PB_THRESHOLD_HIGH,
        threshold_low=PB_THRESHOLD_LOW,
        fetch_data=lambda ticker: ticker.info.get("priceToBook")
    )
    return range_analyzer(ticker, config)


def analyze_price_to_sales(    
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_price_to_sales not implemented")


def analyze_price_to_cashflow(    
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_price_to_cashflow not implemented")


def analyze_standard_deviation(    
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    return "standard_deviation"


def analyze_beta(    
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_beta not implemented")


def analyze_bollinger_bands(    
        ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_bollinger_bands not implemented")

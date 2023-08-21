from typing import List
from typing import Optional


import yfinance as yf
from src.common.enums.metric import Metric, MetricResult
from src.common.models.AnalysisResult import AnalysisResult

# Constants
PE_THRESHOLD_HIGH = 25
PE_THRESHOLD_LOW = 10
PB_THRESHOLD_HIGH = 5
PB_THRESHOLD_LOW = 1

def analyze(symbol: str, ticker: yf.Ticker, metrics: [Metric]) -> [AnalysisResult]:
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

        analysis = analysis_function(symbol, ticker)
        if analysis and analysis.metric_result != MetricResult.NEUTRAL:
            results.append(analysis)

    return results


def analyze_price_to_earnings(
    symbol: str, ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    pe = ticker.info.get("trailingPE") or ticker.info.get("forwardPE")

    if not pe:
        return None

    if pe > PE_THRESHOLD_HIGH:
        message = f"{symbol} has a high P/E ratio of {pe}"
        return AnalysisResult(
            symbol, Metric.PRICE_TO_EARNINGS, message, MetricResult.NEGATIVE
        )
    elif pe < PE_THRESHOLD_LOW:
        message = f"{symbol} has a low P/E ratio of {pe}"
        return AnalysisResult(
            symbol, Metric.PRICE_TO_EARNINGS, message, MetricResult.POSITIVE
        )
    else:
        message = f"{symbol} has a neutral P/E ratio of {pe}"
        return AnalysisResult(
            symbol, Metric.PRICE_TO_EARNINGS, message, MetricResult.NEUTRAL
        )


def analyze_price_to_book(    
        symbol: str, ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    pb = ticker.info.get("priceToBook")

    if not pb:
        return None

    if pb > PB_THRESHOLD_HIGH:
        message = f"{symbol} has a high P/B ratio of {pb}"
        return AnalysisResult(
            symbol, Metric.PRICE_TO_BOOK, message, MetricResult.NEGATIVE
        )
    elif pb < PB_THRESHOLD_LOW:
        message = f"{symbol} has a low P/B ratio of {pb}"
        return AnalysisResult(
            symbol, Metric.PRICE_TO_BOOK, message, MetricResult.POSITIVE
        )
    else:
        message = f"{symbol} has a neutral P/B ratio of {pb}"
        return AnalysisResult(
            symbol, Metric.PRICE_TO_BOOK, message, MetricResult.NEUTRAL
        )



def analyze_price_to_sales(    
        symbol: str, ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_price_to_sales not implemented")


def analyze_price_to_cashflow(    
        symbol: str, ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_price_to_cashflow not implemented")


def analyze_standard_deviation(    
        symbol: str, ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    return "standard_deviation"


def analyze_beta(    
        symbol: str, ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_beta not implemented")


def analyze_bollinger_bands(    
        symbol: str, ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_bollinger_bands not implemented")

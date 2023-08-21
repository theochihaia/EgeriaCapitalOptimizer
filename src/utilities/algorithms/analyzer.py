from typing import Optional
import yfinance as yf
from src.common.enums.metric import Metric, MetricResult
from src.common.models.AnalysisResult import AnalysisResult

# Constants
HIGH_PE_THRESHOLD = 30
LOW_PE_THRESHOLD = 10


def analyze(symbol: str, ticker: yf.Ticker, metrics: [Metric]) -> [AnalysisResult]:
    analyzers = {
        Metric.PRICE_TO_EARNINGS: analyze_price_to_earnings,
        # Metric.PRICE_TO_BOOK: analyze_price_to_book,
        # ... Map other metrics here ...
    }

    results = []
    for metric in metrics:
        analysis_function = analyzers.get(metric)
        if not analysis_function:
            raise ValueError(f"No Analyzer for metric: {metric}")

        analysis = analysis_function(symbol, ticker)
        if analysis:
            results.append(analysis)

    return results


def analyze_price_to_earnings(
    symbol: str, ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    pe = ticker.info.get("trailingPE") or ticker.info.get("forwardPE")

    if not pe or (pe <= HIGH_PE_THRESHOLD and pe >= LOW_PE_THRESHOLD):
        return None

    if pe > HIGH_PE_THRESHOLD:
        message = f"{symbol} has a high P/E ratio of {pe}"
        return AnalysisResult(
            symbol, Metric.PRICE_TO_EARNINGS, message, MetricResult.NEGATIVE
        )
    elif pe < LOW_PE_THRESHOLD:
        message = f"{symbol} has a low P/E ratio of {pe}"
        return AnalysisResult(
            symbol, Metric.PRICE_TO_EARNINGS, message, MetricResult.POSITIVE
        )


def analyze_price_to_book(ticker: yf.Ticker):
    raise NotImplementedError("analyze_price_to_book not implemented")


def analyze_price_to_sales(ticker: yf.Ticker):
    raise NotImplementedError("analyze_price_to_sales not implemented")


def analyze_price_to_cashflow(ticker: yf.Ticker):
    raise NotImplementedError("analyze_price_to_cashflow not implemented")


def analyze_standard_deviation(ticker: yf.Ticker):
    return "standard_deviation"


def analyze_beta(ticker: yf.Ticker):
    raise NotImplementedError("analyze_beta not implemented")


def analyze_bollinger_bands(ticker: yf.Ticker):
    raise NotImplementedError("analyze_bollinger_bands not implemented")

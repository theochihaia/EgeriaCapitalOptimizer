from collections import defaultdict
from typing import List
from typing import Optional
import pandas as pd
from datetime import datetime


import yfinance as yf
from src.common.configuration.sector_weights import SECTOR_METRIC_THRESHOLDS
from src.common.enums.metric import Metric, MetricResult
from src.common.models.AnalysisResult import AnalysisResult
from src.common.models.AnalysisResultGroup import AnalysisResultGroup
from src.utilities.algorithms.range_analyzer import RangeAnalysisConfig, range_analyzer

# Constants
FIVE_YEAR_RETURN = (60, 120)
TEN_YEAR_RETURN = (150, 250)

metric_weights = {
    Metric.PRICE_TO_EARNINGS: 1,
    Metric.PRICE_TO_BOOK: 1,
    Metric.PRICE_TO_SALES: 1,
    Metric.PRICE_TO_CASHFLOW: 1,
    Metric.STANDARD_DEVIATION: 2,
    Metric.BETA: 4,
    Metric.NORMALIZED_EBIDTA_DEVIATION: 3,
    Metric.TOTAL_REVENUE_DEVIATION: 3,
    Metric.FIVE_YEAR_RETURN: 5,
    Metric.TEN_YEAR_RETURN: 5,
    Metric.FIFTY_DAY_AVG: 3,
    Metric.BOLLINGER_BANDS: 1,
    Metric.QUICK_RATIO: 3,
    Metric.DEBT_TO_EQUITY: 3,
}

metric_weights_total = sum(metric_weights.values())


def analyze(ticker: yf.Ticker, metrics: [Metric]) -> [AnalysisResult]:
    analyzers = {
        Metric.PRICE_TO_EARNINGS: analyze_price_to_earnings,
        Metric.PRICE_TO_BOOK: analyze_price_to_book,
        Metric.PRICE_TO_SALES: analyze_price_to_sales,
        Metric.PRICE_TO_CASHFLOW: analyze_price_to_cashflow,
        Metric.STANDARD_DEVIATION: analyze_standard_deviation,
        Metric.BETA: analyze_beta,
        Metric.NORMALIZED_EBIDTA_DEVIATION: analyze_ebidta_deviation,
        Metric.TOTAL_REVENUE_DEVIATION: analyze_revenue_deviation,
        Metric.FIVE_YEAR_RETURN: analyze_five_year_return,
        Metric.TEN_YEAR_RETURN: analyze_ten_year_return,
        Metric.FIFTY_DAY_AVG: analyze_fifty_day_avg,
        Metric.BOLLINGER_BANDS: analyze_bollinger_bands,
        Metric.QUICK_RATIO: analyze_quick_ratios,
        Metric.DEBT_TO_EQUITY: analyze_debt_to_equity,
    }


    results: List[AnalysisResult] = []
    for metric in metrics:
        try:
            analysis_function = analyzers.get(metric)
            if not analysis_function:
                raise ValueError(f"No Analyzer for metric: {metric}")
            
            results.append(analysis_function(ticker))
        except ValueError as e:
            # Handle the exception here
            print(f"Error for symbol  {ticker.info['symbol']} :", e)


    # Generate grouped results
    try:
        egeria_score = analyze_egeria_score(results)
    except ValueError as e:
        # Handle the exception here
        print(f"Error for symbol  {ticker.info['symbol']} :", e)

    
    grouped_results = AnalysisResultGroup(ticker.info["symbol"], results, egeria_score, ticker)

    return grouped_results


def analyze_egeria_score(results: [AnalysisResult]) -> float:
    if(results is None or len(results) == 0):
        return 0.0

    sum = 0.0
    for result in results:
        value = 0
        if result is None:
            continue
        elif result.metric_result == MetricResult.NEGATIVE:
            value = -1
        elif result.metric_result == MetricResult.POSITIVE:
            value = 1
        sum += metric_weights.get(result.metric, 1) * value
    return round(sum/metric_weights_total * 100, 2)


def get_threshold(ticker: yf.Ticker, metric_key):
    sector = ticker.info.get("sector", "Default")
    return SECTOR_METRIC_THRESHOLDS.get(sector, {}).get(metric_key, (None, None))


def analyze_price_to_earnings(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    threshold_low, threshold_high = get_threshold(ticker, "PE")

    config = RangeAnalysisConfig(
        metric=Metric.PRICE_TO_EARNINGS,
        threshold_high=threshold_high,
        threshold_low=threshold_low,
        fetch_data=lambda t: t.info.get("forwardPE") or t.info.get("trailingPE"),
    )
    return range_analyzer(ticker, config)


def analyze_price_to_book(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    threshold_low, threshold_high = get_threshold(ticker, "PB")

    config = RangeAnalysisConfig(
        metric=Metric.PRICE_TO_BOOK,
        threshold_high=threshold_high,
        threshold_low=threshold_low,
        fetch_data=lambda t: t.info.get("priceToBook"),
    )
    return range_analyzer(ticker, config)


def analyze_price_to_sales(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    threshold_low, threshold_high = get_threshold(ticker, "PS")

    config = RangeAnalysisConfig(
        metric=Metric.PRICE_TO_SALES,
        threshold_high=threshold_high,
        threshold_low=threshold_low,
        fetch_data=lambda t: t.info.get("priceToSalesTrailing12Months"),
    )
    return range_analyzer(ticker, config)


def analyze_price_to_cashflow(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_price_to_cashflow not implemented")


def analyze_standard_deviation(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    return "standard_deviation"


def analyze_beta(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    threshold_low, threshold_high = get_threshold(ticker, "BETA")

    config = RangeAnalysisConfig(
        metric=Metric.BETA,
        threshold_high=threshold_high,
        threshold_low=threshold_low,
        fetch_data=lambda t: t.info.get("beta"),
    )
    return range_analyzer(ticker, config)


def analyze_revenue_deviation(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    # Get Revenue list for ticker
    total_revenue = []
    for key, value in ticker.get_income_stmt().items():
        total_revenue.append(value.get("TotalRevenue"))

    # Get latest Revenue
    latest_revenue = total_revenue[0] if len(total_revenue) > 0 else 0

    # Determine avg and standard deviation of Revenue
    revenue_avg = pd.Series(total_revenue).mean()
    revenue_std = pd.Series(total_revenue).std()

    config = RangeAnalysisConfig(
        metric=Metric.TOTAL_REVENUE_DEVIATION,
        threshold_high=revenue_avg + revenue_std,
        threshold_low=revenue_avg - revenue_std,
        fetch_data=lambda ticker: latest_revenue,
    )
    return range_analyzer(ticker, config, invert=True)


def analyze_ebidta_deviation(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    # Get Revenue list for ticker
    ebidta = []
    for key, value in ticker.get_income_stmt().items():
        ebidta.append(value.get("NormalizedEBITDA"))

    # Get latest Revenue
    latest_ebidta = ebidta[0] if len(ebidta) > 0 else 0

    # Determine avg and standard deviation of Revenue
    ebidta_avg = pd.Series(ebidta).mean()
    ebidta_std = pd.Series(ebidta).std()

    config = RangeAnalysisConfig(
        metric=Metric.NORMALIZED_EBIDTA_DEVIATION,
        threshold_high=ebidta_avg + ebidta_std,
        threshold_low=ebidta_avg - ebidta_std,
        fetch_data=lambda ticker: latest_ebidta,
    )
    return range_analyzer(ticker, config, invert=True)


def analyze_five_year_return(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    return_low, return_high = FIVE_YEAR_RETURN
    data = ticker.history(period="5y")

    if data.empty:
        return

    latest_price = data["Close"].iloc[-1]
    initial_price = data["Close"].iloc[0]
    five_year_return = (latest_price - initial_price) / initial_price * 100

    config = RangeAnalysisConfig(
        metric=Metric.FIVE_YEAR_RETURN,
        threshold_high=return_high,
        threshold_low=return_low,
        fetch_data=lambda ticker: five_year_return,
    )
    return range_analyzer(ticker, config, invert=True)


def analyze_ten_year_return(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    return_low, return_high = TEN_YEAR_RETURN
    data = ticker.history(period="10y")

    if data.empty:
        return

    latest_price = data["Close"].iloc[-1]
    initial_price = data["Close"].iloc[0]
    ten_year_return = (latest_price - initial_price) / initial_price * 100

    config = RangeAnalysisConfig(
        metric=Metric.TEN_YEAR_RETURN,
        threshold_high=return_high,
        threshold_low=return_low,
        fetch_data=lambda ticker: ten_year_return,
    )
    return range_analyzer(ticker, config, invert=True)

def analyze_quick_ratios(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    threshold_low, threshold_high = get_threshold(ticker, "QUICK_RATIO")

    config = RangeAnalysisConfig(
        metric=Metric.QUICK_RATIO,
        threshold_high=threshold_high,
        threshold_low=threshold_low,
        fetch_data=lambda t: t.info.get("quickRatio"),
    )
    return range_analyzer(ticker, config)

def analyze_debt_to_equity(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    threshold_low, threshold_high = get_threshold(ticker, "DEBT_TO_EQUITY")

    config = RangeAnalysisConfig(
        metric=Metric.DEBT_TO_EQUITY,
        threshold_high=threshold_high,
        threshold_low=threshold_low,
        fetch_data=lambda t: t.info.get("debtToEquity"),
    )
    return range_analyzer(ticker, config)

def analyze_fifty_day_avg(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_bollinger_bands not implemented")


def analyze_bollinger_bands(ticker: yf.Ticker) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_bollinger_bands not implemented")

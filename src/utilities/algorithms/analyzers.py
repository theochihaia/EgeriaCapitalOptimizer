from typing import List
from typing import Optional
import pandas as pd
from datetime import datetime


import yfinance as yf
from src.common.enums.metric import Metric, MetricResult
from src.common.models.AnalysisResult import AnalysisResult
from src.utilities.algorithms.range_analyzer import RangeAnalysisConfig, range_analyzer

# Constants
PE_THRESHOLD_HIGH = 30
PE_THRESHOLD_LOW = 10
PB_THRESHOLD_HIGH = 9
PB_THRESHOLD_LOW = 1
PS_THRESHOLD_HIGH = 15
PS_THRESHOLD_LOW = 1
BETA_THRESHOLD_HIGH = 1.2
BETA_THRESHOLD_LOW = 0.5
TEN_YR_RETURN_HIGH = 200
TEN_YR_RETURN_LOW = 100

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
        Metric.TEN_YEAR_RETURN: analyze_ten_year_return,
        Metric.FIFTY_DAY_AVG: analyze_fifty_day_avg,
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
    config = RangeAnalysisConfig(
        metric=Metric.PRICE_TO_SALES,
        threshold_high=PS_THRESHOLD_HIGH,
        threshold_low=PS_THRESHOLD_LOW,
        fetch_data=lambda ticker: ticker.info.get("priceToSalesTrailing12Months")
    )
    return range_analyzer(ticker, config)


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
    config = RangeAnalysisConfig(
        metric=Metric.BETA,
        threshold_high=BETA_THRESHOLD_HIGH,
        threshold_low=BETA_THRESHOLD_LOW,
        fetch_data=lambda ticker: ticker.info.get("beta")
    )
    return range_analyzer(ticker, config)

def analyze_revenue_deviation(
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    
    # Get Revenue list for ticker
    total_revenue = []
    for(key, value) in ticker.get_income_stmt().items():
        total_revenue.append(value.get("TotalRevenue"))

    # Get latest Revenue
    latest_revenue = total_revenue[0]

    # Determine avg and standard deviation of Revenue
    revenue_avg = pd.Series(total_revenue).mean()
    revenue_std = pd.Series(total_revenue).std()
    
    config = RangeAnalysisConfig(
        metric=Metric.TOTAL_REVENUE_DEVIATION,
        threshold_high=revenue_avg + revenue_std,
        threshold_low=revenue_avg - revenue_std,
        fetch_data=lambda ticker: latest_revenue
    )
    return range_analyzer(ticker, config, invert=True)


def analyze_ebidta_deviation(
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    
    # Get Revenue list for ticker
    ebidta = []
    for(key, value) in ticker.get_income_stmt().items():
        ebidta.append(value.get("NormalizedEBITDA"))

    # Get latest Revenue
    latest_ebidta = ebidta[0]

    # Determine avg and standard deviation of Revenue
    ebidta_avg = pd.Series(ebidta).mean()
    ebidta_std = pd.Series(ebidta).std()
    
    config = RangeAnalysisConfig(
        metric=Metric.NORMALIZED_EBIDTA_DEVIATION,
        threshold_high=ebidta_avg + ebidta_std,
        threshold_low=ebidta_avg - ebidta_std,
        fetch_data=lambda ticker: latest_ebidta
    )
    return range_analyzer(ticker, config, invert=True)


def analyze_ten_year_return(    
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    data = ticker.history(period="10y")

    latest_price = data["Close"].iloc[-1]
    initial_price = data["Close"].iloc[0]
    ten_year_return = (latest_price - initial_price) / initial_price * 100

    config = RangeAnalysisConfig(
        metric=Metric.TEN_YEAR_RETURN,
        threshold_high=TEN_YR_RETURN_HIGH,
        threshold_low=TEN_YR_RETURN_LOW,
        fetch_data=lambda ticker: ten_year_return
    )
    return range_analyzer(ticker, config, invert=True)


def analyze_fifty_day_avg(    
    ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_bollinger_bands not implemented")

def analyze_bollinger_bands(    
        ticker: yf.Ticker
) -> Optional[AnalysisResult]:
    raise NotImplementedError("analyze_bollinger_bands not implemented")

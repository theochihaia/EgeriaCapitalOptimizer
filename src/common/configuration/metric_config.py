import yfinance as yf
import numpy as np

from src.common.models.MetricConfig import MetricConfig
from src.common.enums.metric import Metric

METRIC_CONFIG = {
    Metric.PRICE_TO_EARNINGS: MetricConfig(
        stat_key="PE",
        data_fetcher=lambda t: t.info.get("forwardPE") or t.info.get("trailingPE"),
        metric_weight=2,
        is_inverted=True
    ),
    Metric.PRICE_TO_BOOK: MetricConfig(
        stat_key="PB",
        data_fetcher=lambda t: t.info.get("priceToBook"),
        metric_weight=1,
        is_inverted=True
    ),
    Metric.PRICE_TO_SALES: MetricConfig(
        stat_key="PS",
        data_fetcher=lambda t: t.info.get("priceToSalesTrailing12Months"),
        metric_weight=1,
        is_inverted=True
    ),
    Metric.BETA: MetricConfig(
        stat_key="BETA",
        data_fetcher=lambda t: t.info.get("beta"),
        metric_weight=5,
        is_inverted=True
    ),
    Metric.FIVE_YEAR_RETURN: MetricConfig(
        stat_key="RETURN_5_YR",
        data_fetcher=lambda t: get_return(t, "5y"),
        metric_weight=5,
        is_inverted=False
    ),
    Metric.TEN_YEAR_RETURN: MetricConfig(
        stat_key="RETURN_10_YR",
        data_fetcher=lambda t: get_return(t, "10y"),
        metric_weight=5,
        is_inverted=False
    ),
    Metric.FIVE_YEAR_VARIANCE: MetricConfig(
        stat_key="VARIANCE_5_YR",
        data_fetcher=lambda t: get_variance(t, "5y"),
        metric_weight=4,
        is_inverted=True
    ),
    Metric.TEN_YEAR_VARIANCE: MetricConfig(
        stat_key="VARIANCE_10_YR",
        data_fetcher=lambda t: get_variance(t, "10y"),
        metric_weight=4,
        is_inverted=True
    ),
    Metric.QUICK_RATIO: MetricConfig(
        stat_key="QUICK_RATIO",
        data_fetcher=lambda t: t.info.get("quickRatio"),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.DEBT_TO_EQUITY: MetricConfig(
        stat_key="DEBT_TO_EQUITY",
        data_fetcher=lambda t: t.info.get("debtToEquity"),
        metric_weight=2,
        is_inverted=True
    ),
    Metric.YIELD: MetricConfig(
        stat_key="YIELD",
        data_fetcher=lambda t: t.info.get("fiveYearAvgDividendYield"),
        metric_weight=1,
        is_inverted=False
    ),
    Metric.EBIDTA_MARGIN: MetricConfig(
        stat_key="EBIDTA_MARGIN",
        data_fetcher=lambda t: t.info.get("ebitdaMargins"),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.EBIDTA_AVG_GROWTH_RATE: MetricConfig(
        stat_key="EBIDTA_GROWTH_RATE",
        data_fetcher=lambda t: get_income_growth(t, "NormalizedEBITDA"),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.REVENUE_AVG_GROWTH_RATE: MetricConfig(
        stat_key="REVENUE_GROWTH_RATE",
        data_fetcher=lambda t: get_income_growth(t, "TotalRevenue"),
        metric_weight=3,
        is_inverted=False
    ),
}


def get_return(ticker: yf.Ticker, period: str):
    data = ticker.history(period=period)
    if data.empty:
        return

    latest_price = data["Close"].iloc[-1]
    initial_price = data["Close"].iloc[0]
    return (latest_price - initial_price) / initial_price * 100


def get_income_growth(ticker: yf.Ticker, data_point: str):

    data = []
    for key, value in ticker.get_income_stmt().items():
        data.append(value.get(data_point))

    if len(data) < 2:
        return None

    avgGrowthRate = 0
    for i in range(len(data) - 1):
        if data[i + 1] is None or data[i] is None:
            continue
        avgGrowthRate += (data[i] - data[i + 1]) / data[i + 1]
        
    avgGrowthRate /= len(data) - 1
    return avgGrowthRate * 100

def get_n_day_returns(data_close, days):
    five_day_returns = []
    for i in range(0, len(data_close) - days, days):
        if data_close.iloc[i + days] is None or data_close.iloc[i] is None or data_close.iloc[i] == 0:
            continue
        five_day_returns.append((data_close.iloc[i + days] - data_close.iloc[i]) / data_close.iloc[i])
    return five_day_returns

def get_variance(ticker: yf.Ticker, period: str):
    data = ticker.history(period=period)
    day_period = 10
    data_close = data["Close"]
    if data.empty:
        return

    n_day_returns = get_n_day_returns(data_close, day_period)
    if len(n_day_returns) == 0:
        return None
    
    variance = np.var(n_day_returns)
    return variance * 100
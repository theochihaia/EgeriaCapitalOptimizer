import yfinance as yf
import numpy as np

from src.common.utils.ticker_util import get_return, get_income_growth, get_variance

from src.common.models.MetricConfig import MetricConfig
from src.common.enums.metric import Metric

METRIC_CONFIG = {
    Metric.PRICE_TO_EARNINGS: MetricConfig(
        data_fetcher=lambda t: t.info.get("forwardPE") or t.info.get("trailingPE"),
        metric_weight=1,
        is_inverted=True
    ),
    Metric.PRICE_TO_BOOK: MetricConfig(
        data_fetcher=lambda t: t.info.get("priceToBook"),
        metric_weight=1,
        is_inverted=True
    ),
    Metric.PRICE_TO_SALES: MetricConfig(
        data_fetcher=lambda t: t.info.get("priceToSalesTrailing12Months"),
        metric_weight=1,
        is_inverted=True
    ),
    Metric.BETA: MetricConfig(
        data_fetcher=lambda t: t.info.get("beta"),
        metric_weight=5,
        is_inverted=True
    ),
    Metric.RETURN_FIVE_YEAR: MetricConfig(
        data_fetcher=lambda t: get_return(t, "5y"),
        metric_weight=5,
        is_inverted=False
    ),
    Metric.RETURN_TEN_YEAR: MetricConfig(
        data_fetcher=lambda t: get_return(t, "10y"),
        metric_weight=5,
        is_inverted=False
    ),
    Metric.VARIANCE_FIVE_YEAR: MetricConfig(
        data_fetcher=lambda t: get_variance(t, "5y"),
        metric_weight=4,
        is_inverted=True
    ),
    Metric.VARIANCE_TEN_YEAR: MetricConfig(
        data_fetcher=lambda t: get_variance(t, "10y"),
        metric_weight=4,
        is_inverted=True
    ),
    Metric.QUICK_RATIO: MetricConfig(
        data_fetcher=lambda t: t.info.get("quickRatio"),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.DEBT_TO_EQUITY: MetricConfig(
        data_fetcher=lambda t: t.info.get("debtToEquity"),
        metric_weight=2,
        is_inverted=True
    ),
    Metric.YIELD: MetricConfig(
        data_fetcher=lambda t: t.info.get("fiveYearAvgDividendYield"),
        metric_weight=1,
        is_inverted=False
    ),
    Metric.EBIDTA_MARGIN: MetricConfig(
        data_fetcher=lambda t: t.info.get("ebitdaMargins"),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.RETURN_ON_EQUITY: MetricConfig(
        data_fetcher=lambda t: t.info.get("returnOnEquity"),
        metric_weight=2,
        is_inverted=False
    ),
    Metric.RETURN_ON_ASSETS: MetricConfig(
        data_fetcher=lambda t: t.info.get("returnOnAssets"),
        metric_weight=2,
        is_inverted=False
    ),
    Metric.EBIDTA_AVG_GROWTH_RATE: MetricConfig(
        data_fetcher=lambda t: get_income_growth(t, "NormalizedEBITDA"),
        metric_weight=1,
        is_inverted=False
    ),
    Metric.REVENUE_AVG_GROWTH_RATE: MetricConfig(
        data_fetcher=lambda t: get_income_growth(t, "TotalRevenue"),
        metric_weight=1,
        is_inverted=False
    ),
}

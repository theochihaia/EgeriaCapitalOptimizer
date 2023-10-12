import yfinance as yf
import numpy as np

from src.common.utils.ticker_util import get_return, get_income_growth, get_variance

from src.common.models.MetricConfig import MetricConfig
from src.common.enums.metric import Metric

METRIC_CONFIG = {
    Metric.PRICE_TO_EARNINGS: MetricConfig(
        stat_key="PE",
        data_fetcher=lambda t: t.info.get("forwardPE") or t.info.get("trailingPE"),
        metric_weight=1,
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
        metric_weight=1,
        is_inverted=False
    ),
    Metric.REVENUE_AVG_GROWTH_RATE: MetricConfig(
        stat_key="REVENUE_GROWTH_RATE",
        data_fetcher=lambda t: get_income_growth(t, "TotalRevenue"),
        metric_weight=1,
        is_inverted=False
    ),
}

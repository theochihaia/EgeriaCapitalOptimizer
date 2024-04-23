import yfinance as yf
import numpy as np

from src.common.utils.ticker_util import get_return, get_income_growth, get_std, get_quick_ratio, get_debt_to_equity_ratio, get_pe_ratio, get_ps_ratio, get_ebidta_margin, get_beta, get_cashflow_growth

from src.common.models.MetricConfig import MetricConfig
from src.common.enums.metric import Metric

METRIC_CONFIG = {
    Metric.BETA: MetricConfig(
        data_fetcher=lambda t: get_beta(t.ticker),
        metric_weight=4,
        is_inverted=True
    ),
    Metric.DEBT_TO_EQUITY: MetricConfig(
        data_fetcher=lambda t: get_debt_to_equity_ratio(t),
        metric_weight=2,
        is_inverted=True
    ),
    Metric.EBIDTA_AVG_GROWTH_RATE: MetricConfig(
        data_fetcher=lambda t: get_income_growth(t, "NormalizedEBITDA"),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.EBIDTA_MARGIN: MetricConfig(
        data_fetcher=lambda t: get_ebidta_margin(t),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.PRICE_TO_BOOK: MetricConfig(
        data_fetcher=lambda t: t.info.get("priceToBook"),
        metric_weight=1,
        is_inverted=True
    ),
    Metric.PRICE_TO_EARNINGS: MetricConfig(
        data_fetcher=lambda t: get_pe_ratio(t),
        metric_weight=1,
        is_inverted=True
    ),
    Metric.PRICE_TO_SALES: MetricConfig(
        data_fetcher=lambda t: get_ps_ratio(t),
        metric_weight=1,
        is_inverted=True
    ),
    Metric.QUICK_RATIO: MetricConfig(
        data_fetcher=lambda t: get_quick_ratio(t),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.RETURN_FIVE_YEAR: MetricConfig(
        data_fetcher=lambda t: get_return(t, "5y"),
        metric_weight=4,
        is_inverted=False
    ),
    Metric.RETURN_ON_ASSETS: MetricConfig(
        data_fetcher=lambda t: t.info.get("returnOnAssets"),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.RETURN_ON_EQUITY: MetricConfig(
        data_fetcher=lambda t: t.info.get("returnOnEquity"),
        metric_weight=4,
        is_inverted=False
    ),
    Metric.RETURN_TEN_YEAR: MetricConfig(
        data_fetcher=lambda t: get_return(t, "10y"),
        metric_weight=4,
        is_inverted=False
    ),
    Metric.REVENUE_AVG_GROWTH_RATE: MetricConfig(
        data_fetcher=lambda t: get_income_growth(t, "TotalRevenue"),
        metric_weight=1,
        is_inverted=False
    ),
    Metric.STD_FIVE_YEAR: MetricConfig(
        data_fetcher=lambda t: get_std(t, "5y"),
        metric_weight=3,
        is_inverted=True
    ),
    Metric.STD_TEN_YEAR: MetricConfig(
        data_fetcher=lambda t: get_std(t, "10y"),
        metric_weight=3,
        is_inverted=True
    ),
    Metric.YIELD: MetricConfig(
        data_fetcher=lambda t: t.info.get("fiveYearAvgDividendYield"),
        metric_weight=2,
        is_inverted=False
    ),
    Metric.FREE_CASHFLOW_GROWTH: MetricConfig(
        data_fetcher=lambda t: get_cashflow_growth(t,"FreeCashFlow"),
        metric_weight=5,
        is_inverted=False
    ),
}


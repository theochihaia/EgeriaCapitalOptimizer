import yfinance as yf

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
        metric_weight=4,
        is_inverted=True
    ),
    Metric.NORMALIZED_EBIDTA_DEVIATION: MetricConfig(
        stat_key="NORMALIZED_EBIDTA_DEVIATION",
        data_fetcher=lambda t: t.info.get("ebitda"),
        metric_weight=3,
        is_inverted=False
    ),
    Metric.TOTAL_REVENUE_DEVIATION: MetricConfig(
        stat_key="TOTAL_REVENUE_DEVIATION",
        data_fetcher=lambda t: t.info.get("totalRevenue"),
        metric_weight=3,
        is_inverted=False
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
    Metric.FIFTY_DAY_AVG: MetricConfig(
        stat_key="50_DAY_AVG",
        data_fetcher=lambda t: t.info.get("fiftyDayAverage"),
        metric_weight=3,
        is_inverted=False
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
        metric_weight=3,
        is_inverted=True
    ),
    Metric.YIELD: MetricConfig(
        stat_key="YIELD",
        data_fetcher=lambda t: t.info.get("fiveYearAvgDividendYield"),
        metric_weight=1,
        is_inverted=False
    )
}


def get_return(ticker: yf.Ticker, period: str):
    data = ticker.history(period=period)
    if data.empty:
        return

    latest_price = data["Close"].iloc[-1]
    initial_price = data["Close"].iloc[0]
    return (latest_price - initial_price) / initial_price * 100


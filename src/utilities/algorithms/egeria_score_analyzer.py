from dataclasses import dataclass
from typing import Optional, Callable, Union

import yfinance as yf

from src.common.enums.metric import Metric, MetricResult
from src.common.models.AnalysisResult import AnalysisResult

@dataclass
class RangeAnalysisConfig:
    metric: Metric
    threshold_high: float
    threshold_low: float
    fetch_data: Callable[[yf.Ticker], Union[float, None]]

def range_analyzer(ticker: yf.Ticker, config: RangeAnalysisConfig) -> Optional[AnalysisResult]:
    value = config.fetch_data(ticker)
    symbol = ticker.get_info().get("symbol")

    if not value:
        return None

    if value > config.threshold_high:
        message = f"{symbol} HIGH {config.metric.value} : {value}"
        result = MetricResult.NEGATIVE
    elif value < config.threshold_low:
        message = f"{symbol} LOW {config.metric.value} : {value}"
        result = MetricResult.POSITIVE
    else:
        message = f"{symbol} NEUTRAL {config.metric.value} : {value}"
        result = MetricResult.NEUTRAL

    return AnalysisResult(symbol, config.metric, message, result)

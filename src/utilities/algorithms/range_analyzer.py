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

def range_analyzer(symbol: str, ticker: yf.Ticker, config: RangeAnalysisConfig) -> Optional[AnalysisResult]:
    value = config.fetch_data(ticker)
    
    if not value:
        return None

    if value > config.threshold_high:
        message = f"{symbol} has a high {config.metric.value} ratio of {value}"
        result = MetricResult.NEGATIVE
    elif value < config.threshold_low:
        message = f"{symbol} has a low {config.metric.value} ratio of {value}"
        result = MetricResult.POSITIVE
    else:
        message = f"{symbol} has a neutral {config.metric.value} ratio of {value}"
        result = MetricResult.NEUTRAL

    return AnalysisResult(symbol, config.metric, message, result)

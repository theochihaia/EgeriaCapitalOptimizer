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

def range_analyzer(ticker: yf.Ticker, config: RangeAnalysisConfig, invert: bool = False) -> Optional[AnalysisResult]:
    value = config.fetch_data(ticker)
    symbol = ticker.get_info().get("symbol")

    high_result_value = MetricResult.NEGATIVE if not invert else MetricResult.POSITIVE
    low_result_value = MetricResult.POSITIVE if not invert else MetricResult.NEGATIVE

    if not value:
        return None

    message = ""
    if value > config.threshold_high:
        message = f"{value} 🔺"
        result = high_result_value
    elif value < config.threshold_low:
        message = f"{value} 🔻"
        result = low_result_value
    else:
        message = f"{value} ◼"
        result = MetricResult.NEUTRAL

    return AnalysisResult(symbol, config.metric, message, result)

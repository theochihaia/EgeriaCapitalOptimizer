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

    # Convert the value to float and format it with commas and two decimal places
    display_value = "{:,.2f}".format(round(float(value), 2))

    message = ""
    if value > config.threshold_high:
        message = display_value
        result = high_result_value
    elif value < config.threshold_low:
        message = f"{display_value}"
        result = low_result_value
    else:
        message = f"{display_value}"
        result = MetricResult.NEUTRAL

    return AnalysisResult(symbol, config.metric, message, result)

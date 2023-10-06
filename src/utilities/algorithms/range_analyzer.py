from dataclasses import dataclass
from typing import Optional, Callable, Union

import yfinance as yf

from src.common.enums.metric import Metric, MetricResult
from src.common.models.AnalysisResult import AnalysisResult

@dataclass
class RangeAnalysisConfig:
    metric: Metric
    avg: float
    std: float
    fetch_data: Callable[[yf.Ticker], Union[float, None]]

def range_analyzer(ticker: yf.Ticker, config: RangeAnalysisConfig, invert: bool = False) -> Optional[AnalysisResult]:
    value = config.fetch_data(ticker)
    symbol = ticker.get_info().get("symbol")

    positive_result = MetricResult.POSITIVE if not invert else MetricResult.NEGATIVE
    negative_result = MetricResult.NEGATIVE if not invert else MetricResult.POSITIVE
    multiplier = (-1 if invert else 1)

    if value is None:
        return None

    # Convert the value to float and format it with commas and two decimal places
    display_value = "{:,.2f}".format(round(float(value), 2))

    message = ""
    if value > config.avg + config.std:
        message = display_value
        result = positive_result
    elif value < config.avg - config.std:
        message = f"{display_value}"
        result = negative_result
    else:
        message = f"{display_value}"
        result = MetricResult.NEUTRAL

    normalized_value = (value - config.avg) / config.std * multiplier
    normalized_value = 3 if normalized_value > 3 else normalized_value
    normalized_value = -3 if normalized_value < -3 else normalized_value
    
    return AnalysisResult(symbol, config.metric, message, result, normalized_value ,invert)


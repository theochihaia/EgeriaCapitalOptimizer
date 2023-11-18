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

def range_normalizer(symbol: str, ticker: yf.Ticker, config: RangeAnalysisConfig, invert: bool = False) -> Optional[AnalysisResult]:
    value = None
    try:
        value = config.fetch_data(ticker)
    except Exception as e:
        print(f"Error fetching {config.metric} for {symbol}: {e}")
        return None
    
    if value is None:
        return None
    
    symbol = ticker.ticker

    positive_result = MetricResult.POSITIVE if not invert else MetricResult.NEGATIVE
    negative_result = MetricResult.NEGATIVE if not invert else MetricResult.POSITIVE
    multiplier = (-1 if invert else 1)

    # Convert the value to float and format it with commas and two decimal places
    display_value = ""
    try:
        display_value = "{:,.2f}".format(round(float(value), 2))
    except Exception as e:
        print(f"Error formatting {config.metric} for {symbol}. Value {value}")
        return None

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


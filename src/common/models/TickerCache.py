from dataclasses import dataclass
from ..enums.metric import Metric, MetricResult


@dataclass
class TickerCache:
    symbol: str
    name: str
    TickerJSON: str
    TradingDataJSON: str
    DateTimeCreated: int
    DateTimeUpdated: int
    ExpirationDateTime: int
    
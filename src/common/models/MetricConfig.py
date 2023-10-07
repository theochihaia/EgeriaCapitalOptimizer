from dataclasses import dataclass
from typing import Callable
from ..enums.metric import Metric, MetricResult


@dataclass
class MetricConfig:
    stat_key: str
    data_fetcher: Callable
    metric_weight: float = 1.0
    is_inverted: bool = False

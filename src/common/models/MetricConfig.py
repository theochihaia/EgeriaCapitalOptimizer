from dataclasses import dataclass
from typing import Callable
from ..enums.metric import Metric, MetricResult


@dataclass
class MetricConfig:
    data_fetcher: Callable
    metric_weight: float = 1.0
    is_inverted: bool = False

from dataclasses import dataclass
from ..enums.metric import Metric, MetricResult


@dataclass
class AnalysisResult:
    symbol: str
    metric: Metric
    message: str
    metric_result: MetricResult
    normalized_value: float = 0.0
    is_inverted: bool = False

    def __str__(self) -> str:
        return f"{self.symbol} - {self.metric.value} {self.metric_result.value}: {self.message}"

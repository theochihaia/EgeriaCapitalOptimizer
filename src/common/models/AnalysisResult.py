from dataclasses import dataclass
from ..enums.metric import Metric, MetricResult


@dataclass
class AnalysisResult:
    symbol: str
    metric: Metric
    message: str
    result: MetricResult

    def __str__(self) -> str:
        return f"{self.symbol} - {self.metric.value} ({self.result.value}): {self.message})"

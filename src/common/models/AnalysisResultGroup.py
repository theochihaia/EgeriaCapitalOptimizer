import yfinance as yf
from dataclasses import dataclass
from ..enums.metric import Metric, MetricResult
from ..models.AnalysisResult import AnalysisResult


@dataclass
class AnalysisResultGroup:
    symbol: str
    results: list[AnalysisResult]
    egeria_score: float
    ticker: yf.Ticker


    def __str__(self) -> str:
        # Only display symbols with non-empty analysis
        output = ""
        if self.results:
            output += "{symbol} - {name} ({sector})\n".format(symbol=self.symbol, name=self.ticker.get_info().get("longName"), sector=self.ticker.get_info().get("sector"))
            output += f"Egeria Score: {self.egeria_score}\n"
            for res in self.results:
                if res is not None:
                    output += f"  {res.metric_result.value} {res.metric.value}: {res.message}\n"
            output += "\n"
        return output
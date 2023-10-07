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
            sector = "Default"
            name = "Unknown"

            if self.ticker and self.ticker.get_info():
                ticker_info = self.ticker.get_info()
                sector = ticker_info.get("sector")
                name = ticker_info.get("longName")

            output += "{symbol} - {name} ({sector})\n".format(symbol=self.symbol, name=name, sector=sector)
            output += f"Egeria Score: {self.egeria_score}\n"
            for res in self.results:
                if res is not None:
                    output += f"  {res.metric_result.value} {res.metric.value}: {res.message}\n"
            output += "\n"
        return output
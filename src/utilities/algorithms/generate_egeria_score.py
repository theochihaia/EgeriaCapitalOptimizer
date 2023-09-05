from dataclasses import dataclass, field
from ...common.enums.metric import Metric, MetricResult
import yfinance as yf

# The goal here is to iterate through all symbols, 
# normalize each parameter and create a score
@dataclass
class EgeriaScore:
    symbol: str
    score: float
    metric_score: dict[Metric, float]
    _ticker_data: yf.Ticker = field(repr=False, init=False)  # make it private and non-init
    _metrics: list[Metric] = field(repr=False, init=False)  # make it private and non-init

    def __init__(self, ticker_data, metrics):
        self.symbol = ticker_data.get_info().get("symbol")
        self._ticker_data = ticker_data
        self._metrics = metrics
        self.metric_score = generate_metric_score(ticker_data, metrics)
        self.score = sum(self.metric_score.values())

    @property
    def ticker_data(self):
        return self._ticker_data

    @property
    def metrics(self):
        return self._metrics

    def __str__(self) -> str:
        return f"{self.symbol} - score: {self.score}"

    #----------------------------------------------#

# Need to handle negative score
def get_data_point(ticker: yf.Ticker, metrics: [Metric]) -> [float]:
    data_lookup = {
        Metric.PRICE_TO_EARNINGS: ticker.info.get("trailingPE") or ticker.info.get("forwardPE"),
        Metric.PRICE_TO_BOOK: ticker.info.get("priceToBook"),
        Metric.PRICE_TO_SALES: ticker.info.get("priceToSalesTrailing12Months"),
        Metric.BETA: ticker.info.get("beta"),
    }
    return data_lookup.get(metrics)

def generate_metric_score(ticker: yf.Ticker, metrics: [Metric]) -> dict[Metric, float]:
    metric_score = {}
    for metric in metrics:
        metric_score[metric] = normalize(metric, get_data_point(ticker, metric))
    return metric_score


def normalize(metric: Metric, value: float):
    metric_range = {
        Metric.PRICE_TO_EARNINGS: (5, 50),
        Metric.PRICE_TO_BOOK: (.5, 10),
        Metric.PRICE_TO_SALES: (1, 5),
        Metric.BETA: (.5, 2),
    }
    low, high = metric_range.get(metric)

    if value is None or low is None or high is None:
        return 0
    
    return (value - low) / (high - low) * 100



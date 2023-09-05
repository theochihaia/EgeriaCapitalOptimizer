from enum import Enum


class Metric(Enum):
    PRICE_TO_EARNINGS = "P/E Ratio"
    PRICE_TO_BOOK = "Price/Book"
    PRICE_TO_SALES = "Price/Sales"
    PRICE_TO_CASHFLOW = "Price/Cashflow"
    STANDARD_DEVIATION = "Standard Deviation"
    BETA = "Beta"
    BOLLINGER_BANDS = "Bollinger Bands"
    EBIDTA_GROWTH = "EBIDTA Growth"
    REVENUE_GROWTH = "Revenue Growth"
    TEN_YEAR_RETURN = "10 Year Return"
    FIVE_YEAR_RETURN = "5 Year Return"
    EGERIA_SCORE = "Egeria Score"


class MetricResult(Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"

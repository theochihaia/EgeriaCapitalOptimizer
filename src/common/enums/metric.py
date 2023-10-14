from enum import Enum


class Metric(Enum):
    PRICE_TO_EARNINGS = "P/E Ratio"
    PRICE_TO_BOOK = "Price/Book"
    PRICE_TO_SALES = "Price/Sales"
    PRICE_TO_CASHFLOW = "Price/Cashflow"
    STANDARD_DEVIATION = "Standard Deviation"
    BETA = "Beta"
    TEN_YEAR_RETURN = "10 Year Return"
    FIVE_YEAR_RETURN = "5 Year Return"
    FIVE_YEAR_VARIANCE = "5 Year Variance"
    TEN_YEAR_VARIANCE = "10 Year Variance"
    FIFTY_DAY_AVG = "50 Day Average"
    BOLLINGER_BANDS = "Bollinger Bands"
    QUICK_RATIO = "Quick Ratio"
    DEBT_TO_EQUITY = "Debt/Equity"
    EBIDTA_MARGIN = "EBIDTA Margin"
    RETURN_ON_EQUITY = "Return on Equity"
    RETURN_ON_ASSETS = "Return on Assets"
    YIELD = "Yield"
    EGERIA_SCORE = "Egeria Score"
    EBIDTA_AVG_GROWTH_RATE = "EBIDTA Avg Growth Rate"
    REVENUE_AVG_GROWTH_RATE = "Revenue Avg Growth Rate"

class MetricResult(Enum):
    POSITIVE = "✅"
    NEGATIVE = "❌"
    NEUTRAL = "🟡"

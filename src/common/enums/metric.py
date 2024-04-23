from enum import Enum


class Metric(Enum):
    PRICE_TO_EARNINGS = "P/E Ratio"
    PRICE_TO_BOOK = "Price/Book"
    PRICE_TO_SALES = "Price/Sales"
    PRICE_TO_CASHFLOW = "Price/Cashflow"
    STANDARD_DEVIATION = "Standard Deviation"
    BETA = "Beta"
    RETURN_TEN_YEAR = "10 Year Return"
    RETURN_FIVE_YEAR = "5 Year Return"
    STD_FIVE_YEAR = "5 Year STD"
    STD_TEN_YEAR = "10 Year STD"
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
    FREE_CASHFLOW_GROWTH = "Free Cashflow Growth"

class MetricResult(Enum):
    POSITIVE = "✅"
    NEGATIVE = "❌"
    NEUTRAL = "🟡"

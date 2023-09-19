from enum import Enum


class Metric(Enum):
    PRICE_TO_EARNINGS = "P/E Ratio"
    PRICE_TO_BOOK = "Price/Book"
    PRICE_TO_SALES = "Price/Sales"
    PRICE_TO_CASHFLOW = "Price/Cashflow"
    STANDARD_DEVIATION = "Standard Deviation"
    BETA = "Beta"
    TOTAL_REVENUE_DEVIATION = "Total Revenue Deviation"
    NORMALIZED_EBIDTA_DEVIATION = "EBIDTA Deviation"
    TEN_YEAR_RETURN = "10 Year Return"
    FIVE_YEAR_RETURN = "5 Year Return"
    FIFTY_DAY_AVG = "50 Day Average"
    BOLLINGER_BANDS = "Bollinger Bands"
    QUICK_RATIO = "Quick Ratio"
    DEBT_TO_EQUITY = "Debt/Equity"
    EBIDTA_GROWTH = "EBIDTA Growth"
    REVENUE_GROWTH = "Revenue Growth"
    EGERIA_SCORE = "Egeria Score"


class MetricResult(Enum):
    POSITIVE = "🟢"
    NEGATIVE = "🔴"
    NEUTRAL = "🟡"

from enum import Enum


class EquityDataCategory(Enum):
    INFO = "info"
    FAST_INFO = "fast_info"
    HISTORY = "history"  # Requires parameter e.g., period="1mo"
    HISTORY_METADATA = "history_metadata"
    ACTIONS = "actions"
    DIVIDENDS = "dividends"
    SPLITS = "splits"
    CAPITAL_GAINS = "capital_gains"  # Only for mutual funds & ETFs
    GET_SHARES_FULL = (
        "get_shares_full"  # Requires parameters e.g., start="2000-01-01", end=None
    )
    INCOME_STMT = "income_stmt"
    QUARTERLY_INCOME_STMT = "quarterly_income_stmt"
    BALANCE_SHEET = "balance_sheet"
    QUARTERLY_BALANCE_SHEET = "quarterly_balance_sheet"
    CASHFLOW = "cashflow"
    QUARTERLY_CASHFLOW = "quarterly_cashflow"
    MAJOR_HOLDERS = "major_holders"
    INSTITUTIONAL_HOLDERS = "institutional_holders"
    MUTUALFUND_HOLDERS = "mutualfund_holders"
    ISIN = "isin"  # Experimental
    OPTIONS = "options"
    NEWS = "news"

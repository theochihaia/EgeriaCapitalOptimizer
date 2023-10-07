'''
https://www.gurufocus.com/economic_indicators/4238/sp-500-price-to-sales
    IX 0 = Avg
    IX 1 = Std Dev

Metric  Avg     Deviation
P/E     24.2    15.8
P/B     2.92    0.68
P/S     1.76    0.54
Beta    0.8     0.4
Q/R     1       0.5
D/E     100     50
5 YR    50      25
10 YR	150     75
Yield	1.19    1.11
'''

SECTOR_METRIC_STATISTICS_STR = """
Metric      Avg         Deviation
P/E         24.2        15.8
P/B         2.92        0.68
P/S         1.76        0.54
Beta        1.0         0.2
Yield       0.00        1.00
Q/R         1           0.5
D/E         100         50
Var 5 YR    0.7         0.3
var 10 YR   0.7         0.3
EBTAMRGN    0.2         0.1
EBTAGROW    15          5
REVGROW     15          5
5 YR        50          25
10 YR	    150         75

"""

SECTOR_METRIC_STATISTICS = {
    "Default": {
        "PE": (24.2, 15.8),
        "PB": (2.92, .68),
        "PS": (1.76, .54),
        "BETA": (1, .2),
        "QUICK_RATIO": (1, .5),
        "DEBT_TO_EQUITY": (100, 50),
        "RETURN_5_YR": (50, 25),
        "RETURN_10_YR": (150, 75),
        "VARIANCE_5_YR": (.7, .3),
        "VARIANCE_10_YR": (.7, .3),
        "YIELD": (0, 1),
        "EBIDTA_MARGIN": (.2, .1),
        "EBIDTA_GROWTH_RATE": (15, 5),
        "REVENUE_GROWTH_RATE": (15, 5)
    },
    "Healthcare": {

    },
    "Basic Materials": {

    },
    "Industrials": {

    },
    "Technology": {

    },
    "Consumer Cyclical": {

    },
    "Consumer Defensive": {

    },
    "Utilities": {

    },
    "Financial Services": {

    },
    "Communication Services": {

    }
}

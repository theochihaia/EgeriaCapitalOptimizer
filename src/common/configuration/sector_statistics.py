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

SECTOR_METRIC_STATISTICS = {
    "Default": {
        "BETA": (.8, .2),
        "DEBT_TO_EQUITY": (100, 50),
        "EBIDTA_AVG_GROWTH_RATE": (15, 5),
        "EBIDTA_MARGIN": (.2, .1),
        "PRICE_TO_BOOK": (2.92, .68),
        "PRICE_TO_EARNINGS": (24.2, 15.8),
        "PRICE_TO_SALES": (1.76, .54),
        "QUICK_RATIO": (1, .5),
        "RETURN_FIVE_YEAR": (50, 25),
        "RETURN_ON_ASSETS": (.05, .03),
        "RETURN_ON_EQUITY": (.15, .07),
        "RETURN_TEN_YEAR": (150, 75),
        "REVENUE_AVG_GROWTH_RATE": (15, 5),
        "VARIANCE_FIVE_YEAR": (.7, .3),
        "VARIANCE_TEN_YEAR": (.7, .3),
        "YIELD": (0, 1),
    }
}

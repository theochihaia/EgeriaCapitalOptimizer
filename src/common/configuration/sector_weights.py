# Depricated: 10/05/2023
SECTOR_METRIC_THRESHOLDS = {
    "Default": {
        "PE": (14, 30),
        "PB": (1, 9),
        "PS": (1, 15),
        "BETA": (0.7, 1.2),
        "QUICK_RATIO": (1, 2),
        "DEBT_TO_EQUITY": (0.5, 2)
    },
    "Healthcare": {
        "PE": (15, 35),
        "PB": (2, 8),
        "PS": (2, 15),
        "BETA": (0.7, 1.3),
        "QUICK_RATIO": (0.8, 2.5),
        "DEBT_TO_EQUITY": (0.3, 1.5)
    },
    "Basic Materials": {
        "PE": (10, 25),
        "PB": (1, 4),
        "PS": (0.7, 3),
        "BETA": (0.7, 1.4),
        "QUICK_RATIO": (0.7, 2),
        "DEBT_TO_EQUITY": (0.5, 3)
    },
    "Industrials": {
        "PE": (14, 25),
        "PB": (1.5, 5),
        "PS": (0.6, 4),
        "BETA": (0.7, 1.3),
        "QUICK_RATIO": (0.8, 2.2),
        "DEBT_TO_EQUITY": (0.7, 2.5)
    },
    "Technology": {
        "PE": (15, 50),
        "PB": (5, 20),
        "PS": (3, 20),
        "BETA": (0.7, 1.5),
        "QUICK_RATIO": (1, 3),
        "DEBT_TO_EQUITY": (0.2, 1.2)
    },
    "Consumer Cyclical": {
        "PE": (14, 30),
        "PB": (2, 10),
        "PS": (0.6, 5),
        "BETA": (0.7, 1.4),
        "QUICK_RATIO": (0.6, 2),
        "DEBT_TO_EQUITY": (0.5, 2.5)
    },
    "Consumer Defensive": {
        "PE": (14, 25),
        "PB": (2, 8),
        "PS": (0.7, 4),
        "BETA": (0.7, 1.2),
        "QUICK_RATIO": (0.8, 2.5),
        "DEBT_TO_EQUITY": (0.3, 1.8)
    },
    "Utilities": {
        "PE": (14, 20),
        "PB": (1, 4),
        "PS": (0.7, 3),
        "BETA": (0.7, 1),
        "QUICK_RATIO": (0.7, 1.5),
        "DEBT_TO_EQUITY": (1, 3.5) # Utilities tend to have higher D/E due to the capital-intensive nature of the industry.
    },
    "Financial Services": {
        "PE": (12, 20),
        "PB": (0.5, 2.5),
        "PS": (0.5, 3),
        "BETA": (0.7, 1.3),
        "QUICK_RATIO": (0.6, 1.8),
        "DEBT_TO_EQUITY": (2, 10) # Financial institutions often have higher leverage and thus higher D/E ratios.
    },
    "Communication Services": {
        "PE": (14, 30),
        "PB": (1.5, 6),
        "PS": (1, 6),
        "BETA": (0.8, 1.3),
        "QUICK_RATIO": (0.7, 2.2),
        "DEBT_TO_EQUITY": (0.5, 2.5)
    }
}

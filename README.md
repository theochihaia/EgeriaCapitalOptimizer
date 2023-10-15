# Egeria Capital Optimizer

This tool pulls trading, statistic, earnings, debt, and other data from Yahoo Finance.

Given a portfolio and a list of metrics, it will generate an Egeria Score and recommended weights for the portfolio. Data is saved as a "results_{portfolio_name}.txt" and a results_{portfolio_name}.csv.

## Getting Started

### Setting Up

1. Set up a virtual environment:
    ```bash
    python3 -m venv newenv
    source newenv/bin/activate
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

- **Add a portfolio**: 
    - `src.common.portfolios`: This is a txt file that stores a newline-delimited list of equity symbols.

- **Application Configuration**:
    - `src.common.configuration - app_config.py`: This allows the user to set the portfolio, metrics, and other configurations to run the tool.

- **Metric Configuration**:
    - `src.common.configuration - metric_config.py`: Set Metrics, their weights, and calculation function per ticker.

- **Sector Statistics**:
    - `src.common.configuration - sector_statistics.py`: For each Metric, define an avg and std range.

### Key Functionalities

- **Ticker Analysis**:
    - Analyze tickers concurrently, generate portfolio statistics, and more. Check out `analyzers.py` for detailed functionalities.

- **File Generation**:
    - Generate result files based on the analysis. Refer to `file_generator.py` for more details.

- **Monthly Returns Calculation**:
    - Calculate monthly returns of a ticker over a specified period. Explore `monthly_returns.py` to understand the process.

- **Range Normalization**:
    - Normalize ticker data based on given metrics. The `range_normalizer.py` provides detailed functionalities.

### Prerequisites

See `requirements.txt` for all necessary dependencies.

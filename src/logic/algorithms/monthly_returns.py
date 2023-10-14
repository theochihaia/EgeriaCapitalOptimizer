from datetime import datetime
import yfinance as yf
import pandas as pd
import calendar

def get_monthly_stats(symbol: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    # Download S&P 500 data
    ticker = yf.download(symbol, start=start_date, end=end_date)

    # Calculate monthly returns
    ticker['Monthly_Return'] = ticker['Adj Close'].resample('M').ffill().pct_change()

    # Create a column for the month
    ticker['Month'] = ticker.index.month

    # Group by month and calculate statistics
    grouped = ticker.groupby('Month')['Monthly_Return']
    avg_monthly_returns = grouped.mean()
    std_monthly_returns = grouped.std()
    min_monthly_returns = grouped.min()
    max_monthly_returns = grouped.max()

    # Convert to percentage
    avg_monthly_returns = avg_monthly_returns * 100
    std_monthly_returns = std_monthly_returns * 100
    min_monthly_returns = min_monthly_returns * 100
    max_monthly_returns = max_monthly_returns * 100

    # Combine all stats into one DataFrame
    result = pd.DataFrame({
        'Average_Return': avg_monthly_returns,
        'Standard_Deviation': std_monthly_returns,
        'Min_Return': min_monthly_returns,
        'Max_Return': max_monthly_returns
    })

    # Rename index from numeric to string label for month
    result.index = result.index.map(lambda x: calendar.month_name[x])
    
    # Format the numbers for better readability
    result = result.round(2)  # Round to 2 decimal places

    # Display output
    print(f"Symbol: {symbol}")
    print("-" * 50)  # Print separator for better visual distinction
    print(result)
    print("-" * 50)

    return result
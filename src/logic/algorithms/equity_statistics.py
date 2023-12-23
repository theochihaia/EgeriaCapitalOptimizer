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


def get_weekly_stats(symbol: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    # Download stock data
    ticker = yf.download(symbol, start=start_date, end=end_date)

    # Calculate daily returns
    ticker['Daily_Return'] = ticker['Adj Close'].pct_change()

    # Create a column for the day of the week
    ticker['DayOfWeek'] = ticker.index.dayofweek

    # Group by day of the week and calculate statistics
    grouped = ticker.groupby('DayOfWeek')

    avg_daily_returns = grouped['Daily_Return'].mean()
    std_daily_returns = grouped['Daily_Return'].std()
    min_daily_returns = grouped['Daily_Return'].min()
    max_daily_returns = grouped['Daily_Return'].max()
    median_volume = grouped['Volume'].median()

    # Convert to percentage
    avg_daily_returns = avg_daily_returns * 100
    std_daily_returns = std_daily_returns * 100
    min_daily_returns = min_daily_returns * 100
    max_daily_returns = max_daily_returns * 100

    # Combine all stats into one DataFrame
    result = pd.DataFrame({
        'Average_Return': avg_daily_returns,
        'Standard_Deviation': std_daily_returns,
        'Min_Return': min_daily_returns,
        'Max_Return': max_daily_returns,
        'Median_Volume': median_volume
    })

    # Rename index from numeric to string label for day of the week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    result.index = result.index.map(lambda x: days[x])
    
    # Format the numbers for better readability
    result = result.round(2)  # Round to 2 decimal places

    # Display output
    print(f"Symbol: {symbol}")
    print("-" * 50)  # Print separator for better visual distinction
    print(result)
    print("-" * 50)

    return result
import sqlite3
from datetime import datetime
from typing import List
from src.common.models.TickerCache import TickerCache


def datetime_to_unix(dt_obj: datetime) -> int:
    return int(dt_obj.timestamp())

def unix_to_datetime(unix_timestamp: int) -> str:
    return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Modified insert function
def insert_ticker_data(ticker: TickerCache):
    conn = sqlite3.connect('ticker_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO ticker_cache (symbol, name, TickerJSON, TradingDataJSON, DateTimeCreated, DateTimeUpdated, ExpirationDateTime)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (ticker.symbol, ticker.name, ticker.TickerJSON, ticker.TradingDataJSON, 
          datetime_to_unix(ticker.DateTimeCreated), datetime_to_unix(ticker.DateTimeUpdated), datetime_to_unix(ticker.ExpirationDateTime)))
    
    conn.commit()
    conn.close()

# Modified retrieve functions
def get_ticker_cache_by_symbol(symbol: str) -> TickerCache:
    conn = sqlite3.connect('ticker_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT symbol, name, TickerJSON, TradingDataJSON, DateTimeCreated, DateTimeUpdated, ExpirationDateTime 
    FROM ticker_cache WHERE symbol = ?
    ''', (symbol,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Convert Unix timestamps to datetime strings
        row = list(row)
        row[4] = unix_to_datetime(row[4])
        row[5] = unix_to_datetime(row[5])
        row[6] = unix_to_datetime(row[6])
        return TickerCache(*row)
    else:
        return None

def get_ticker_cache_by_expiration(expiration_date: str) -> List[TickerCache]:
    conn = sqlite3.connect('ticker_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT symbol, name, TickerJSON, TradingDataJSON, DateTimeCreated, DateTimeUpdated, ExpirationDateTime 
    FROM ticker_cache WHERE ExpirationDateTime <= ?
    ''', (datetime_to_unix(expiration_date),))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert Unix timestamps to datetime strings for all retrieved rows
    for i in range(len(rows)):
        row = list(rows[i])
        row[4] = unix_to_datetime(row[4])
        row[5] = unix_to_datetime(row[5])
        row[6] = unix_to_datetime(row[6])
        rows[i] = row
        
    return [TickerCache(*row) for row in rows]

# Modified update function
def update_ticker_cache(ticker: TickerCache):
    conn = sqlite3.connect('ticker_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE ticker_cache 
    SET name = ?, TickerJSON = ?, TradingDataJSON = ?, DateTimeCreated = ?, DateTimeUpdated = ?, ExpirationDateTime = ?
    WHERE symbol = ?
    ''', (ticker.name, ticker.TickerJSON, ticker.TradingDataJSON, 
          datetime_to_unix(ticker.DateTimeCreated), datetime_to_unix(ticker.DateTimeUpdated), datetime_to_unix(ticker.ExpirationDateTime), ticker.symbol))
    
    conn.commit()
    conn.close()


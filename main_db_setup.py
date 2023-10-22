import sqlite3
from datetime import datetime
from typing import List


def setup_ticker_database():
    conn = sqlite3.connect('ticker_data.db')
    cursor = conn.cursor()

    # Create an updated table for ticker_cache
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ticker_cache (
        id INTEGER PRIMARY KEY,
        symbol TEXT,
        name TEXT,
        TickerJSON TEXT,
        TradingDataJSON TEXT,
        DateTimeCreated INTEGER,
        DateTimeUpdated INTEGER,
        ExpirationDateTime INTEGER
    )
    ''')

    conn.commit()
    conn.close()

def clear_ticker_cache():
    conn = sqlite3.connect('ticker_data.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM ticker_cache')
    
    conn.commit()
    conn.close()


# Run the function to set up the updated database and table
setup_ticker_database()
clear_ticker_cache()

import json
import os
import shutil
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

from src.common.enums.equity_data_category import EquityDataCategory


# Save Data for a Symbol
def save_data(
    symbol,
    data: yf.Ticker,
    data_categories: [],
    directory="src/storage/data",
):
    for category in data_categories:
        save_data_for_category(symbol, data, category, directory + "/" + category.value)


def save_data_parallel(symbol, data, data_categories, directory):
    with ThreadPoolExecutor() as executor:
        category_symbol_to_future = {
            (symbol, category): executor.submit(
                save_data_for_category,
                symbol,
                data,
                category,
                directory + "/" + category.value,
            )
            for category in data_categories
        }

        for (symbol_key, category), future in category_symbol_to_future.items():
            try:
                result = future.result()
                print("Saving data for " + symbol_key + " - " + category.value)
            except Exception as e:
                print(
                    f"Function raised an exception for symbol {symbol_key} and category {category.value}:",
                    e,
                )


# Save Data for a single category
def save_data_for_category(
    symbol,
    data: yf.Ticker,
    category: EquityDataCategory,
    directory="src/storage/data",
):
    # Ensure directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the file path
    file_path = os.path.join(directory, f"{category.value}_{symbol}.json")

    # Serialize and save data as JSON
    with open(file_path, "w") as f:
        if category == EquityDataCategory.INFO:
            json.dump(data.get_info(), f, indent=4)
        elif category == EquityDataCategory.INCOME_STMT:
            f.write(data.get_income_stmt().to_json())
        elif category == EquityDataCategory.BALANCE_SHEET:
            f.write(data.get_balance_sheet().to_json())
        elif category == EquityDataCategory.QUARTERLY_INCOME_STMT:
            f.write(data.quarterly_income_stmt.to_json())
        elif category == EquityDataCategory.FAST_INFO:
            f.write(data.get_fast_info().to_json())
        else:
            raise ValueError(f"No Parser for data category: {category}")


# Clear Directory
def clear_directory(directory: str):
    print("Clearing directory: " + directory)

    # Wipe out the directory first
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

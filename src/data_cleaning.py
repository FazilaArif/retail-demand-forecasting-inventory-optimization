import pandas as pd
from pathlib import Path

# Get the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# File paths
calendar_path = BASE_DIR / "data" / "raw" / "calendar.csv"
sales_path = BASE_DIR / "data" / "raw" / "sales_train_validation.csv"
prices_path = BASE_DIR / "data" / "raw" / "sell_prices.csv"

# Load datasets
calendar = pd.read_csv(calendar_path)
sales = pd.read_csv(sales_path)
prices = pd.read_csv(prices_path)

print("Files loaded successfully!")

print("Calendar:", calendar.shape)
print("Sales:", sales.shape)
print("Prices:", prices.shape)
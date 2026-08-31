import pandas as pd

# Load datasets
calendar = pd.read_csv("data/raw/calendar.csv")
prices = pd.read_csv("data/raw/sell_prices.csv")
sales = pd.read_csv("data/raw/sales_train_evaluation.csv")

# Calendar information
print("\n========== CALENDAR DATA ==========")
print("\nFirst 5 rows:")
print(calendar.head())

print("\nShape:")
print(calendar.shape)

print("\nColumns:")
print(calendar.columns.tolist())


# Price information
print("\n========== PRICE DATA ==========")
print("\nFirst 5 rows:")
print(prices.head())

print("\nShape:")
print(prices.shape)

print("\nColumns:")
print(prices.columns.tolist())


# Sales information
print("\n========== SALES DATA ==========")
print("\nFirst 5 rows:")
print(sales.head())

print("\nShape:")
print(sales.shape)

print("\nFirst 20 Columns:")
print(sales.columns[:20].tolist())
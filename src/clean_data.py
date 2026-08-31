import pandas as pd
import os

# Create processed folder if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

# ==========================
# LOAD RAW DATA
# ==========================

calendar = pd.read_csv("data/raw/calendar.csv")
prices = pd.read_csv("data/raw/sell_prices.csv")

print("Raw Calendar Shape:", calendar.shape)
print("Raw Prices Shape:", prices.shape)


# ==========================
# CLEAN CALENDAR DATA
# ==========================

calendar["date"] = pd.to_datetime(calendar["date"])

# Fill missing event values
calendar["event_name_1"] = calendar["event_name_1"].fillna("No Event")
calendar["event_type_1"] = calendar["event_type_1"].fillna("No Event")

calendar["event_name_2"] = calendar["event_name_2"].fillna("No Event")
calendar["event_type_2"] = calendar["event_type_2"].fillna("No Event")

# Remove duplicates
calendar = calendar.drop_duplicates()

# Save cleaned calendar
calendar.to_csv(
    "data/processed/calendar_clean.csv",
    index=False
)


# ==========================
# CLEAN PRICE DATA
# ==========================

# Remove duplicate rows
prices = prices.drop_duplicates()

# Remove missing important values
prices = prices.dropna(
    subset=[
        "store_id",
        "item_id",
        "sell_price"
    ]
)

# Keep only valid prices
prices = prices[
    prices["sell_price"] >= 0
]

# Save cleaned prices
prices.to_csv(
    "data/processed/prices_clean.csv",
    index=False
)


# ==========================
# OUTPUT
# ==========================

print("\nCleaning Completed Successfully!")

print("\nClean Calendar Shape:", calendar.shape)
print("Clean Prices Shape:", prices.shape)
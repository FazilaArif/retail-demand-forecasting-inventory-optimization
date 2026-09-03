import pandas as pd

# Load raw sell prices data
df = pd.read_csv("data/raw/sell_prices.csv")

# Show first 5 rows
print(df.head())

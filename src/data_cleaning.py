import pandas as pd

# Load raw sell prices data
df = pd.read_csv("data/raw/sell_prices.csv")

# Show first 5 rows
print(df.head())

print(df.info())
print(df.describe())
print(df.isnull().sum())

df.duplicated().sum()
df.drop_duplicates()
df.to_csv("data/processed/sell_prices_clean.csv", index=False)

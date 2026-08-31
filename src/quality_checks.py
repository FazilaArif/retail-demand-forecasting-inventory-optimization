import pandas as pd

print("Loading processed sales data...")

sales = pd.read_csv(
    "data/processed/final_sales_sample.csv"
)

print("\n====================================")
print("       DATA QUALITY REPORT")
print("====================================")


# ==========================================
# 1. TOTAL ROW COUNT
# ==========================================

print("\n1. TOTAL ROWS")

print(len(sales))


# ==========================================
# 2. MISSING VALUES
# ==========================================

print("\n2. MISSING VALUES")

print(sales.isnull().sum())


# ==========================================
# 3. DUPLICATE RECORDS
# ==========================================

print("\n3. DUPLICATE RECORDS")

duplicates = sales.duplicated().sum()

print(duplicates)


# ==========================================
# 4. DUPLICATE BUSINESS KEYS
# ==========================================

print("\n4. DUPLICATE ITEM + STORE + DATE")

duplicate_keys = sales.duplicated(
    subset=[
        "item_id",
        "store_id",
        "date"
    ]
).sum()

print(duplicate_keys)


# ==========================================
# 5. NEGATIVE SALES
# ==========================================

print("\n5. NEGATIVE SALES")

negative_sales = (
    sales["sales"] < 0
).sum()

print(negative_sales)


# ==========================================
# 6. MISSING DATES
# ==========================================

print("\n6. MISSING DATES")

missing_dates = (
    sales["date"].isnull().sum()
)

print(missing_dates)


# ==========================================
# 7. MISSING ITEM IDs
# ==========================================

print("\n7. MISSING ITEM IDs")

missing_items = (
    sales["item_id"].isnull().sum()
)

print(missing_items)


# ==========================================
# 8. SALES DATA TYPE
# ==========================================

print("\n8. SALES DATA TYPE")

print(sales["sales"].dtype)


print("\n====================================")
print(" QUALITY CHECK COMPLETED SUCCESSFULLY")
print("====================================")
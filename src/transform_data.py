import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

# ==========================================
# LOAD SALES DATA
# ==========================================

print("Loading sales data...")

sales = pd.read_csv(
    "data/raw/sales_train_evaluation.csv"
)

print("Original sales shape:", sales.shape)


# ==========================================
# TAKE SAMPLE FOR SAFE PROCESSING
# ==========================================

sales_sample = sales.head(100)

print("Sample shape:", sales_sample.shape)


# ==========================================
# IDENTIFY ID AND DAY COLUMNS
# ==========================================

id_columns = [
    "id",
    "item_id",
    "dept_id",
    "cat_id",
    "store_id",
    "state_id"
]

day_columns = [
    col for col in sales_sample.columns
    if col.startswith("d_")
]

print("Number of day columns:", len(day_columns))


# ==========================================
# WIDE → LONG TRANSFORMATION
# ==========================================

print("Converting wide data to long format...")

sales_long = pd.melt(
    sales_sample,
    id_vars=id_columns,
    value_vars=day_columns,
    var_name="d",
    value_name="sales"
)

print("Long format shape:", sales_long.shape)


# ==========================================
# LOAD CLEAN CALENDAR DATA
# ==========================================

print("Loading calendar data...")

calendar = pd.read_csv(
    "data/processed/calendar_clean.csv"
)

# Convert date to datetime
calendar["date"] = pd.to_datetime(
    calendar["date"]
)


# ==========================================
# JOIN SALES WITH CALENDAR
# ==========================================

print("Joining sales with calendar...")

final_sales = sales_long.merge(
    calendar,
    on="d",
    how="left"
)

print("Final sales shape:", final_sales.shape)


# ==========================================
# SELECT IMPORTANT COLUMNS
# ==========================================

final_sales = final_sales[
    [
        "id",
        "item_id",
        "dept_id",
        "cat_id",
        "store_id",
        "state_id",
        "date",
        "d",
        "sales",
        "weekday",
        "month",
        "year",
        "event_name_1",
        "event_type_1"
    ]
]


# ==========================================
# SORT DATA
# ==========================================

final_sales = final_sales.sort_values(
    by=[
        "item_id",
        "store_id",
        "date"
    ]
)


# ==========================================
# SAVE FINAL SALES SAMPLE
# ==========================================

final_sales.to_csv(
    "data/processed/final_sales_sample.csv",
    index=False
)

print("\n========== TRANSFORMATION COMPLETED ==========")

print("\nFirst 10 rows:")
print(final_sales.head(10))

print("\nFinal shape:")
print(final_sales.shape)

print("\nSaved as:")
print("data/processed/final_sales_sample.csv")
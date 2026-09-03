import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "tonal-justice-507110-s6"
DATASET_ID = "retail_forecasting"

client = bigquery.Client(project=PROJECT_ID)


def load_dataframe(dataframe, table_name):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    print(f"\nLoading {table_name}...")

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )

    job = client.load_table_from_dataframe(
        dataframe,
        table_id,
        job_config=job_config
    )

    job.result()

    print(f"✅ {table_name} loaded successfully!")


print("Reading calendar data...")
calendar = pd.read_csv(
    "data/processed/calendar_clean.csv"
)
load_dataframe(calendar, "raw_calendar")


print("Reading price data...")
prices = pd.read_csv(
    "data/processed/prices_clean.csv"
)
load_dataframe(prices, "raw_sell_prices")


print("Reading sales data...")
sales = pd.read_csv(
    "data/processed/final_sales_sample.csv"
)
load_dataframe(sales, "raw_sales_sample")


print("\n==========================================")
print("🎉 ALL DATA LOADED TO BIGQUERY SUCCESSFULLY!")
print("==========================================")
import pandas as pd
from google.cloud import bigquery
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

PROJECT_ID = "tonal-justice-507110-s6"

client = bigquery.Client(project=PROJECT_ID)

query = """
SELECT
    item_id,
    store_id,
    date,
    sales,
    lag_1,
    lag_7,
    lag_28,
    rolling_mean_7,
    rolling_mean_28,
    dataset_type
FROM
    `tonal-justice-507110-s6.retail_forecasting.forecasting_train_split`
ORDER BY
    item_id,
    store_id,
    date
"""

print("Loading forecasting data from BigQuery...")

df = client.query(query).to_dataframe()

df["date"] = pd.to_datetime(df["date"])

print(f"Total rows loaded: {len(df):,}")

# Separate training and validation data
train = df[df["dataset_type"] == "train"].copy()
validation = df[df["dataset_type"] == "validation"].copy()

print(f"Training rows: {len(train):,}")
print(f"Validation rows: {len(validation):,}")

# Baseline forecast:
# Predict today's sales using sales from 7 days ago
validation["prediction"] = validation["lag_7"]

# Remove rows where prediction is unavailable
validation = validation.dropna(subset=["prediction", "sales"])

mae = mean_absolute_error(
    validation["sales"],
    validation["prediction"]
)

rmse = np.sqrt(
    mean_squared_error(
        validation["sales"],
        validation["prediction"]
    )
)

print("\n====================================")
print("BASELINE FORECAST RESULTS")
print("====================================")
print(f"MAE : {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print("====================================")
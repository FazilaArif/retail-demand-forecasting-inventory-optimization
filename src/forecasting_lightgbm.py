import pandas as pd
import numpy as np
from google.cloud import bigquery
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os
import joblib

PROJECT_ID = "tonal-justice-507110-s6"

client = bigquery.Client(project=PROJECT_ID)

query = """
SELECT
    item_id,
    store_id,
    date,
    sales,
    sell_price,
    year,
    month,
    day_of_week,
    is_weekend,
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

# Features used by the model
features = [
    "sell_price",
    "year",
    "month",
    "day_of_week",
    "is_weekend",
    "lag_1",
    "lag_7",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_28"
]

target = "sales"

# Split data
train = df[df["dataset_type"] == "train"].copy()
validation = df[df["dataset_type"] == "validation"].copy()

print(f"Training rows: {len(train):,}")
print(f"Validation rows: {len(validation):,}")

# Remove rows with missing feature values
train = train.dropna(subset=features + [target])
validation = validation.dropna(subset=features + [target])

X_train = train[features]
y_train = train[target]

X_validation = validation[features]
y_validation = validation[target]

print(f"\nRows used for training: {len(X_train):,}")
print(f"Rows used for validation: {len(X_validation):,}")

# LightGBM model
model = LGBMRegressor(
    objective="regression",
    n_estimators=300,
    learning_rate=0.05,
    num_leaves=31,
    max_depth=-1,
    random_state=42,
    verbosity=-1
)

print("\nTraining LightGBM model...")

model.fit(
    X_train,
    y_train
)

print("Model training completed!")

# Predictions
predictions = model.predict(X_validation)

# Avoid negative demand predictions
predictions = np.maximum(predictions, 0)

# Evaluation
mae = mean_absolute_error(
    y_validation,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_validation,
        predictions
    )
)

print("\n====================================")
print("LIGHTGBM FORECAST RESULTS")
print("====================================")
print(f"MAE : {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print("====================================")

# Compare with baseline
baseline_predictions = validation["lag_7"].values

baseline_mae = mean_absolute_error(
    y_validation,
    baseline_predictions
)

baseline_rmse = np.sqrt(
    mean_squared_error(
        y_validation,
        baseline_predictions
    )
)

print("\n====================================")
print("MODEL COMPARISON")
print("====================================")
print(f"Baseline MAE  : {baseline_mae:.4f}")
print(f"LightGBM MAE  : {mae:.4f}")
print()
print(f"Baseline RMSE : {baseline_rmse:.4f}")
print(f"LightGBM RMSE : {rmse:.4f}")
print("====================================")

if mae < baseline_mae:
    print("\n✅ LightGBM improved the MAE over the baseline.")
else:
    print("\n⚠️ LightGBM did not improve the MAE over the baseline.")

if rmse < baseline_rmse:
    print("✅ LightGBM improved the RMSE over the baseline.")
else:
    print("⚠️ LightGBM did not improve the RMSE over the baseline.")


# ============================================================
# SAVE FORECAST PREDICTIONS
# ============================================================

print("\nSaving forecast predictions...")

forecast_output = validation[
    [
        "item_id",
        "store_id",
        "date",
        "sales",
        "sell_price"
    ]
].copy()

forecast_output["predicted_sales"] = predictions

forecast_output["absolute_error"] = np.abs(
    forecast_output["sales"] -
    forecast_output["predicted_sales"]
)

# Create output directory if it does not exist
os.makedirs("outputs", exist_ok=True)

output_file = "outputs/lightgbm_predictions.csv"

forecast_output.to_csv(
    output_file,
    index=False
)

print(f"✅ Forecast predictions saved to: {output_file}")

print(f"Prediction rows saved: {len(forecast_output):,}")

print("\n====================================")
print("FORECAST OUTPUT PREVIEW")
print("====================================")

print(
    forecast_output.head(10).to_string(index=False)
)

print("====================================")
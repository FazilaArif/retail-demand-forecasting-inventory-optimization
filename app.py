import streamlit as st
import pandas as pd
import numpy as np


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #777777;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 650;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = "outputs/lightgbm_predictions.csv"

    data = pd.read_csv(file_path)

    data["date"] = pd.to_datetime(data["date"])

    return data


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "Prediction file was not found."
    )

    st.info(
        "Run src/forecasting_lightgbm.py first."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📊 Retail Demand Forecasting</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Demand forecasting and inventory analysis using LightGBM'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown("---")


# Item filter

item_list = sorted(
    df["item_id"].unique()
)

selected_item = st.sidebar.selectbox(
    "📦 Select Product",
    ["All Products"] + item_list
)


# Store filter

store_list = sorted(
    df["store_id"].unique()
)

selected_store = st.sidebar.selectbox(
    "🏪 Select Store",
    ["All Stores"] + store_list
)


# Date filter

min_date = df["date"].min().date()
max_date = df["date"].max().date()

selected_date_range = st.sidebar.slider(
    "📅 Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()


if selected_item != "All Products":

    filtered_df = filtered_df[
        filtered_df["item_id"] == selected_item
    ]


if selected_store != "All Stores":

    filtered_df = filtered_df[
        filtered_df["store_id"] == selected_store
    ]


start_date = pd.to_datetime(
    selected_date_range[0]
)

end_date = pd.to_datetime(
    selected_date_range[1]
)


filtered_df = filtered_df[
    (filtered_df["date"] >= start_date)
    &
    (filtered_df["date"] <= end_date)
]


# ============================================================
# CHECK DATA
# ============================================================

if filtered_df.empty:

    st.warning(
        "No data available for the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_actual = filtered_df["sales"].sum()

total_predicted = filtered_df["predicted_sales"].sum()

average_daily_demand = (
    filtered_df
    .groupby("date")["predicted_sales"]
    .sum()
    .mean()
)

mae = filtered_df["absolute_error"].mean()

rmse = np.sqrt(
    np.mean(
        (
            filtered_df["sales"]
            -
            filtered_df["predicted_sales"]
        ) ** 2
    )
)


# ============================================================
# KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">📌 Key Performance Indicators</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Actual Sales",
        f"{total_actual:,.0f}"
    )


with col2:

    st.metric(
        "Predicted Demand",
        f"{total_predicted:,.0f}"
    )


with col3:

    st.metric(
        "MAE",
        f"{mae:.2f}"
    )


with col4:

    st.metric(
        "RMSE",
        f"{rmse:.2f}"
    )


st.markdown("---")


# ============================================================
# ACTUAL VS PREDICTED
# ============================================================

st.markdown(
    '<div class="section-title">📈 Actual vs Predicted Demand</div>',
    unsafe_allow_html=True
)


daily_data = (
    filtered_df
    .groupby("date")
    .agg(
        Actual=("sales", "sum"),
        Predicted=("predicted_sales", "sum")
    )
    .reset_index()
)


chart_data = daily_data.set_index("date")

st.line_chart(
    chart_data,
    use_container_width=True
)


# ============================================================
# DEMAND ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Demand Analysis</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# TOP PRODUCTS
# ------------------------------------------------------------

with col1:

    st.subheader("🏆 Top Products")

    top_products = (
        filtered_df
        .groupby("item_id")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(
        top_products
    )


# ------------------------------------------------------------
# DAILY DEMAND
# ------------------------------------------------------------

with col2:

    st.subheader("📅 Daily Predicted Demand")

    daily_prediction = (
        filtered_df
        .groupby("date")["predicted_sales"]
        .sum()
    )

    st.area_chart(
        daily_prediction
    )


# ============================================================
# INVENTORY ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📦 Inventory Planning</div>',
    unsafe_allow_html=True
)


# Calculate demand statistics

daily_demand = (
    filtered_df
    .groupby("date")["predicted_sales"]
    .sum()
)


avg_demand = daily_demand.mean()

demand_std = daily_demand.std()

if pd.isna(demand_std):

    demand_std = 0


# Assumptions for demonstration

lead_time_days = 7

safety_factor = 1.65


safety_stock = (
    safety_factor
    *
    demand_std
    *
    np.sqrt(lead_time_days)
)


reorder_point = (
    avg_demand
    *
    lead_time_days
    +
    safety_stock
)


inventory_col1, inventory_col2, inventory_col3 = st.columns(3)


with inventory_col1:

    st.metric(
        "Average Daily Demand",
        f"{avg_demand:,.1f}"
    )


with inventory_col2:

    st.metric(
        "Estimated Safety Stock",
        f"{safety_stock:,.1f}"
    )


with inventory_col3:

    st.metric(
        "Estimated Reorder Point",
        f"{reorder_point:,.1f}"
    )


st.caption(
    "Inventory values are estimates based on predicted demand, "
    "a 7-day lead-time assumption, and a safety-stock factor."
)


# ============================================================
# FORECAST DETAILS
# ============================================================

st.markdown(
    '<div class="section-title">🔮 Forecast Details</div>',
    unsafe_allow_html=True
)


forecast_table = filtered_df[
    [
        "item_id",
        "store_id",
        "date",
        "sales",
        "predicted_sales",
        "absolute_error"
    ]
].copy()


forecast_table = forecast_table.rename(
    columns={
        "item_id": "Product",
        "store_id": "Store",
        "date": "Date",
        "sales": "Actual Sales",
        "predicted_sales": "Predicted Sales",
        "absolute_error": "Absolute Error"
    }
)


forecast_table = forecast_table.sort_values(
    "Date",
    ascending=False
)


st.dataframe(
    forecast_table,
    use_container_width=True,
    height=400
)


# ============================================================
# DOWNLOAD BUTTON
# ============================================================

csv_data = forecast_table.to_csv(
    index=False
)


st.download_button(
    label="⬇️ Download Forecast Results",
    data=csv_data,
    file_name="retail_forecast_results.csv",
    mime="text/csv"
)


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">🤖 Model Performance</div>',
    unsafe_allow_html=True
)


baseline_mae = 1.3967
baseline_rmse = 3.5893

lightgbm_mae = 1.0169
lightgbm_rmse = 2.4601


comparison = pd.DataFrame(
    {
        "Model": [
            "7-Day Lag Baseline",
            "LightGBM"
        ],
        "MAE": [
            baseline_mae,
            lightgbm_mae
        ],
        "RMSE": [
            baseline_rmse,
            lightgbm_rmse
        ]
    }
)


st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)


# Calculate improvement

mae_improvement = (
    (baseline_mae - lightgbm_mae)
    / baseline_mae
    * 100
)


rmse_improvement = (
    (baseline_rmse - lightgbm_rmse)
    / baseline_rmse
    * 100
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "MAE Improvement",
        f"{mae_improvement:.1f}%"
    )


with col2:

    st.metric(
        "RMSE Improvement",
        f"{rmse_improvement:.1f}%"
    )


st.success(
    "LightGBM performs better than the 7-day lag baseline "
    "on the validation dataset."
)


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.markdown("---")

st.subheader("ℹ️ Project Information")

info_col1, info_col2, info_col3 = st.columns(3)


with info_col1:

    st.write("**Data Platform**")

    st.write("Google BigQuery")


with info_col2:

    st.write("**Transformation**")

    st.write("dbt")


with info_col3:

    st.write("**Forecasting Model**")

    st.write("LightGBM")


st.caption(
    "Retail Demand Forecasting & Inventory Optimization | "
    "BigQuery + dbt + LightGBM + Streamlit"
)
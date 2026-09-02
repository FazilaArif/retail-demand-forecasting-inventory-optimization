# Retail Demand Forecasting

## Project Overview

This project focuses on building a retail demand forecasting data pipeline using historical retail sales data.

The project processes raw retail datasets, performs data cleaning and transformation, validates data quality, and prepares the processed data for storage and analysis in Google BigQuery.

The final goal of the project is to build a scalable data pipeline and develop a demand forecasting system that can help predict future product sales.

---

## Project Objectives

The main objectives of this project are:

- Process raw retail sales data.
- Clean calendar and product price datasets.
- Transform sales data from wide format to long format.
- Join sales data with calendar information.
- Perform data quality validation.
- Store processed data in Google BigQuery.
- Perform SQL-based analysis.
- Engineer features for demand forecasting.
- Build and evaluate forecasting models.

---

## Technologies Used

- Python 3.12
- Pandas
- NumPy
- PyArrow
- Google Cloud Platform
- Google BigQuery
- Google Cloud CLI
- Jupyter Notebook
- Git
- GitHub
- VS Code

---

## Dataset

This project uses retail sales data containing information about:

- Product IDs
- Department IDs
- Product categories
- Store IDs
- State IDs
- Daily sales
- Calendar information
- Product prices
- Events and holidays

The main datasets include:

```text
calendar.csv
sell_prices.csv
sales_train_evaluation.csv

Project Architecture

                    RETAIL DATASET
                         │
          ┌──────────────┼──────────────┐
          │              │              │
       Calendar         Prices         Sales
          │              │              │
          ▼              ▼              ▼
                 Python ETL Pipeline
                         │
          ┌──────────────┼──────────────┐
          │              │              │
       Cleaning     Transformation   Validation
                         │
                         ▼
                  Processed Data
                         │
                         ▼
                  Google BigQuery
                         │
                         ▼
                    SQL Analysis
                         │
                         ▼
                 Feature Engineering
                         │
                         ▼
                 Demand Forecasting


Project Structure

retail-demand-forecasting/
│
├── data/
│   │
│   ├── raw/
│   │   ├── calendar.csv
│   │   ├── sell_prices.csv
│   │   └── sales_train_evaluation.csv
│   │
│   └── processed/
│       ├── calendar_clean.csv
│       ├── prices_clean.csv
│       ├── sales_long_sample.csv
│       └── final_sales_sample.csv
│
├── src/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── transform_data.py
│   ├── quality_checks.py
│   ├── test_bigquery.py
│   └── load_bigquery.py
│
├── .gitignore
│
└── README.md

Data Setup and ETL Pipeline
1. Python Environment Setup

A Python virtual environment was created to isolate project dependencies.

Python version used:

Python 3.12

Virtual environment:

venv
2. Dataset Inspection

The raw retail datasets were inspected to understand:

Dataset structure
Number of rows and columns
Column names
Data types
Missing values
Sales data format

The sales dataset stores daily sales using columns such as:

d_1
d_2
d_3
...

This format required transformation before analysis and forecasting.

3. Data Cleaning

The calendar and price datasets were cleaned using Python and Pandas.

Data cleaning included:

Checking missing values.
Handling event-related missing values.
Converting date columns.
Checking data types.
Preparing datasets for transformation.

Processed files were saved in:

data/processed/
4. Sales Data Transformation

The sales dataset was originally stored in wide format.

Original Format
item_id | store_id | d_1 | d_2 | d_3

Example:

ITEM_1 | CA_1 | 10 | 15 | 20

The data was transformed into long format.

Transformed Format
item_id | store_id | d | sales

Example:

ITEM_1 | CA_1 | d_1 | 10
ITEM_1 | CA_1 | d_2 | 15
ITEM_1 | CA_1 | d_3 | 20

This format is more suitable for:

Time-series analysis
SQL queries
Feature engineering
Machine learning
Demand forecasting
5. Calendar and Sales Join

The transformed sales dataset was joined with the calendar dataset using the day column:

d

This added useful information such as:

Actual date
Weekday
Month
Year
Events
Event type

The resulting dataset contains sales information along with time-based features.

Output:

final_sales_sample.csv
6. Data Quality Checks

Data quality validation was performed on the processed sales dataset.

The following checks were implemented:

Total row count
Missing values
Duplicate records
Duplicate business keys
Negative sales values
Missing dates
Missing product IDs
Sales data type validation

The business key used was:

item_id + store_id + date

This ensures that each product has one sales record per store per day.

7. Google Cloud Setup

Google Cloud CLI was installed and configured.

The active Google Cloud project is:

tonal-justice-507110-s6

Google Cloud authentication was completed successfully.

Application Default Credentials were configured to allow the Python application to communicate with Google Cloud services.

8. BigQuery Connection

The Python application was successfully connected to Google BigQuery using:

from google.cloud import bigquery

A test query was executed successfully to verify the connection.

Expected output:

BigQuery connection successful!
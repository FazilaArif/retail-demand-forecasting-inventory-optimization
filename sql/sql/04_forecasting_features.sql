CREATE OR REPLACE TABLE
  `tonal-justice-507110-s6.retail_forecasting.forecasting_features`
AS

WITH base AS (
  SELECT
    item_id,
    store_id,
    date,
    sales,
    sell_price,

    EXTRACT(YEAR FROM date) AS year,

    EXTRACT(MONTH FROM date) AS month,

    EXTRACT(DAYOFWEEK FROM date) AS day_of_week,

    CASE
      WHEN EXTRACT(DAYOFWEEK FROM date) IN (1, 7)
      THEN 1
      ELSE 0
    END AS is_weekend

  FROM
    `tonal-justice-507110-s6.retail_forecasting.fact_sales`
),

features AS (
  SELECT
    *,

    LAG(sales, 1) OVER (
      PARTITION BY item_id, store_id
      ORDER BY date
    ) AS lag_1,

    LAG(sales, 7) OVER (
      PARTITION BY item_id, store_id
      ORDER BY date
    ) AS lag_7,

    LAG(sales, 28) OVER (
      PARTITION BY item_id, store_id
      ORDER BY date
    ) AS lag_28,

    AVG(sales) OVER (
      PARTITION BY item_id, store_id
      ORDER BY date
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_mean_7,

    AVG(sales) OVER (
      PARTITION BY item_id, store_id
      ORDER BY date
      ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
    ) AS rolling_mean_28

  FROM base
)

SELECT *
FROM features
ORDER BY item_id, store_id, date;
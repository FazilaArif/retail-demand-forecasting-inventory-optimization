-- Main analytical sales table

CREATE OR REPLACE TABLE
  `tonal-justice-507110-s6.retail_forecasting.analytics_sales`
AS
SELECT
  id,
  item_id,
  dept_id,
  cat_id,
  store_id,
  state_id,
  PARSE_DATE('%Y-%m-%d', date) AS date,
  d,
  sales,
  weekday,
  year,
  event_name_1,
  event_type_1
FROM
  `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`;


-- Daily sales aggregation

CREATE OR REPLACE TABLE
  `tonal-justice-507110-s6.retail_forecasting.analytics_daily_sales`
AS
SELECT
  date,
  item_id,
  dept_id,
  cat_id,
  store_id,
  state_id,
  SUM(sales) AS total_sales,
  COUNT(*) AS records_count
FROM
  `tonal-justice-507110-s6.retail_forecasting.analytics_sales`
GROUP BY
  date,
  item_id,
  dept_id,
  cat_id,
  store_id,
  state_id
ORDER BY
  date,
  item_id;


-- Add selling price

CREATE OR REPLACE TABLE
  `tonal-justice-507110-s6.retail_forecasting.analytics_sales_with_price`
AS
SELECT
  s.id,
  s.item_id,
  s.dept_id,
  s.cat_id,
  s.store_id,
  s.state_id,
  s.date,
  s.d,
  s.sales,
  s.weekday,
  s.year,
  s.event_name_1,
  s.event_type_1,
  p.sell_price

FROM
  `tonal-justice-507110-s6.retail_forecasting.analytics_sales` AS s

LEFT JOIN
  `tonal-justice-507110-s6.retail_forecasting.raw_calendar` AS c
ON
  s.d = c.d

LEFT JOIN
  `tonal-justice-507110-s6.retail_forecasting.raw_sell_prices` AS p
ON
  s.store_id = p.store_id
  AND s.item_id = p.item_id
  AND c.wm_yr_wk = p.wm_yr_wk;


-- Final fact table

CREATE OR REPLACE TABLE
  `tonal-justice-507110-s6.retail_forecasting.fact_sales`
AS
SELECT
  id,
  item_id,
  dept_id,
  cat_id,
  store_id,
  state_id,
  date,
  d,
  sales,
  weekday,
  year,
  event_name_1,
  event_type_1,
  sell_price

FROM
  `tonal-justice-507110-s6.retail_forecasting.analytics_sales_with_price`;
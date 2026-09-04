-- Row counts

SELECT
  'raw_calendar' AS table_name,
  COUNT(*) AS row_count
FROM `tonal-justice-507110-s6.retail_forecasting.raw_calendar`

UNION ALL

SELECT
  'raw_sell_prices',
  COUNT(*)
FROM `tonal-justice-507110-s6.retail_forecasting.raw_sell_prices`

UNION ALL

SELECT
  'raw_sales_sample',
  COUNT(*)
FROM `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`;


-- NULL validation

SELECT
  COUNT(*) AS total_rows,
  COUNTIF(id IS NULL) AS null_id,
  COUNTIF(item_id IS NULL) AS null_item_id,
  COUNTIF(store_id IS NULL) AS null_store_id,
  COUNTIF(date IS NULL) AS null_date,
  COUNTIF(sales IS NULL) AS null_sales
FROM `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`;
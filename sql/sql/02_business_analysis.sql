-- Top 10 products

SELECT
  item_id,
  SUM(sales) AS total_sales
FROM `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`
GROUP BY item_id
ORDER BY total_sales DESC
LIMIT 10;


-- Store sales

SELECT
  store_id,
  SUM(sales) AS total_sales
FROM `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`
GROUP BY store_id
ORDER BY total_sales DESC;


-- Category sales

SELECT
  cat_id,
  SUM(sales) AS total_sales
FROM `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`
GROUP BY cat_id
ORDER BY total_sales DESC;


-- Department sales

SELECT
  dept_id,
  SUM(sales) AS total_sales
FROM `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`
GROUP BY dept_id
ORDER BY total_sales DESC;


-- Daily sales

SELECT
  date,
  SUM(sales) AS total_sales
FROM `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`
GROUP BY date
ORDER BY date;


-- Monthly sales

SELECT
  EXTRACT(
    YEAR FROM PARSE_DATE('%Y-%m-%d', date)
  ) AS year,

  EXTRACT(
    MONTH FROM PARSE_DATE('%Y-%m-%d', date)
  ) AS month,

  SUM(sales) AS total_sales

FROM `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`

GROUP BY year, month
ORDER BY year, month;


-- Weekday sales

SELECT
  weekday,
  SUM(sales) AS total_sales
FROM `tonal-justice-507110-s6.retail_forecasting.raw_sales_sample`
GROUP BY weekday
ORDER BY total_sales DESC;
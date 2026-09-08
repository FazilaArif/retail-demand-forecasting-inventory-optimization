SELECT
    DATE_TRUNC(date, WEEK(MONDAY)) AS week_start_date,
    item_id,
    store_id,
    dept_id,
    cat_id,
    state_id,
    SUM(total_sales) AS weekly_sales,
    AVG(average_sell_price) AS average_sell_price,
    SUM(records_count) AS records_count
FROM {{ ref('daily_sales') }}
GROUP BY
    week_start_date,
    item_id,
    store_id,
    dept_id,
    cat_id,
    state_id
SELECT
    date,
    item_id,
    store_id,
    dept_id,
    cat_id,
    state_id,
    total_sales,
    average_sell_price,
    records_count
FROM {{ ref('daily_sales') }}
WHERE total_sales >= 0
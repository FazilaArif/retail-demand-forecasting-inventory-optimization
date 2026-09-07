SELECT
    date,
    item_id,
    store_id,
    dept_id,
    cat_id,
    state_id,

    SUM(sales) AS total_sales,

    AVG(sell_price) AS average_sell_price,

    COUNT(*) AS records_count

FROM {{ ref('stg_sales') }}

GROUP BY
    date,
    item_id,
    store_id,
    dept_id,
    cat_id,
    state_id
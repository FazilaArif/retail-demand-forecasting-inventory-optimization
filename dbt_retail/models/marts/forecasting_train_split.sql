WITH ranked_data AS (
    SELECT
        *,
        NTILE(5) OVER (
            PARTITION BY item_id, store_id
            ORDER BY date
        ) AS time_group
    FROM {{ ref('forecasting_train') }}
)

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

    CASE
        WHEN time_group <= 4 THEN 'train'
        ELSE 'validation'
    END AS dataset_type

FROM ranked_data
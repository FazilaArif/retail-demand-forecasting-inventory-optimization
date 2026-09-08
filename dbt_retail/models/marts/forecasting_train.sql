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
    rolling_mean_28
FROM {{ ref('forecasting_features') }}
WHERE
    lag_1 IS NOT NULL
    AND lag_7 IS NOT NULL
    AND lag_28 IS NOT NULL
    AND rolling_mean_7 IS NOT NULL
    AND rolling_mean_28 IS NOT NULL
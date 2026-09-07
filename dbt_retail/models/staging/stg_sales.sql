WITH source AS (

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

    FROM `tonal-justice-507110-s6.retail_forecasting.fact_sales`

)

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

FROM source
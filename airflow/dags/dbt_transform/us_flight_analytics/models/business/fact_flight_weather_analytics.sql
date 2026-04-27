{{ config(
    materialized='table',
    format='parquet',
    write_compression='snappy',
    partitioned_by=['flight_year', 'flight_month'] 
) }}

WITH joined_data AS (
    SELECT * FROM {{ ref('int_flights_with_weather') }}
)

SELECT
    flight_date,

    day_of_week,
    deptime_label,
    airline,
    tail_number,
    dep_airport,

    departure_delay_minutes,
    avg_temp_c,

    -- Using for machine learning --
    precipitation_mm,

    snow_mm,
    wind_speed_kmh,
    CASE
        WHEN departure_delay_minutes <= 0 THEN 'On Time'
        WHEN
            departure_delay_minutes > 0 AND departure_delay_minutes <= 15
            THEN 'Slight Delay'
        WHEN
            departure_delay_minutes > 15 AND departure_delay_minutes <= 60
            THEN 'Moderate Delay'
        ELSE 'Severe Delay'
    END AS delay_severity,
    CASE
        WHEN departure_delay_minutes > 15 THEN 1
        ELSE 0
    END AS is_delayed,

    CASE
        WHEN snow_mm > 0 OR wind_speed_kmh > 40 OR precipitation_mm > 20 THEN 1
        ELSE 0
    END AS is_extreme_weather,

    EXTRACT(YEAR FROM flight_date) AS flight_year,
    EXTRACT(MONTH FROM flight_date) AS flight_month

FROM joined_data

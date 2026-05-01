WITH raw_cancelled AS (
    SELECT * FROM {{ source('aws_data_lake', 'clean_cancelled_diverted') }}
)

SELECT
    flightdate AS flight_date,
    day_of_week,
    airline,
    tail_number,

    cancelled,
    diverted,
    flight_duration,
    dep_airport,
    dep_cityname,
    deptime_label,
    dep_delay_tag,
    dep_delay_type,
    arr_airport,
    arr_cityname,
    arr_delay_type,
    distance_type
FROM raw_cancelled
WHERE
    flightdate IS NOT NULL
    AND
    tail_number IS NOT NULL

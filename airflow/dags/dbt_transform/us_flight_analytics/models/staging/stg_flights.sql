WITH raw_flights AS (
    SELECT * FROM {{ source('aws_data_lake', 'clean_flights') }}
)

SELECT
    flightdate AS flight_date,
    day_of_week,
    airline,
    tail_number,
    dep_airport,
    dep_cityname,
    deptime_label,
    dep_delay AS departure_delay_minutes,
    dep_delay_tag,
    dep_delay_type,
    arr_airport,
    arr_cityname,
    arr_delay,
    arr_delay_type,
    flight_duration,
    distance_type,
    delay_carrier,
    delay_weather,
    delay_nas,
    delay_security,
    delay_lastaircraft,
    manufacturer,
    model,
    aicraft_age AS aircraft_age
FROM raw_flights
WHERE
    flightdate IS NOT NULL
AND
    tail_number IS NOT NULL;
WITH flights AS (
    SELECT * FROM {{ ref('stg_flights') }}
),

weather AS (
    SELECT * FROM {{ ref('stg_weather') }}
),

joined_flights_weather AS (
    SELECT
        f.*,

        w.avg_temp_c,
        w.precipitation_mm,
        w.snow_mm,
        w.wind_speed_kmh

    FROM
        flights f
    LEFT JOIN
        weather w
        ON
            f.dep_airport = w.airport_code
        AND
            f.flight_date = w.weather_timestamp
)

SELECT * FROM joined_flights_weather
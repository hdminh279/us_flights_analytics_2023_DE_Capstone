WITH cancelled AS (
    SELECT * FROM {{ ref('stg_cancelled') }}
),

weather AS (
    SELECT * FROM {{ ref('stg_weather') }}
),

joined_cancelled_weather AS (
    SELECT 
        c.*,
        w.avg_temp_c,
        w.precipitation_mm,
        w.snow_mm,
        w.wind_speed_kmh
    FROM cancelled c
    LEFT JOIN weather w
        ON c.dep_airport = w.airport_code
        AND DATE(c.flight_date) = DATE(w.weather_timestamp)
)

SELECT * FROM joined_cancelled_weather
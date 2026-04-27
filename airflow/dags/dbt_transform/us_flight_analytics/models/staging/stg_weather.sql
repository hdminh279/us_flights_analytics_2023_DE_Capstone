WITH raw_weather AS (
    SELECT * FROM {{ source('aws_data_lake', 'clean_weather') }}
)

SELECT
    airport_id AS airport_code,
    time AS weather_timestamp,
    tavg AS avg_temp_c,
    prcp AS precipitation_mm,
    snow AS snow_mm,
    wspd AS wind_speed_kmh,
    pres AS sea_level_pressure
FROM raw_weather
WHERE
    airport_id IS NOT NULL
    AND
    time IS NOT NULL;

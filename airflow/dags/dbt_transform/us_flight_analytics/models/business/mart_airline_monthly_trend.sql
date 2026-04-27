WITH fact_flights AS (
    SELECT * FROM {{ ref('fact_flight_weather_analytics') }}
)

SELECT
    airline,
    flight_year,
    flight_month,

    COUNT(*) AS monthly_total_flights,

    ROUND(CAST(SUM(is_delayed) AS DOUBLE) / COUNT(*) * 100, 2)
        AS monthly_delay_rate

FROM fact_flights
GROUP BY
    airline,
    flight_year,
    flight_month

ORDER BY
    airline,
    flight_year,
    flight_month;

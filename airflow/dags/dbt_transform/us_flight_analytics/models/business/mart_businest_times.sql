WITH fact_flights AS (
    SELECT * FROM {{ ref('fact_flight_weather_analytics') }}
)

SELECT
    day_of_week,
    deptime_label,

    CAST(COUNT(*) AS INT) AS total_flights,

    SUM(is_delayed) AS delayed_flights,
    ROUND(CAST(SUM(is_delayed) AS DOUBLE) / COUNT(*) * 100, 2)
        AS delay_rate_percentage

FROM fact_flights
GROUP BY
    day_of_week,
    deptime_label
ORDER BY total_flights DESC;

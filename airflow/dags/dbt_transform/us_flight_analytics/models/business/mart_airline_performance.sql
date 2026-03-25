WITH fact_flights AS (
    SELECT * FROM {{ ref('fact_flight_weather_analytics') }}
)

SELECT 
    airline,

    COUNT(*) AS total_flights,
    
    SUM(is_delayed) AS total_delayed_flights,
    
    ROUND(CAST(SUM(is_delayed) AS DOUBLE) / COUNT(*) * 100, 2) AS delay_rate_percentage,
    
    ROUND(AVG(departure_delay_minutes), 2) AS avg_delay_minutes

FROM fact_flights
GROUP BY airline
ORDER BY total_flights DESC;
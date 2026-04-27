WITH cancelled_flights AS (
    SELECT * FROM {{ ref('stg_cancelled') }}
)

SELECT
    airline,
    COUNT(*) AS cancelled_amount

FROM
    cancelled_flights
GROUP BY
    airline
ORDER BY cancelled_amount DESC;

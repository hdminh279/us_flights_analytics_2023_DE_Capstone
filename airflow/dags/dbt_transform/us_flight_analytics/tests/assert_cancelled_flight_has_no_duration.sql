SELECT 
    tail_number,
    flight_date,
    cancelled,
    flight_duration
FROM {{ ref('stg_cancelled') }}
WHERE cancelled = 1 
  AND flight_duration > 0

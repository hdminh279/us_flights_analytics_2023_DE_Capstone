SELECT 
    Tail_Number,
    FlightDate,
    Cancelled,
    Flight_Duration
FROM {{ ref('stg_cancelled') }}
WHERE Cancelled = 1 
  AND Flight_Duration > 0

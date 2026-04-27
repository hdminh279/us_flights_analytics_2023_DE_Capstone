WITH raw_geo AS (
    SELECT * FROM {{ source('aws_data_lake', 'clean_geo') }}
)

SELECT
    iata_code AS airport_code,
    airport AS airport_name,
    city,
    state,
    country,
    latitude,
    longitude
FROM raw_geo
WHERE iata_code IS NOT NULL;

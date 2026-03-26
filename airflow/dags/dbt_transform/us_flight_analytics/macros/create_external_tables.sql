{% macro create_external_tables() %}
    
    {% set db = target.schema %}
    {% set bucket = env_var('TARGET_S3_BUCKET') %}

    {% set query_geo %}
        CREATE EXTERNAL TABLE IF NOT EXISTS {{ db }}.clean_geo (
          iata_code STRING,
          airport STRING,
          city STRING,
          state STRING,
          country STRING,
          latitude DOUBLE,
          longitude DOUBLE
        )
        STORED AS PARQUET
        LOCATION 's3://{{ bucket }}/clean/geo/';
    {% endset %}

    {% set query_weather %}
        CREATE EXTERNAL TABLE IF NOT EXISTS {{ db }}.clean_weather (
          time TIMESTAMP,
          tavg FLOAT,
          tmin FLOAT,
          tmax FLOAT,
          prcp FLOAT,
          snow FLOAT,
          wdir FLOAT,
          wspd FLOAT,
          pres FLOAT,
          airport_id STRING
        )
        STORED AS PARQUET
        LOCATION 's3://{{ bucket }}/clean/weather/';
    {% endset %}

    {% set query_cancelled %}
        CREATE EXTERNAL TABLE IF NOT EXISTS {{ db }}.clean_cancelled_diverted (
          flightdate TIMESTAMP,
          day_of_week INT,
          airline STRING,
          tail_number STRING,
          cancelled INT,
          diverted INT,
          dep_airport STRING,
          dep_cityname STRING,
          deptime_label STRING,
          dep_delay INT,
          dep_delay_tag INT,
          dep_delay_type STRING,
          arr_airport STRING,
          arr_cityname STRING,
          arr_delay INT,
          arr_delay_type STRING,
          flight_duration INT,
          distance_type STRING,
          delay_carrier INT,
          delay_weather INT,
          delay_nas INT,
          delay_security INT,
          delay_lastaircraft INT
        )
        STORED AS PARQUET
        LOCATION 's3://{{ bucket }}/clean/cancelled_diverted/';
    {% endset %}

    {% set query_flights %}
        CREATE EXTERNAL TABLE IF NOT EXISTS {{ db }}.clean_flights (
          flightdate TIMESTAMP,
          day_of_week INT,
          airline STRING,
          tail_number STRING,
          dep_airport STRING,
          dep_cityname STRING,
          deptime_label STRING,
          dep_delay INT,
          dep_delay_tag INT,
          dep_delay_type STRING,
          arr_airport STRING,
          arr_cityname STRING,
          arr_delay INT,
          arr_delay_type STRING,
          flight_duration INT,
          distance_type STRING,
          delay_carrier INT,
          delay_weather INT,
          delay_nas INT,
          delay_security INT,
          delay_lastaircraft INT,
          manufacturer STRING,
          model STRING,
          aircraft_age INT
        )
        STORED AS PARQUET
        LOCATION 's3://{{ bucket }}/clean/flights/';
    {% endset %}
    
    #Execute sql
    {% do run_query(query_geo) %}
    {% do run_query(query_weather) %}
    {% do run_query(query_cancelled) %}
    {% do run_query(query_flights) %}

{% endmacro %}
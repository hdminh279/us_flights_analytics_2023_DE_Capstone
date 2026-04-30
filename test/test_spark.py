import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

from airflow.dags.spark_jobs.spark_preprocessing import clean_airport_geo, clean_flight, weather_clean

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("Unit-Testing-Flights").getOrCreate()

def test_clean_airport_geo(spark):
    schema = StructType([
        StructField('IATA_CODE', StringType(), True), 
        StructField('AIRPORT', StringType(), True),
        StructField('CITY', StringType(), True),
        StructField('STATE', StringType(), True),
        StructField('COUNTRY', StringType(), True),
        StructField('LATITUDE', DoubleType(), True), 
        StructField('LONGITUDE', DoubleType(), True)
    ])
    
    data = [
        ("JFK", "John F Kennedy", "NY", "NY", "USA", 40.64, -73.77),   
        ("LAX", "Los Angeles", "CA", "CA", "USA", 999.0, -118.40),    
    ]
    df = spark.createDataFrame(data, schema)
    
    result_df = clean_airport_geo(df)
    
    assert result_df.count() == 1
    assert result_df.collect()[0]["IATA_CODE"] == "JFK"

def test_clean_flight_drops_invalid_duration_and_nulls(spark):
    schema = StructType([
        StructField('FlightDate', StringType(), True),
        StructField('Day_Of_Week', IntegerType(), True),
        StructField('Dep_Delay_Tag', IntegerType(), True),
        StructField('Airline', StringType(), True),
        StructField('Tail_Number', StringType(), True),
        StructField('Dep_Airport', StringType(), True),
        StructField('Dep_CityName', StringType(), True),
        StructField('DepTime_label', StringType(), True),
        StructField('Dep_Delay_Type', StringType(), True),
        StructField('Arr_Airport', StringType(), True),
        StructField('Arr_CityName', StringType(), True),
        StructField('Arr_Delay_Type', StringType(), True),
        StructField('Manufacturer', StringType(), True),
        StructField('Model', StringType(), True),
        StructField('Arr_Delay', IntegerType(), True),
        StructField('Flight_Duration', IntegerType(), True),
        StructField('Delay_Carrier', IntegerType(), True),
        StructField('Delay_Weather', IntegerType(), True),
        StructField('Delay_NAS', IntegerType(), True),
        StructField('Delay_Security', IntegerType(), True),
        StructField('Delay_LastAircraft', IntegerType(), True),
        StructField('Aircraft_age', IntegerType(), True)
    ])

    data = [
        ("2023-01-01 10:00:00", 1, 0, "Delta", "N123", "JFK", "NY", "Morning", "None", "LAX", "LA", "None", "Boeing", "737", 0, 300, 0, 0, 0, 0, 0, 5),
        ("2023-01-02 10:00:00", 2, 0, None, "N124", "ORD", "CHI", "Morning", "None", "SFO", "SF", "None", "Airbus", "A320", 0, 200, 0, 0, 0, 0, 0, 3),
        ("2023-01-03 10:00:00", 3, 0, "United", "N125", "MIA", "MIA", "Morning", "None", "JFK", "NY", "None", "Boeing", "777", 0, -50, 0, 0, 0, 0, 0, 10),
    ]
    df = spark.createDataFrame(data, schema)
    
    result_df = clean_flight(df)
    
    assert result_df.count() == 1
    assert result_df.collect()[0]["Airline"] == "Delta"

def test_weather_clean_trims_whitespace(spark):
    schema = StructType([
        StructField('time', StringType(), True),
        StructField('tavg', StringType(), True),
        StructField('tmin', StringType(), True),
        StructField('tmax', StringType(), True),
        StructField('prcp', StringType(), True),
        StructField('snow', StringType(), True),
        StructField('wdir', StringType(), True),
        StructField('wspd', StringType(), True),
        StructField('pres', StringType(), True),
        StructField('airport_id', StringType(), True)
    ])
    
    data = [("2023-01-01 12:00:00", "25.5", "20.0", "30.0", "0.0", "0.0", "180", "15.0", "1012.5", " JFK ")]
    df = spark.createDataFrame(data, schema)
    
    result_df = weather_clean(df)
    
    assert result_df.collect()[0]["airport_id"] == "JFK"
    assert dict(result_df.dtypes)["tavg"] == "float"

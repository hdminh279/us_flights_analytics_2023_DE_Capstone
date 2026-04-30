from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F
import os

def clean_airport_geo(df):
    df_clean = df.dropna(subset=['IATA_CODE', 'AIRPORT', 'LATITUDE', 'LONGITUDE'])
    df_clean = df_clean.filter(F.col("IATA_CODE").rlike("^[A-Z]{3}$"))

    df_clean = df_clean \
        .withColumn("IATA_CODE", F.trim("IATA_CODE")) \
        .withColumn("AIRPORT", F.trim("AIRPORT")) \
        .withColumn("CITY", F.trim("CITY")) \
        .withColumn("STATE", F.trim("STATE")) \
        .withColumn("COUNTRY", F.trim("COUNTRY")) 

    df_clean = df_clean.filter(
        (F.col("LATITUDE") > -90) & (F.col("LATITUDE") < 90) & (F.col("LONGITUDE") > -180) & (F.col("LONGITUDE") < 180)
    )

    df_clean = df_clean.dropDuplicates(subset=["IATA_CODE"])
    return df_clean

def clean_flight(df):
    df_clean = df.dropna(subset=['FlightDate', 'Airline', 'Dep_Airport', 'Arr_Airport'])

    df_clean = df_clean.withColumn("FlightDate", F.to_date(F.col("FlightDate"), "yyyy-MM-dd HH:mm:ss"))
    df_clean = df_clean.filter(F.col("Day_Of_Week").between(1, 7))
    df_clean = df_clean.filter(F.col("Dep_Delay_Tag").between(0,1)) 
    df_clean = df_clean.filter(F.col("Flight_Duration") > 0)

    string_cols = ["Airline", "Tail_Number", "Dep_Airport", "Dep_CityName", "DepTime_label", "Dep_Delay_Type", "Arr_Airport", "Arr_CityName", "Arr_Delay_Type", "Manufacturer", "Model"]
    for col_name in string_cols:
        df_clean = df_clean.withColumn(col_name, F.trim(col_name))

    int_cols = [
        "Arr_Delay", "Flight_Duration", "Delay_Carrier", 
        "Delay_Weather", "Delay_NAS", "Delay_Security", 
        "Delay_LastAircraft", "Aircraft_age"
    ]

    for col_name in int_cols:
        df_clean = df_clean.withColumn(col_name, F.col(col_name).cast("int"))

    return df_clean

def can_div_clean(df):
    df_clean = df.dropna(subset=['FlightDate', 'Airline', 'Dep_Airport', 'Arr_Airport'])
    df_clean = df.withColumn("FlightDate", F.to_date(F.col("FlightDate"), "yyyy-MM-dd HH:mm:ss"))
    df_clean = df_clean.filter(F.col("Day_Of_Week").between(1, 7))
    df_clean = df_clean.filter(F.col("Dep_Delay_Tag").between(0,1)) 

    string_cols = ["Airline", "Tail_Number", "Dep_Airport", "Dep_CityName", "DepTime_label", "Dep_Delay_Type", "Arr_Airport", "Arr_CityName", "Arr_Delay_Type", "Distance_type"]
    for col_name in string_cols:
        df_clean = df_clean.withColumn(col_name, F.trim(col_name))

    int_cols = [
        "Cancelled", "Diverted", "Dep_Delay", "Dep_Delay_Tag", 
        "Arr_Delay", "Flight_Duration", "Delay_Carrier", 
    ]
    for col_name in int_cols:
        df_clean = df_clean.withColumn(col_name, F.col(col_name).cast("int"))

    return df_clean

def weather_clean(df):
    df_clean = df.dropna(subset=['time'])
    df_clean = df_clean.withColumn("time", F.to_date(F.col("time"), "yyyy-MM-dd HH:mm:ss"))

    weather_float = ['tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wdir', 'wspd', 'pres']
    for col_name in weather_float:
        df_clean = df_clean.withColumn(col_name, F.col(col_name).cast("float"))

    df_clean = df_clean.withColumn("airport_id", F.trim("airport_id"))
    
    return df_clean


if __name__ == "__main__":
    S3_BUCKET = os.getenv("TARGET_S3_BUCKET")

    spark = SparkSession.builder \
        .appName("S3Integration") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.115") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config("spark.hadoop.fs.s3a.threads.keepalivetime", "60") \
        .config("spark.hadoop.fs.s3a.connection.timeout", "60000") \
        .config("spark.hadoop.fs.s3a.connection.establish.timeout", "5000") \
        .config("spark.hadoop.fs.s3a.multipart.purge.age", "86400") \
        .getOrCreate()

    airport_geo_schema = types.StructType([
        types.StructField('IATA_CODE', types.StringType(), True), 
        types.StructField('AIRPORT', types.StringType(), True), 
        types.StructField('CITY', types.StringType(), True), 
        types.StructField('STATE', types.StringType(), True), 
        types.StructField('COUNTRY', types.StringType(), True), 
        types.StructField('LATITUDE', types.DoubleType(), True), 
        types.StructField('LONGITUDE', types.DoubleType(), True)]
    )

    df_airport_geo = spark.read \
        .option("header", "true") \
        .schema(airport_geo_schema) \
        .csv(f"s3a://{S3_BUCKET}/raw_flights/airports_geolocation.csv")

    df_airport_geo_clean = clean_airport_geo(df_airport_geo)
    df_airport_geo_clean.write.parquet(f"s3a://{S3_BUCKET}/clean/geo",mode="overwrite")


    flights_schema = types.StructType([
        types.StructField('FlightDate', types.TimestampType(), True), 
        types.StructField('Day_Of_Week', types.IntegerType(), True), 
        types.StructField('Airline', types.StringType(), True), 
        types.StructField('Tail_Number', types.StringType(), True), 
        types.StructField('Dep_Airport', types.StringType(), True), 
        types.StructField('Dep_CityName', types.StringType(), True), 
        types.StructField('DepTime_label', types.StringType(), True), 
        types.StructField('Dep_Delay', types.IntegerType(), True), 
        types.StructField('Dep_Delay_Tag', types.IntegerType(), True), 
        types.StructField('Dep_Delay_Type', types.StringType(), True), 
        types.StructField('Arr_Airport', types.StringType(), True), 
        types.StructField('Arr_CityName', types.StringType(), True), 
        types.StructField('Arr_Delay', types.IntegerType(), True), 
        types.StructField('Arr_Delay_Type', types.StringType(), True), 
        types.StructField('Flight_Duration', types.IntegerType(), True), 
        types.StructField('Distance_type', types.StringType(), True), 
        types.StructField('Delay_Carrier', types.IntegerType(), True), 
        types.StructField('Delay_Weather', types.IntegerType(), True), 
        types.StructField('Delay_NAS', types.IntegerType(), True), 
        types.StructField('Delay_Security', types.IntegerType(), True), 
        types.StructField('Delay_LastAircraft', types.IntegerType(), True), 
        types.StructField('Manufacturer', types.StringType(), True), 
        types.StructField('Model', types.StringType(), True), 
        types.StructField('Aicraft_age', types.IntegerType(), True)]
    )

    df_flights = spark.read \
        .option("header", "true") \
        .schema(flights_schema) \
        .csv(f"s3a://{S3_BUCKET}/raw_flights/US_flights_2023.csv")
    df_flights_clean = clean_flight(df_flights)

    df_flights_24 = spark.read \
        .option("header", "true") \
        .schema(flights_schema) \
        .csv(f"s3a://{S3_BUCKET}/raw_flights/maj us flight - january 2024.csv")
    df_flights_24_clean = clean_flight(df_flights_24)

    df_flights_final_clean = df_flights_clean.unionByName(df_flights_24_clean)

    df_flights_final_clean.write.parquet(f"s3a://{S3_BUCKET}/clean/flights", mode="overwrite")


    can_div_schema = types.StructType([
        types.StructField('FlightDate', types.TimestampType(), True), 
        types.StructField('Day_Of_Week', types.IntegerType(), True), 
        types.StructField('Airline', types.StringType(), True), 
        types.StructField('Tail_Number', types.StringType(), True), 
        types.StructField('Cancelled', types.IntegerType(), True), 
        types.StructField('Diverted', types.IntegerType(), True), 
        types.StructField('Dep_Airport', types.StringType(), True), 
        types.StructField('Dep_CityName', types.StringType(), True), 
        types.StructField('DepTime_label', types.StringType(), True), 
        types.StructField('Dep_Delay', types.IntegerType(), True), 
        types.StructField('Dep_Delay_Tag', types.IntegerType(), True), 
        types.StructField('Dep_Delay_Type', types.StringType(), True), 
        types.StructField('Arr_Airport', types.StringType(), True), 
        types.StructField('Arr_CityName', types.StringType(), True), 
        types.StructField('Arr_Delay', types.IntegerType(), True), 
        types.StructField('Arr_Delay_Type', types.StringType(), True), 
        types.StructField('Flight_Duration', types.IntegerType(), True), 
        types.StructField('Distance_type', types.StringType(), True), 
        types.StructField('Delay_Carrier', types.IntegerType(), True), 
        types.StructField('Delay_Weather', types.IntegerType(), True), 
        types.StructField('Delay_NAS', types.IntegerType(), True), 
        types.StructField('Delay_Security', types.IntegerType(), True), 
        types.StructField('Delay_LastAircraft', types.IntegerType(), True)]
    )

    df_can_div = spark.read \
        .option("header", "true") \
        .schema(can_div_schema) \
        .csv(f"s3a://{S3_BUCKET}/raw_flights/Cancelled_Diverted_2023.csv")
    df_can_div_clean = can_div_clean(df_can_div)

    df_can_div_clean.write.parquet(f"s3a://{S3_BUCKET}/clean/cancelled_diverted", mode="overwrite")


    weather_schema = types.StructType([
        types.StructField('time', types.TimestampType(), True), 
        types.StructField('tavg', types.FloatType(), True), 
        types.StructField('tmin', types.FloatType(), True), 
        types.StructField('tmax', types.FloatType(), True), 
        types.StructField('prcp', types.FloatType(), True), 
        types.StructField('snow', types.FloatType(), True), 
        types.StructField('wdir', types.FloatType(), True), 
        types.StructField('wspd', types.FloatType(), True), 
        types.StructField('pres', types.FloatType(), True), 
        types.StructField('airport_id', types.StringType(), True)]
    )

    df_weather= spark.read \
        .option("header", "true") \
        .schema(weather_schema) \
        .csv(f"s3a://{S3_BUCKET}/raw_flights/weather_meteo_by_airport.csv")
    df_weather_clean = weather_clean(df_weather)

    df_weather_clean.write.parquet(f"s3a://{S3_BUCKET}/clean/weather", mode="overwrite")

    spark.stop()


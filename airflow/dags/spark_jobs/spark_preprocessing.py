from pyspark.sql import SparkSession
from pyspark.sql import types
import os

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

df_airport_geo_clean = spark.read \
    .option("header", "true") \
    .schema(airport_geo_schema) \
    .csv(f"s3a://{S3_BUCKET}/raw_flights/airports_geolocation.csv")

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

df_flights_clean = spark.read \
    .option("header", "true") \
    .schema(flights_schema) \
    .csv(f"s3a://{S3_BUCKET}/raw_flights/US_flights_2023.csv")

df_flights_24_clean = spark.read \
    .option("header", "true") \
    .schema(flights_schema) \
    .csv(f"s3a://{S3_BUCKET}/raw_flights/maj us flight - january 2024.csv")

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

df_can_div_clean = spark.read \
    .option("header", "true") \
    .schema(can_div_schema) \
    .csv(f"s3a://{S3_BUCKET}/raw_flights/Cancelled_Diverted_2023.csv")

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

df_weather_clean = spark.read \
    .option("header", "true") \
    .schema(weather_schema) \
    .csv(f"s3a://{S3_BUCKET}/raw_flights/weather_meteo_by_airport.csv")

df_weather_clean.write.parquet(f"s3a://{S3_BUCKET}/clean/weather", mode="overwrite")

spark.stop()
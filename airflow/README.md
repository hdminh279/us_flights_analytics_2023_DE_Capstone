# 🚀 Airflow DAGs - Data Pipeline Orchestration

## Overview

This directory contains Apache Airflow DAGs that orchestrate the entire data pipeline from data ingestion through transformation. Airflow manages task dependencies, scheduling, retry logic, and monitoring.

---

## 📊 Pipeline DAG: `flight_delay_pipeline`

### DAG Configuration

```python
DAG ID: flight_delay_pipeline
Schedule: @once (can be changed to 0 0 * * * for daily)
Start Date: 2026-03-21
Catchup: False
Retries: 1 per task (5 minute delay on failure)
Executor: LocalExecutor (Docker)
```

### DAG Graph

```
┌─────────────────────┐
│ create_tmp_folder   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ download_kaggle_data│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   upload_to_s3      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   cleanup_tmp       │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────┐
│ spark_preprocessing_job  │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ dbt_install_packages     │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ dbt_create_tables        │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ dbt_run_models           │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ dbt_test_models          │
└──────────────────────────┘
```

---

## 📋 Pipeline Stages & Tasks

### **STAGE 1: INGEST - Raw Data Ingestion**

#### Task 1: `create_tmp_folder`
- **Type**: BashOperator
- **Purpose**: Create temporary directory for Kaggle download on Container
- **Command**: `mkdir -p /tmp/kaggle_data`

#### Task 2: `download_kaggle_data`
- **Type**: BashOperator
- **Purpose**: Download 2023 US Civil Flights dataset from Kaggle
- **Dataset**: `bordanova/2023-us-civil-flights-delay-meteo-and-aircraft`
- **Size**: ~1.7 GB (6M+ rows)
- **Files**: 
  - `US_flights_2023.csv`
  - `airports_geolocation.csv`
  - `weather_meteo_by_airport.csv`
  - `Cancelled_Diverted.csv`
  - `maj us flight.csv`
- **Output Location**: `/tmp/kaggle_data/`
- **Requirements**: Kaggle CLI credentials in `.env`

#### Task 3: `upload_to_s3`
- **Type**: BashOperator
- **Purpose**: Sync downloaded data to AWS S3 raw data lake
- **Source**: `/tmp/kaggle_data/*`
- **Destination**: `s3://TARGET_S3_BUCKET/raw_flights/`
- **Command**: `aws s3 sync /tmp/kaggle_data s3://${TARGET_S3_BUCKET}/raw_flights/`

#### Task 4: `cleanup_tmp`
- **Type**: BashOperator
- **Purpose**: Remove temporary files to free disk space
- **Command**: `rm -rf /tmp/kaggle_data`

---

### **STAGE 2: PROCESS - Data Cleaning & Transformation**

#### Task 5: `spark_preprocessing_job`
- **Type**: BashOperator (SparkSubmit)
- **Purpose**: Clean, validate, and convert raw data to Parquet format
- **Job File**: `spark_jobs/spark_preprocessing.py`
- **Key Operations**:
  - Read CSV files from S3 Raw bucket
  - Infer and validate schemas
  - Convert columns to appropriate data types
  - Save as Parquet with Snappy compression
- **Output Bucket**: `s3://TARGET_S3_BUCKET/clean_flights/`
- **Spark Configuration**:
  ```
  --packages org.apache.hadoop:hadoop-aws:3.3.2
  --packages com.amazonaws:aws-java-sdk-bundle:1.12.115
  ```

See [../spark_jobs/README.md](../spark_jobs/README.md) for detailed Spark job documentation.

---

### **STAGE 3: TRANSFORM - dbt Analytics Engineering**

#### Task 6: `dbt_install_packages`
- **Type**: BashOperator
- **Purpose**: Install dbt package dependencies
- **Command**: `dbt deps`
- **Location**: `dbt_transform/us_flight_analytics/`
- **Output**: Downloads packages to `dbt_packages/` directory

#### Task 7: `dbt_create_tables`
- **Type**: BashOperator
- **Purpose**: Create tables in Athena to get data from S3
- **Command**: `dbt run-operation create_external_tables`
- **Location**: `dbt_transform/us_flight_analytics/macros`
- **Output**: Creates tables/views in AWS Athena + S3

#### Task 8: `dbt_run_models`
- **Type**: BashOperator
- **Purpose**: Build all dbt models (staging → intermediate → business)
- **Command**: `dbt run`
- **Number of Models**: ~15-20 models
- **Execution**: Sequential (respects dependencies)
- **Output**: Creates tables/views in AWS Athena + S3


#### Task 9: `dbt_test_models`
- **Type**: BashOperator
- **Purpose**: Run automated dbt tests and data quality checks
- **Command**: `dbt test`
- **Test Types**: 
  - Schema tests (uniqueness, not-null, referential integrity)
  - Custom SQL tests (data validation logic)
- **Failure Handling**: Pipeline fails if any test fails

---


## 🚀 Running the Pipeline

### Via Airflow UI

1. Navigate to `http://localhost:8080`
2. Find `flight_delay_pipeline` in the DAGs list
3. Click the **Trigger DAG** button
4. Monitor execution in real-time

---

## 🐛 Troubleshooting

### Common Issues

**PostgreSQL Connection Error**
```bash
docker-compose down -v
docker-compose up -d
# Wait 30 seconds for DB initialization
```

**Permission Denied Errors**
```bash
sudo chown -R 50000:0 airflow/logs
```

**Out of Memory**
```bash
# Reduce Spark memory in DAG
spark.driver.memory=2g
spark.executor.memory=2g
```

---

## 🔗 Related Documentation

- [Main README](../README.md) - Project overview
- [Spark Jobs](../spark_jobs/README.md) - Data processing details
- [dbt Models](dbt_transform/us_flight_analytics/README.md) - Transformation logic

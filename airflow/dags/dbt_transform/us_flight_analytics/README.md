# 📊 dbt - Data Build Tool (Analytics Engineering)

## Overview

**dbt** (data build tool) is an analytics engineering platform that transforms raw data into clean, validated datasets using SQL and Python. This project uses dbt to:

- Build **staging models** (raw data standardization)
- Create **intermediate models** (feature engineering)
- Generate **business models** (aggregated facts and dimensions for BI)
- Run **automated tests** (data quality validation)
- Generate **documentation** (data lineage and context)

---

## 🏗️ Project Structure

### Directory Layout

```
us_flight_analytics/
├── dbt_project.yml           # Project configuration
├── profiles.yml              # Connection profiles (AWS Athena)
├── README.md                 # This file
├── models/                   # SQL transformation models
│   ├── staging/              # Stage 1: Raw data standardization
│   ├── intermediate/         # Stage 2: Feature engineering
│   └── business/             # Stage 3: Analytics-ready tables
├── tests/                    # Data quality tests
├── macros/                   # Reusable SQL functions
├── analyses/                 # Ad-hoc analysis queries
├── seeds/                    # Static reference data (CSV)
├── snapshots/                # Slowly Changing Dimensions (SCD)
├── docs/                     # Custom documentation
└── target/                   # Compiled models (auto-generated)
```

---

## ⚙️ Configuration

### `dbt_project.yml` - Project Config

```yaml
name: 'us_flight_analytics'
version: '1.0.0'
profile: 'us_flight_analytics'

# Path configurations
model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

clean-targets:
  - "target"
  - "dbt_packages"

# Model materialization settings
models:
  us_flight_analytics:
    # Staging layer: VIEWs (no storage)
    staging:
      +materialized: view
    
    # Intermediate layer: VIEWs (logical grouping)
    intermediate:
      +materialized: view
    
    # Business layer: TABLEs (optimized for queries)
    business:
      +materialized: table
      +format: parquet
      +write_compression: snappy
```

### `profiles.yml` - Database Connection

```yaml
us_flight_analytics:
  target: athena_dev
  outputs:
    athena_dev:
      type: athena
      method: iam_role  # or access_key_id + secret_access_key
      role_arn: arn:aws:iam::ACCOUNT_ID:role/dbt-role
      database: us_flight_database
      s3_output_path: s3://us-flight-analytics-athena-result/
      s3_output_encryption: false
      region_name: us-east-1
      schema: analytics
```

---

## 🔄 Three-Layer Transformation Architecture

### **LAYER 1: STAGING** 
#### Purpose: Standardization & Cleaning
**Materialization**: VIEW  
**Input**: Clean Parquet files from Spark (S3 `clean_flights/`)  
**Output**: Standardized, renamed columns ready for analysis

#### Models:
- `stg_flights` - Standardized flight records
- `stg_airports` - Airport dimension
- `stg_weather` - Weather facts
- `stg_airlines` - Airline dimension

#### Example: `stg_flights.sql`
```sql
{{ config(
    materialized='view',
    description='Standardized flight records from raw data'
) }}

SELECT
    -- Surrogate key for analytics
    CAST(FLIGHT_ID AS STRING) AS flight_key,
    
    -- Dimensions
    CAST(AIRLINE AS STRING) AS airline_code,
    CAST(DEPARTURE_AIRPORT AS STRING) AS origin_airport_code,
    CAST(ARRIVAL_AIRPORT AS STRING) AS destination_airport_code,
    
    -- Facts
    CAST(FLIGHT_DISTANCE AS INTEGER) AS flight_distance_miles,
    CAST(DELAY_MINUTES AS INTEGER) AS departure_delay_minutes,
    CAST(CANCELLED AS BOOLEAN) AS is_cancelled,
    
    -- Dates
    CAST(DATE(SCHEDULED_DEPARTURE) AS DATE) AS scheduled_departure_date,
    CAST(DATE(ACTUAL_DEPARTURE) AS DATE) AS actual_departure_date,
    
    -- Metadata
    CURRENT_TIMESTAMP AS dbt_loaded_at,
    '{{ var("load_id") }}' AS load_id

FROM {{ source('raw_flights', 'flights') }}

WHERE SCHEDULED_DEPARTURE >= '2023-01-01'
  AND SCHEDULED_DEPARTURE < '2024-01-01'
```

---

### **LAYER 2: INTERMEDIATE**
#### Purpose: Feature Engineering & Complex Logic
**Materialization**: VIEW  
**Input**: Staging models  
**Output**: Enriched datasets with business logic

#### Models:
- `int_flights_enhanced` - Flights with geographic + weather context
- `int_airline_daily_summary` - Aggregated daily stats per airline
- `int_route_performance` - Route-level metrics
- `int_delay_patterns` - Temporal patterns (hour, dow, month)

---

### **LAYER 3: BUSINESS**
#### Purpose: Analytics-Ready Aggregated Datasets
**Materialization**: TABLE (Parquet, Snappy compressed)  
**Input**: Intermediate models  
**Output**: Ready for BI dashboards

#### Core Models:

1. **`fct_flights`** - Flight Facts Table
2. **`dim_airline`** - Airline Dimension
3. **`dim_airport`** - Airport Dimension
4. **`fct_airline_daily_performance`** - Airline Daily Stats
5. **`fct_route_analytics`** - Route-Level Analytics

---

## 🧪 Tests & Data Quality

### Test Types

- **Uniqueness Tests**: Ensure key columns have no duplicates
- **Not-Null Tests**: Validate required columns are populated
- **Referential Integrity**: Check foreign key relationships
- **Custom SQL Tests**: Domain-specific validation logic

### Running Tests

```bash
# All tests
dbt test

# Tests for specific model
dbt test --select fct_flights

# Run with debug output
dbt test --debug

# Run tests and fail on warnings
dbt test --warn-error
```

---

## 📚 dbt Commands

### Initialization
```bash
# Install dependencies
dbt deps

# Debug connections
dbt debug
```

### Development
```bash
# Run all models
dbt run

# Run specific model
dbt run --select stg_flights

# Run model and its downstream dependencies
dbt run --select +fct_flights+
```

### Testing & Quality
```bash
# Run all tests
dbt test

# Generate documentation
dbt docs generate

# Start local docs server
dbt docs serve
```

### Utilities
```bash
# Freshness check on sources
dbt source freshness

# Create snapshots (SCD)
dbt snapshot

# Compile without running
dbt compile
```

---

## 🚀 Running in Production

### Via Airflow

```bash
cd /opt/airflow/dags/dbt_transform/us_flight_analytics

# Install packages
dbt deps

# Run all models
dbt run

# Run tests
dbt test
```

### Via Docker

```bash
docker-compose exec airflow-webserver bash
cd /opt/airflow/dags/dbt_transform/us_flight_analytics
dbt run --profiles-dir .
dbt test --profiles-dir .
```

---

## 🐛 Troubleshooting

### Connection Issues
```bash
dbt debug

# Profile not found error
dbt debug --profiles-dir .
```

### Model Failures
```bash
# Run with debug output
dbt run --select stg_flights --debug

# Compile to check SQL syntax
dbt compile --select stg_flights
```

### Test Failures
```bash
# Show failing test details
dbt test --select test_name --debug
```

---

## 📚 Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [dbt Athena Plugin](https://github.com/Tomme/dbt-athena)
- [Discourse Community](https://discourse.getdbt.com/)

---

## 🔗 Related Documentation

- [Main README](../../../../README.md) - Project overview
- [Airflow DAGs](../../../README.md) - Pipeline orchestration
- [Spark Processing](../../../../spark_jobs/README.md) - Data ingestion
- [Infrastructure](../../../../infra/README.md) - AWS setup

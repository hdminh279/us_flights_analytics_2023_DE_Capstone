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
---

## 🔄 Three-Layer Transformation Architecture

### **LAYER 1: STAGING** 
#### Purpose: Standardization & Cleaning
**Materialization**: VIEW  
**Input**: Clean Parquet files from Spark (S3 `clean_flights/`)  
**Output**: Standardized, renamed columns ready for analysis

---

### **LAYER 2: INTERMEDIATE**
#### Purpose: Feature Engineering & Complex Logic
**Materialization**: VIEW  
**Input**: Staging models  
**Output**: Enriched datasets with business logic

---

### **LAYER 3: BUSINESS**
#### Purpose: Analytics-Ready Aggregated Datasets
**Materialization**: TABLE (Parquet, Snappy compressed)  
**Input**: Intermediate models  
**Output**: Ready for BI dashboards

---

## 🧪 Tests & Data Quality

### Test Types

- **Uniqueness Tests**: Ensure key columns have no duplicates
- **Not-Null Tests**: Validate required columns are populated
- **Referential Integrity**: Check foreign key relationships
- **Custom SQL Tests**: Domain-specific validation logic

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

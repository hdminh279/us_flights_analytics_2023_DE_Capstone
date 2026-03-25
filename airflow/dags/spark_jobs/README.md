# 🔥 Apache Spark Data Processing

## Overview

This directory contains Apache Spark jobs for large-scale data cleaning, validation, and transformation. The primary job `spark_preprocessing.py` takes raw CSV data from S3 and converts it to optimized Parquet format for downstream analytics.

---

## 📊 Pipeline: Spark Data Preprocessing

### Purpose
- **Input**: Raw CSV files from Kaggle (stored in S3)
- **Processing**: Data cleaning, schema inference, type casting, missing value handling
- **Output**: Optimized Parquet files with Snappy compression (stored in S3)
- **Scale**: Processes 6M+ rows efficiently using distributed computing
- **Cost**: Parquet reduces storage by 60-70% vs CSV + enables faster queries

---

### Jupyter Notebook Development

See `spark_preprocessing.ipynb` for interactive development and testing.

**Usage**:
```bash
jupyter notebook spark_jobs/spark_preprocessing.ipynb
```

### Converting Notebook to Script

```bash
jupyter nbconvert --to script spark_preprocessing.ipynb
```

---

## 📖 References

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)
- [Parquet Format](https://parquet.apache.org/)
- [AWS S3 with Spark](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-configure.html)

---

## 🔗 Related Documentation

- [Main README](../README.md) - Project overview
- [Airflow DAGs](../airflow/README.md) - Pipeline orchestration
- [dbt Models](../airflow/dags/dbt_transform/us_flight_analytics/README.md) - Transformation
- [Infrastructure](../infra/README.md) - AWS setup

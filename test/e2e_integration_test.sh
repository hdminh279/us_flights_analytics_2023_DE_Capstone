#!/bin/bash

echo "🚀 Starting End-to-End Integration Test..."

if [ -f .env ]; then
  set -a
  source .env
  set +a
  echo "Loaded environment variables from .env"
else
  echo ".env file not found in the root directory! E2E Test aborted."
  exit 1
fi

echo "----------------------------------------"
echo "Step 1: Running Spark Preprocessing Job"
uv run python airflow/dags/spark_jobs/spark_preprocessing.py

if [ $? -eq 0 ]; then
  echo "Spark Job completed successfully!"
else
  echo "Spark Job failed! E2E Test aborted."
  exit 1
fi

echo "----------------------------------------"
echo "🛠️ Step 2: Running dbt Transformations"
cd airflow/dags/dbt_transform/us_flight_analytics

uv run dbt run

if [ $? -eq 0 ]; then
  echo "dbt run completed successfully!"
else
  echo "dbt run failed! E2E Test aborted."
  exit 1
fi

echo "----------------------------------------"
echo "🛠️ Step 3: Validating Data with dbt test"
uv run dbt test

if [ $? -eq 0 ]; then
  echo "dbt tests passed!"
  echo "E2E INTEGRATION TEST SUCCESSFUL! Pipeline is ready for Production."
else
  echo "dbt tests failed! E2E Test aborted."
  exit 1
fi

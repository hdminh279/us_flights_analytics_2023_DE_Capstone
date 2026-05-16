FROM apache/airflow:2.9.0

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         default-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir uv

RUN uv pip install --system --no-cache \
   "apache-airflow==2.9.0" \
    pyspark==3.5.0 \
    dbt-core==1.9.0 \
    dbt-athena-community==1.10.0 \
    apache-airflow-providers-apache-spark==4.8.0 \
    awscli \
    kaggle

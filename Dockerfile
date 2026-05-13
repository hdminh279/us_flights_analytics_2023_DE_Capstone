FROM apache/airflow:2.9.0

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         default-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir \
    pyspark==3.5.0 \
    dbt-core==1.9.0 \
    dbt-athena-community==1.10.0 \
    awscli \
    kaggle

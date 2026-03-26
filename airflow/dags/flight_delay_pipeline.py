from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="flight_delay_pipeline",
    
    default_args = {
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    },

    description="End-to-End Pipeline: Kaggle -> S3(Raw) -> Spark -> S3(Clean) -> dbt/Athena -> S3(Bussiness)",
    schedule_interval='@once',
    start_date=datetime(2026, 3, 21),
    catchup=False,
    tags=["kaggle", "spark", "dbt", "athena"],
) as dag:
    
    """
    ========= STAGE 1: INGEST =========
    """
    create_tmp = BashOperator(
        task_id="create_tmp_folder",
        bash_command="mkdir -p /tmp/kaggle_data"
    )

    download_data = BashOperator(
        task_id = "download_kaggle_data",
        bash_command = """
        kaggle datasets download bordanova/2023-us-civil-flights-delay-meteo-and-aircraft \
        -p /tmp/kaggle_data --unzip
        """
    )

    upload_s3 = BashOperator(
        task_id = "upload_to_s3",
        bash_command = "aws s3 sync /tmp/kaggle_data s3://${TARGET_S3_BUCKET}/raw_flights/"
    )

    cleanup = BashOperator(
        task_id = "cleanup_tmp",
        bash_command = "rm -rf /tmp/kaggle_data"
    )

    """
    ========= STAGE 2: SPARK PREPROCESSING =========
    """

    spark_clean_data = BashOperator(
        task_id = "spark_preprocessing_job",
        bash_command = """spark-submit \
        --packages org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.115 \
        /opt/airflow/dags/spark_jobs/spark_preprocessing.py
        """
    )


    """
    ========= STAGE 3: dbt/Athena Transform =========
    """

    DBT_PROJECT_DIR = "/opt/airflow/dags/dbt_transform/us_flight_analytics"

    dbt_deps = BashOperator(
        task_id="dbt_install_packages",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt deps"
    )

    dbt_run = BashOperator(
        task_id="dbt_run_models",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run"
    )

    dbt_create_tables = BashOperator(
        task_id="dbt_create_external_tables",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run-operation create_external_tables"
    )

    dbt_test = BashOperator(
        task_id="dbt_test_models",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt test"
    )

    create_tmp >> download_data >> upload_s3 >> cleanup >> spark_clean_data >> dbt_deps >> dbt_create_tables >> dbt_run >> dbt_test
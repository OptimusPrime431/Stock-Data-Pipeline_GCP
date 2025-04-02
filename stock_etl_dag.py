from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from datetime import timedelta
import subprocess

# Constants
PROJECT_ID = "qwiklabs-gcp-03-ace2e7e66b0f"
REGION = "us-east1"
CLUSTER_NAME = "stock-data"
BUCKET = "stock-bucket8"
BQ_DATASET = "stock_data"
BQ_TABLE = "stock"

# GCS locations for scripts
TRANSFORM_SCRIPT = f"gs://{BUCKET}/scripts/spark_weekly.py"

# Local path to script inside Composer's environment
LOCAL_EXTRACT_SCRIPT_PATH = "/home/airflow/gcs/data/fetch_weekly.py"

# DAG defaults
default_args = {
    "owner": "Karthik",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=3),
}

# ✅ Define the Python callable OUTSIDE the DAG block
def run_extract_script():
    subprocess.run(["python3", LOCAL_EXTRACT_SCRIPT_PATH], check=True)

with DAG(
    dag_id="weekly_stock_data_etl",
    default_args=default_args,
    start_date=datetime(2025, 4, 2, 13, 0, tzinfo=local_tz),
    schedule_interval="0 13 * * 3",  # Every Wednesday at 1 PM EST
    catchup=False,
    tags=["stock", "gcp", "etl"],
    description="ETL pipeline to fetch, transform and load stock data to BigQuery weekly",
) as dag:

    extract_job = PythonOperator(
        task_id="extract_stock_data",
        python_callable=run_extract_script
    )

    transform_job = DataprocSubmitJobOperator(
        task_id="transform_stock_data",
        project_id=PROJECT_ID,
        region=REGION,
        job={
            "placement": {"cluster_name": CLUSTER_NAME},
            "pyspark_job": {
                "main_python_file_uri": TRANSFORM_SCRIPT,
            },
        },
    )

    load_to_bq = BigQueryInsertJobOperator(
        task_id="load_to_bigquery",
        configuration={
            "load": {
                "sourceUris": [f"gs://{BUCKET}/stock_transformed/date={{{{ ds }}}}/part-*.parquet"],
                "destinationTable": {
                    "projectId": PROJECT_ID,
                    "datasetId": BQ_DATASET,
                    "tableId": BQ_TABLE,
                },
                "sourceFormat": "PARQUET",
                "writeDisposition": "WRITE_APPEND",
                "autodetect": True,
            }
        },
        location="US",
    )

    extract_job >> transform_job >> load_to_bq

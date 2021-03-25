import os
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.s3_file_transform_operator import S3FileTransformOperator
from airflow.operators.python_operator import PythonOperator
import boto3

start_day = datetime.now() - timedelta(days=2)

default_args = {
    'owner': 'airflow',
    'depends_on': False,
    'start_date': start_day,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    's3_bucket': 'troys-awesome-bucket',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@once'
}

AIRFLOW_HOME = os.environ['AIRFLOW_HOME']

with DAG(
    dag_id='s3_etl',
    default_args=default_args,
    description='Aggregate data from raw bucket to clean bucket',
    catchup=False
    ) as dag:

    etl_task = S3FileTransformOperator(
        task_id='aggregate_data',
        description='calculate total licences by year and month',
        source_s3_key='s3://troys-awesome-bucket/lm_full_load_2021-01-31.csv', #would typically use .format() with timestamp
        dest_s3_key='s3://troys-awesome-bucket/lm_full_metrics_2021-01-31.csv', #again, would typically use dynamic timestamp
        replace=True,
        transform_script=AIRFLOW_HOME+'/myairflow/scripts/etl/practice_pipeline.py'
    )

    etl_task


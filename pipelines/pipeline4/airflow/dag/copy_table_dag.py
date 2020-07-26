from airflow.operators.dummy_operator import DummyOperator
import datetime
from datetime import date, timedelta
import airflow
from google.cloud import storage
import os
import json
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

default_args = {
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(1),
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=2),
}

with airflow.DAG("Copy_Table_BigQuery",
                 default_args=default_args,
                 template_searchpath=['/home/airflow/gcs/data/pipeline4/'],
                 schedule_interval="@once") as dag:
    start_task = DummyOperator(task_id="start")
    stop_task = DummyOperator(task_id="stop")
    copy_records = BigQueryOperator(
        task_id='copy_records',
        sql="myquery.sql",
        use_legacy_sql=False,
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        params=dict(
            destination_project=os.environ['AIRFLOW_VAR_ENTERPRISE_PROJECT'],
            source_project=os.environ['AIRFLOW_VAR_ENTERPRISE_PROJECT']),
        bigquery_conn_id='etl_sa')

    start_task >> copy_records >> stop_task

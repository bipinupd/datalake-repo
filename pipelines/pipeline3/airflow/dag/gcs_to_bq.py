from airflow.operators.dummy_operator import DummyOperator
import datetime
from datetime import date, timedelta
import airflow
from google.cloud import storage
import os
import json
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator

default_args = {
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(1),
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=2),
}

bucket = '{}_ingestion_gcs_to_bq_9876'.format(os.environ['AIRFLOW_VAR_ENV'])
destination_dataset_table = '{}.exampledataset.personal_info'.format(
    os.environ['AIRFLOW_VAR_ENTERPRISE_PROJECT'])

# GCS to BQ operator DAG example
with airflow.DAG("GCS_To_BigQuery",
                 default_args=default_args,
                 schedule_interval="@once") as dag:
    start_task = DummyOperator(task_id="start")
    stop_task = DummyOperator(task_id="stop")
    GCS_to_BQ = GoogleCloudStorageToBigQueryOperator(
        task_id='gcs_to_bq',
        bucket=bucket,
        source_objects=['*.csv'],
        destination_project_dataset_table=destination_dataset_table,
        schema_fields=[
            {
                'name': 'name',
                'type': 'STRING',
                'mode': 'NULLABLE'
            },
            {
                'name': 'email',
                'type': 'STRING',
                'mode': 'NULLABLE'
            },
            {
                'name': 'job',
                'type': 'STRING',
                'mode': 'NULLABLE'
            },
            {
                'name': 'city',
                'type': 'STRING',
                'mode': 'NULLABLE'
            },
            {
                'name': 'country',
                'type': 'STRING',
                'mode': 'NULLABLE'
            },
        ],
        source_format='CSV',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        max_bad_records=900,
        gcp_conn_id='etl_sa')
    start_task >> GCS_to_BQ >> stop_task

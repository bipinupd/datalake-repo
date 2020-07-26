from __future__ import absolute_import

from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import date, timedelta
import airflow
from airflow.contrib.operators.gcs_to_gcs import GoogleCloudStorageToGoogleCloudStorageOperator
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator
import os

default_args = {
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'dataflow_default_options': {
        'project':
        os.environ['AIRFLOW_VAR_WORK_PROJECT'],
        'zone':
        'northamerica-northeast1-b',
        'serviceAccountEmail':
        'dag-trigger@{}.iam.gserviceaccount.com'.format(
            os.environ['AIRFLOW_VAR_WORK_PROJECT']),
        'ipConfiguration':
        'WORKER_IP_PRIVATE',
        'tempLocation':
        'gs://{}_df_templates_8987/pipeline1/temp'.format(
            os.environ['AIRFLOW_VAR_ENV'])
    }
}

with airflow.DAG("Example_Pipeline_P1",
                 default_args=default_args,
                 schedule_interval="@once") as dag:

    start_task = DummyOperator(task_id="start")

    move_to_processing = GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id='move_file_to_processing',
        source_bucket='{}_hr_data_8980'.format(os.environ['AIRFLOW_VAR_ENV']),
        source_object='inbox/*.csv',
        destination_bucket='{}_hr_data_8980'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        destination_object='processing/',
        move_object=True,
        google_cloud_storage_conn_id='etl_sa')

    dataflow_task = DataflowTemplateOperator(
        task_id="invoke_dataflow",
        template="gs://{}_df_templates_8987/pipeline1/pipeline1_template".
        format(os.environ['AIRFLOW_VAR_ENV']),
        job_name='sample_dataflow_example',
        poll_sleep=5,
        parameters={
            'input':
            'gs://{}_hr_data_8980/processing/*.csv'.format(
                os.environ['AIRFLOW_VAR_ENV']),
            'deIdentiyTemplateId':
            'generic_deidentify_template'
        },
        dag=dag,
    )
    move_to_archieve = GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id='move_file_to_archieve',
        source_bucket='{}_hr_data_8980'.format(os.environ['AIRFLOW_VAR_ENV']),
        source_object='/processing/*.csv',
        destination_bucket='{}_hr_data_arc_7856'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        destination_object='/',
        move_object=True,
        google_cloud_storage_conn_id='etl_sa')

    stop_task = DummyOperator(task_id="stop")

    start_task >> move_to_processing >> dataflow_task >> move_to_archieve >> stop_task

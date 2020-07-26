from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators import dataflow_operator
from airflow.contrib.operators.gcs_to_gcs import GoogleCloudStorageToGoogleCloudStorageOperator
from datetime import timedelta
from airflow import models
from airflow import utils
import os

default_dag_args = {
    'start_date': utils.dates.days_ago(1),
    'dataflow_default_options': {
        'project':
        os.environ['AIRFLOW_VAR_WORK_PROJECT'],
        'zone':
        'us-central1-f',
        'inputFile':
        'gs://{}_word_count_data_5696/processing/*'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        'output':
        'gs://{}_word_count_data_5696/output/'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        'stagingLocation':
        'gs://{}_df_templates_8987/pipeline-example/staging'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        'tempLocation':
        'gs://{}_df_templates_8987/pipeline-example/temp'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        'serviceAccount':
        'dag-trigger@{}.iam.gserviceaccount.com'.format(
            os.environ['AIRFLOW_VAR_WORK_PROJECT']),
        'usePublicIps':
        'False'
    }
}

with models.DAG('DAG_WordCount',
                schedule_interval=timedelta(days=1),
                default_args=default_dag_args) as dag:

    start_task = DummyOperator(task_id="start")

    move_to_processing = GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id='move_file_to_processing',
        source_bucket='{}_word_count_data_5696'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        source_object='inbox/*',
        destination_bucket='{}_word_count_data_5696'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        destination_object='processing/',
        move_object=True,
        google_cloud_storage_conn_id='etl_sa')

    dataflow_task = dataflow_operator.DataFlowJavaOperator(
        task_id='dataflow_java_app',
        jar='gs://{}/data/pipeline-example/word-count-beam-0.1.jar'.format(
            os.environ['COMPOSER_BUCKET']),
        options={
            'autoscalingAlgorithm': 'BASIC',
            'maxNumWorkers': '5'
        },
        gcp_conn_id='etl_sa')

    move_to_archieve = GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id='move_file_to_archieve',
        source_bucket='{}_word_count_data_5696'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        source_object='/processing/*',
        destination_bucket='{}_word_count_archive_9696'.format(
            os.environ['AIRFLOW_VAR_ENV']),
        destination_object='/',
        move_object=True,
        google_cloud_storage_conn_id='etl_sa')

    stop_task = DummyOperator(task_id="stop")

    start_task >> move_to_processing >> dataflow_task >> move_to_archieve >> stop_task

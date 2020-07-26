from airflow.models import DagBag
import unittest
import os

#Test for gcs_to_bq_dag
class DAGDependecncyTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        os.environ['AIRFLOW_VAR_ENV'] = 'dev'
        os.environ['AIRFLOW_VAR_WORK_PROJECT'] = 'test'
        os.environ['AIRFLOW_VAR_ENTERPRISE_PROJECT'] = 'test'
        self.dagbag = DagBag()
        self.dag_id = 'GCS_To_BigQuery'

    def test_contain_tasks(self):
        """Check task contains in example_dag dag"""
        dag = self.dagbag.get_dag(self.dag_id)
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        assert sorted(task_ids) == sorted([
            'start', 'gcs_to_bq', 'stop'
        ])

    def test_dependencies_of_print_date(self):
        """Check the task dependencies of dataflow_task in example_dag dag"""
        dag = self.dagbag.get_dag(self.dag_id)
        dataflow_task = dag.get_task('gcs_to_bq')
        upstream_task_ids = list(
            map(lambda task: task.task_id, dataflow_task.upstream_list))
        downstream_task_ids = list(
            map(lambda task: task.task_id, dataflow_task.downstream_list))
        assert sorted(upstream_task_ids) == sorted(['start'])
        assert sorted(downstream_task_ids) == sorted(['stop'])
        

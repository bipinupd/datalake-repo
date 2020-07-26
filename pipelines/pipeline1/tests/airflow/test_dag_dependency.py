from airflow.models import DagBag
import unittest
import os


class DAGDependecncyExample_Pipeline_P1_DAG_Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        os.environ['AIRFLOW_VAR_ENV'] = 'dev'
        os.environ['AIRFLOW_VAR_WORK_PROJECT'] = 'test'
        self.dagbag = DagBag()
        self.dag_id = 'Example_Pipeline_P1'

    def test_contain_tasks(self):
        """Check task contains in example_dag dag"""
        dag = self.dagbag.get_dag(self.dag_id)
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        assert sorted(task_ids) == sorted([
            'start', 'move_file_to_processing', 'invoke_dataflow',
            'move_file_to_archieve', 'stop'
        ])

    def test_dependencies_of_print_date(self):
        """Check the task dependencies of dataflow_task in example_dag dag"""
        dag = self.dagbag.get_dag(self.dag_id)
        dataflow_task = dag.get_task('invoke_dataflow')
        upstream_task_ids = list(
            map(lambda task: task.task_id, dataflow_task.upstream_list))
        downstream_task_ids = list(
            map(lambda task: task.task_id, dataflow_task.downstream_list))
        assert sorted(upstream_task_ids) == sorted(['move_file_to_processing'])
        assert sorted(downstream_task_ids) == sorted(['move_file_to_archieve'])

from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
from apache_beam.testing.test_pipeline import TestPipeline
import apache_beam as beam
from dataflow_python_template import ParseEventFn
import unittest

#Test for gcs_bq_pipeline
class ExamplePipelineTests(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.sample_data = [
            "David N, davidd@test.com,IT,Toronto",
            "Harry M, garry@test.com,Accountant,York",
            "Chris O, chris@test.com,Developer,London",
            "Arjun P, arjun@test.com,Architect,Kingston",
            "Karn Q, karn@test.com,Network Engg,NY",
            "Sri R, srd@test.com,CFO,Toronto"
        ]

    def test_sample_to_User(self):
        EXPECTED_COUNTS = [6]
        with TestPipeline() as p:
            input = p | beam.Create(self.sample_data)
            output = input | beam.ParDo(
                ParseEventFn()) | beam.combiners.Count.Globally()
            assert_that(output,
                        equal_to(EXPECTED_COUNTS),
                        label='CheckOutputCount')

    def test_parseeventfx_removes_extra_space_in_begining_and_last(self):
        EXPECTED_OUTPUT = [
            "David N,davidd@test.com,IT,Toronto",
            "Harry M,garry@test.com,Accountant,York",
            "Chris O,chris@test.com,Developer,London",
            "Arjun P,arjun@test.com,Architect,Kingston",
            "Karn Q,karn@test.com,Network Engg,NY",
            "Sri R,srd@test.com,CFO,Toronto"
        ]
        with TestPipeline() as p:
            input = p | beam.Create(self.sample_data)
            output = input | beam.ParDo(
                ParseEventFn()) | beam.Map(lambda x: str(x))
            assert_that(output,
                        equal_to(EXPECTED_OUTPUT),
                        label='CheckOutputWithtrailingSpaces')

    def test_user_obj_to_bq_row(self):
        EXPECTED_OUTPUT = [{
            'full_name': 'David N',
            'email': 'davidd@test.com',
            'job': 'IT',
            'city': 'Toronto'
        }, {
            'full_name': 'Harry M',
            'email': 'garry@test.com',
            'job': 'Accountant',
            'city': 'York'
        }, {
            'full_name': 'Chris O',
            'email': 'chris@test.com',
            'job': 'Developer',
            'city': 'London'
        }, {
            'full_name': 'Arjun P',
            'email': 'arjun@test.com',
            'job': 'Architect',
            'city': 'Kingston'
        }, {
            'full_name': 'Karn Q',
            'email': 'karn@test.com',
            'job': 'Network Engg',
            'city': 'NY'
        }, {
            'full_name': 'Sri R',
            'email': 'srd@test.com',
            'job': 'CFO',
            'city': 'Toronto'
        }]
        with TestPipeline() as p:
            input = p | beam.Create(self.sample_data)
            output = input | beam.ParDo(
                ParseEventFn()) | beam.Map(lambda x: x.obj_to_Row())
            assert_that(output,
                        equal_to(EXPECTED_OUTPUT),
                        label='CheckOutputWithtrailingSpaces')

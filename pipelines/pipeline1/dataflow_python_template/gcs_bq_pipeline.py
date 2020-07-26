#!/usr/bin/env python
import apache_beam as beam
import sys
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.value_provider import StaticValueProvider


class User:
    def __init__(self, full_name, email, job, city):
        self.full_name = full_name
        self.email = email
        self.job = job
        self.city = city

    def __str__(self):
        return "{},{},{},{}".format(self.full_name, self.email, self.job,
                                    self.city)

    def obj_to_Row(self):
        return {
            'full_name': self.full_name,
            'email': self.email,
            'job': self.job,
            'city': self.city
        }


class TokenizationFxn(beam.DoFn):
    def __init__(self, project_id, template_id):
        self.project_id = project_id
        self.template_id = template_id

    def process(self, elem):
        import google.cloud.dlp
        dlp = google.cloud.dlp_v2.DlpServiceClient()
        data = {"header": ["EMAIL"]}
        headers = [{"name": val} for val in data["header"]]
        rows = []
        for event in elem:
            rows.append({"values": [{"string_value": str(event.email)}]})
        table = {}
        table["headers"] = headers
        table["rows"] = rows
        item = {"table": table}
        parent = dlp.project_path(self.project_id)
        deidentify_template_name = "projects/{}/deidentifyTemplates/{}".format(
            self.project_id, self.template_id.get())
        response = dlp.deidentify_content(
            parent,
            deidentify_template_name=deidentify_template_name,
            item=item)
        i = 0
        for event in elem:
            user = User(event.full_name,
                        response.item.table.rows[i].values[0].string_value,
                        event.job, event.city)
            i = i + 1
            yield user.obj_to_Row()


class RunTimeOptions(PipelineOptions):
    """these are options to be populated at the time the template is instatiated"""
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--bq', required=True)
        parser.add_value_provider_argument(
            '--input',
            help=
            'Input bucket in Google Cloud Storage format: gs://bucket_name/file_name'
        )
        parser.add_value_provider_argument(
            '--deIdentiyTemplateId', help='TemplateId for deIdentification')


class ParseEventFn(beam.DoFn):
    def process(self, elem):
        data = elem.split(",")
        yield User(data[0].strip(), data[1].strip(), data[2].strip(),
                   data[3].strip())


def run(args=None):
    options = PipelineOptions()
    pipeline = beam.Pipeline(options=options)
    runtime_options = options.view_as(RunTimeOptions)
    gcp_proejct = options.view_as(GoogleCloudOptions).project
    pipeline | "Read Files" >> beam.io.ReadFromText(runtime_options.input) |  \
               "Parse Event" >> beam.ParDo(ParseEventFn()) | \
               "BatchElements" >> beam.BatchElements(max_batch_size=200) | \
               "Apply DLP" >> beam.ParDo(TokenizationFxn(gcp_proejct, runtime_options.deIdentiyTemplateId)) | \
               "Write to BigQuery" >>  beam.io.WriteToBigQuery(
                                      runtime_options.bq,
                                      write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                                      create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
    pipeline.run()


if __name__ == '__main__':
    run()

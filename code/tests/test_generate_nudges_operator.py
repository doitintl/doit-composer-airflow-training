import unittest
from unittest import mock
import pytest

from operators.generate_nudges_operator import GenerateNudgesOperator


DUMMY_DATASET_ID = 'dummy_dataset_id'
DUMMY_NON_EXISTED_DATASET_ID = 'dummy_non_existed_dataset_id'
DUMMY_DATASETS = [
    {
        "kind": "bigquery#dataset",
        "location": "US",
        "id": "your-project:dummy_dataset_id",
        "datasetReference": {"projectId": "your-project", "datasetId": "dummy_dataset_id"},
    },
    {
        "kind": "bigquery#dataset",
        "location": "US",
        "id": "your-project:another_dummy_dataset_id",
        "datasetReference": {"projectId": "your-project", "datasetId": "another_dummy_dataset_id"},
    },
]
DUMMY_NUDGES_QUERY = """select ac.email, ac.account_name, i.item_name, i.price, act.visit_time from
`airflow-talk.analytics.activities` act
inner join `airflow-talk.analytics.accounts` ac on ac.account_id = act.account_id
inner join `airflow-talk.analytics.items` i on i.item_id = act.item_id"""
DUMMY_TABLE = "dummy table"


class TestGenerateNudgesOperator(unittest.TestCase):
    @mock.patch('operators.generate_nudges_operator.BigQueryHook')
    def test_generate_nudges(self, mock_hook):
        operator = GenerateNudgesOperator(
            task_id = 'generate_nudges_task',
            nudges_query=DUMMY_NUDGES_QUERY,
            destination_dataset_table=DUMMY_TABLE,
        )

        operator.execute(None)
        mock_hook.return_value.run_query.assert_called_once_with(
            sql = DUMMY_NUDGES_QUERY,
            destination_dataset_table = DUMMY_TABLE,
            write_disposition="WRITE_TRUNCATE",
        )

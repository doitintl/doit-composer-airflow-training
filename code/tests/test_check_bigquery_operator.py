import unittest
from unittest import mock
import pytest

from operators.check_bigquery_dataset_operator import CheckBigQueryOperator
from google.cloud.bigquery.dataset import DatasetListItem


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


class TestCheckBigQueryDatasetOperator(unittest.TestCase):
    @mock.patch('operators.check_bigquery_dataset_operator.BigQueryHook')
    def test_existed_dataset(self, mock_hook):
        operator = CheckBigQueryOperator(
            task_id = 'dataset_exists_task',
            dataset_id = DUMMY_DATASET_ID,
        )

        mock_hook.return_value.get_datasets_list.return_value = [DatasetListItem(d) for d in DUMMY_DATASETS]
        assert operator.execute(None) == True

    @mock.patch('operators.check_bigquery_dataset_operator.BigQueryHook')
    def test_non_existed_dataset(self, mock_hook):
        operator = CheckBigQueryOperator(
            task_id = 'dataset_exists_task',
            dataset_id = DUMMY_NON_EXISTED_DATASET_ID,
        )

        mock_hook.return_value.get_datasets_list.return_value = [DatasetListItem(d) for d in DUMMY_DATASETS]

        with pytest.raises(Exception, match=f"Dataset id {DUMMY_NON_EXISTED_DATASET_ID} not found"):
            operator.execute(None)
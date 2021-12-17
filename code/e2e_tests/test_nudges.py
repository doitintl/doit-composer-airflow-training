# E2E test steps:
# 1. clean up history, raw data from buckets
# 2. clean up bigquery tables
# 3. put test data in GCS buckets
# 4. trigger dag using below command
#    docker-compose run airflow-scheduler airflow dags trigger generate_nudges_dag
# 5. check nudges table

# How to run:
# gcloud auth application-default login
# bash run_e2e_tests.sh

import unittest
from datetime import datetime
import logging
from google.cloud import storage, bigquery
from google.api_core.exceptions import NotFound
from shutil import copyfile
import os
import subprocess
import time

log = logging.getLogger(__name__)

NUDGES_HISTORY_BUCKET = "nudges_history"
STORE_RAW_DATA_BUCKET = "store_raw_data"
DATASET = "analytics"


class TestNudges(unittest.TestCase):
    def setUp(self):
        log.info("Test setup: cleaning up history and raw data from buckets...")

        self.current_date = datetime.today().strftime("%Y-%m-%d")
        self.clean_up_buckets()
        self.clean_up_bigquery()

    def test_nudges(self):
        log.info("Run test: generate and upload raw data to the bucket...")
        self.generate_and_upload_test_files()
        self.trigger_dag()
        time.sleep(20)
        self.check_nudges_in_bigquery()

    # def tearDown(self):
    #     self.clean_up_buckets()
    #     self.clean_up_bigquery()

    # utils
    def clean_up_buckets(self):
        self.delete_blob(NUDGES_HISTORY_BUCKET, self.current_date)
        self.delete_blob(STORE_RAW_DATA_BUCKET, f"accounts_{self.current_date}.csv")
        self.delete_blob(STORE_RAW_DATA_BUCKET, f"activities_{self.current_date}.csv")
        self.delete_blob(STORE_RAW_DATA_BUCKET, f"items_{self.current_date}.csv")

    def delete_blob(self, bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        storage_client = storage.Client(project="airflow-talk")

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        try:
            blob.delete()

            log.info(f"Blob {blob_name} deleted.")
        except NotFound:
            log.info(f"Blob {blob_name} does not exist, pass.")

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        storage_client = storage.Client(project="airflow-talk")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        log.info(f"File {source_file_name} uploaded to {destination_blob_name}.")

    def clean_up_bigquery(self):
        self.delete_table(f"{DATASET}.accounts")
        self.delete_table(f"{DATASET}.activities")
        self.delete_table(f"{DATASET}.items")

    def delete_table(self, table_id):
        client = bigquery.Client(project="airflow-talk")
        client.delete_table(table_id, not_found_ok=True)  # Make an API request.
        log.info(f"Deleted table '{table_id}'.")

    def generate_and_upload_test_files(self):
        dirname = os.path.dirname(__file__)

        for test_file in ["accounts", "activities", "items"]:
            copyfile(
                os.path.join(dirname, f"data/{test_file}.csv"),
                os.path.join(dirname, f"data/{test_file}_{self.current_date}.csv"),
            )
            self.upload_blob(
                STORE_RAW_DATA_BUCKET,
                os.path.join(dirname, f"data/{test_file}_{self.current_date}.csv"),
                f"{test_file}_{self.current_date}.csv",
            )

    def trigger_dag(self):
        subprocess.run(
            "docker-compose run airflow-scheduler airflow dags trigger generate_nudges_dag",
            shell=True,
        )

    def check_nudges_in_bigquery(self):
        client = bigquery.Client(project="airflow-talk")
        query_job = client.query(
            f"""
            SELECT * FROM `{DATASET}.nudges`
            """
        )

        results = query_job.result()  # Waits for job to complete.

        for row in results:
            log.info(f"nudge row: {row}")
            assert row.email == "derrick@doit-intl.com"
            assert row.account_name == "Derrick"
            assert row.item_name == "Google Pixel 5"
            assert row.visit_time.replace(tzinfo=None) == datetime.strptime(
                "2021-04-22 12:54:00", "%Y-%m-%d %H:%M:%S"
            )

from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)

from operators.generate_nudges_operator import GenerateNudgesOperator
from operators.check_bigquery_dataset_operator import CheckBigQueryDatasetOperator

import logging


log = logging.getLogger(__name__)

PROJECT_ID = "derrick-sandbox"
NUDGES_HISTORY_BUCKET = "nudges_history"
STORE_RAW_DATA_BUCKET = "store_raw_data"
CURRENT_DATE = datetime.today().strftime("%Y-%m-%d")
DATASET_ID = "analytics"
NUDGES_QUERY = f"""select ac.email, ac.account_name, i.item_name, i.price, act.visit_time from
`{PROJECT_ID}.analytics.activities` act
inner join `{PROJECT_ID}.analytics.accounts` ac on ac.account_id = act.account_id
inner join `{PROJECT_ID}.analytics.items` i on i.item_id = act.item_id"""


def branch_func(ti):
    xcom_return_value = ti.xcom_pull(task_ids="get_latest_run_date", key="return_value")
    log.info(f"Xcom_return_value: {xcom_return_value}")
    if xcom_return_value:
        log.info("Today's run already exists, finishing the dag...")
        return "finish_run"
    else:
        log.info("Today's run does not exist, kicking off the run...")
        return "kick_off_run"


with DAG(
    "9_generate_nudges_dag",
    description="generate nudges dag",
    schedule_interval=None, #"0 3 * * *",
    start_date=datetime(2021, 12, 20),
    tags=["custom"],
) as dag:

    get_latest_run_date = GCSListObjectsOperator(
        task_id="get_latest_run_date",
        bucket=NUDGES_HISTORY_BUCKET,
        prefix=CURRENT_DATE,
    )

    check_run_date = BranchPythonOperator(
        task_id="check_run_date", python_callable=branch_func
    )
    
    kick_off_run = DummyOperator(task_id="kick_off_run")
    finish_run = DummyOperator(task_id="finish_run")

    check_bigquery_dataset = CheckBigQueryDatasetOperator(
        task_id="check_bigquery_dataset",
        dataset_id=DATASET_ID,
    )

    load_accounts_csv = GCSToBigQueryOperator(
        task_id="load_accounts_csv",
        bucket=STORE_RAW_DATA_BUCKET,
        source_objects=[f"accounts_{CURRENT_DATE}.csv"],
        destination_project_dataset_table=f"{DATASET_ID}.accounts",
        schema_fields=[
            {"name": "account_id", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "account_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "email", "type": "STRING", "mode": "NULLABLE"},
        ],
        write_disposition="WRITE_TRUNCATE",
    )

    load_activities_csv = GCSToBigQueryOperator(
        task_id="load_activities_csv",
        bucket=STORE_RAW_DATA_BUCKET,
        source_objects=[f"activities_{CURRENT_DATE}.csv"],
        destination_project_dataset_table=f"{DATASET_ID}.activities",
        schema_fields=[
            {"name": "account_id", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "item_id", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "visit_time", "type": "TIMESTAMP", "mode": "NULLABLE"},
        ],
        write_disposition="WRITE_TRUNCATE",
    )

    load_items_csv = GCSToBigQueryOperator(
        task_id="load_items_csv",
        bucket=STORE_RAW_DATA_BUCKET,
        source_objects=[f"items_{CURRENT_DATE}.csv"],
        destination_project_dataset_table=f"{DATASET_ID}.items",
        schema_fields=[
            {"name": "item_id", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "item_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "price", "type": "FLOAT", "mode": "NULLABLE"},
        ],
        write_disposition="WRITE_TRUNCATE",
    )

    generate_nudges = GenerateNudgesOperator(
        task_id="generate_nudges",
        nudges_query=NUDGES_QUERY,
        destination_dataset_table="analytics.nudges",
    )

    get_latest_run_date >> check_run_date >> [finish_run, kick_off_run]
    kick_off_run >> check_bigquery_dataset >> [
        load_accounts_csv,
        load_activities_csv,
        load_items_csv,
    ] >> generate_nudges >> finish_run

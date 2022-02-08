from datetime import datetime
import random

from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator

with DAG(
    dag_id="5_braching_dag",
    start_date=datetime(2021, 12, 1),
    schedule_interval="@daily",
    tags=["custom"],
) as dag:
    get_source = DummyOperator(task_id="get_source")

    options = ["type_a_transform", "type_b_transform"]

    branch_check = BranchPythonOperator(
        task_id="branch_check", python_callable=lambda: random.choice(options)
    )
    type_a = DummyOperator(task_id="type_a_transform")
    type_b = DummyOperator(task_id="type_b_transform")

    get_source >> branch_check >> [type_a, type_b]

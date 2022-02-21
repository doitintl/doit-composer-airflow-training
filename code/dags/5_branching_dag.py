from datetime import datetime
import time

from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator

with DAG(
    dag_id="5_braching_dag",
    start_date=datetime(2021, 12, 1),
    catchup=False,
    schedule_interval="@daily",
    tags=["custom"],
) as dag:
    get_source = DummyOperator(task_id="get_source")

    def branch_func():
        if int(time.time()) % 2 == 0:
            return "even_number_transform"
        else:
            return "odd_number_transform"

    branch_check = BranchPythonOperator(
        task_id="branch_check", python_callable=branch_func
    )
    even_number_transform = DummyOperator(task_id="even_number_transform")
    odd_number_transform = DummyOperator(task_id="odd_number_transform")

    get_source >> branch_check >> [even_number_transform, odd_number_transform]

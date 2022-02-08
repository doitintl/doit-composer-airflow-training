from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

import os

sql_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "sql"))
sql_file_names = []


for file in os.listdir(sql_folder):
    if file.endswith(".sql"):
        sql_file_names.append(file)

with DAG(
    "4_dynamic_dag",
    description="my dynamic DAG",
    schedule_interval="0 12 * * *",
    template_searchpath=sql_folder,
    start_date=datetime(2021, 12, 1),
    tags=["custom"],
) as dag:
    d1 = DummyOperator(task_id="kick_off_dag")
    d3 = DummyOperator(task_id="finish_dag")

    for i in sql_file_names:
        d2 = DummyOperator(task_id=f"export_data_for_{i}")
        d1 >> d2 >> d3

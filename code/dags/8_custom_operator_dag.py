from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators.hello_operator import HelloOperator


dag = DAG(
    "8_custom_operator_dag",
    schedule_interval="0 12 * * *",
    start_date=datetime(2021, 12, 1),
    catchup=False,
    tags=["custom"],
)

start = DummyOperator(
    task_id="start",
    dag=dag,
)

hello = HelloOperator(
    task_id="hello",
    operator_param="composer tutorial",
    dag=dag,
)

end = DummyOperator(
    task_id="end",
    dag=dag,
)

start >> hello >> end

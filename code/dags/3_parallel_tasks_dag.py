from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    "3_parallel_tasks_dag",
    default_args=default_args,
    description="parallel tasks Dag",
    schedule_interval="0 12 * * *",
    start_date=datetime(2021, 12, 1),
    catchup=False,
    tags=["custom"],
) as dag:

    t1 = BashOperator(
        task_id="T1",
        bash_command="echo T1",
    )

    t2 = BashOperator(
        task_id="T2",
        bash_command="echo T2",
    )

    t3 = BashOperator(
        task_id="T3",
        bash_command="echo T3",
    )

    t4 = BashOperator(
        task_id="T4",
        bash_command="echo T4",
    )

    #t1 >> t2 >> t3 >> t4
    [t1, t2, t3] >> t4
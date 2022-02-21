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
    "2_context_manager_dag",
    default_args=default_args,
    description="context manager Dag",
    schedule_interval="0 12 * * *",
    start_date=datetime(2021, 12, 1),
    catchup=False,
    tags=["custom"],
) as dag:

    start = BashOperator(
        task_id="start",
        bash_command="echo start",
    )

    end = BashOperator(
        task_id="end",
        bash_command="echo stop",
    )

    start >> end

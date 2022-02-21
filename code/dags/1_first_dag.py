# Step-1: Import Python modules 
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Step-2: Define default args
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
}

# Step-3: Instantiate DAG --- or creating a DAG object
dag = DAG(
    "1_first_dag",
    description="first dag",
    schedule_interval="0 3 * * *",
    start_date=datetime(2022, 2, 17),
    tags=["custom"],
)

# Step-4: Define Tasks
start = BashOperator(
    task_id="start",
    bash_command='echo "start"',
    dag=dag,
)

check_ip = BashOperator(
    task_id="check_ip",
    bash_command='curl checkip.amazonaws.com',
    dag=dag,
)

end = BashOperator(
    task_id="end",
    bash_command='echo "stop"',
    dag=dag,
)

# Step-5. Define task sequence and dependencies
start >> check_ip >> end

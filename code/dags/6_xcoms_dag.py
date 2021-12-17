from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

DAG = DAG(
  dag_id='6_xcoms_dag',
  start_date=datetime.now(),
  schedule_interval='@once',
  tags=['custom']
)

def push_function(**kwargs):
    ls = ['a', 'b', 'c']
    return ls

push_task = PythonOperator(
    task_id='push_task', 
    python_callable=push_function,
    provide_context=True,
    dag=DAG)

def pull_function(**kwargs):
    ti = kwargs['ti']
    ls = ti.xcom_pull(task_ids='push_task')
    print(ls)

pull_task = PythonOperator(
    task_id='pull_task', 
    python_callable=pull_function,
    provide_context=True,
    dag=DAG)

push_task >> pull_task
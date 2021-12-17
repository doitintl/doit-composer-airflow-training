import time
from datetime import datetime
from pprint import pprint

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator


with DAG(
    dag_id='7_python_operator_and_taskflow_dag',
    schedule_interval=None,
    start_date=datetime(2021, 12, 1),
    catchup=False,
    tags=['custom'],
) as dag:
    # 1. print context using PythonOperator
    def print_context(ds, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(kwargs['my_keyword'])
        print(ds)
        return 'Whatever you return gets printed in the logs'

    print_the_context = PythonOperator(
        task_id='print_the_context',
        python_callable=print_context,
        op_kwargs={'my_keyword': 'Airflow'}
    )

    # 2. sleep task using TaskFlow decorator
    @task(task_id='sleep_for_5')
    def my_sleeping_function():
        """This is a function that will run within the DAG execution"""
        time.sleep(5)

    sleeping_task = my_sleeping_function()

    # 3. print context again using TaskFlow decorator
    @task(task_id="print_the_context_again")
    def print_context_again(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(kwargs['my_keyword'])
        print(ds)
        return 'Whatever you return gets printed in the logs'

    print_the_context_again = print_context_again(my_keyword='Airflow')


    print_the_context >> sleeping_task >> print_the_context_again

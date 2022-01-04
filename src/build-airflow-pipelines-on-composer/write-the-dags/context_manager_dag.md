# Context manager DAG
DAGs can be used as [context managers](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers) to assign each Operator/Sensor to that DAG automatically. This can be helpful if you have lots of tasks in a DAG; you don't need to repeat `dag=dag` in each Operator/Sensor. From the latest Airflow document, using context managers is recommended.

Below is a modified version of our first DAG in the previous page.

`code/dags/2_context_manager_dag.py`
```python
{{#include ../../../code/dags/2_context_manager_dag.py}}
```

So far, in the two DAGs that we wrote, the tasks run one by one. It is excellent but may not be the most efficient. What if we have a pipeline, we some tasks that can be running in parallel?

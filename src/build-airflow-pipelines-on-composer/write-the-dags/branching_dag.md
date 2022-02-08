# Branching DAG

When designing data pipelines, there may be use cases that require more complex task flows than "Task A > Task B > Task C". For example, let's say that there is a use case where different tasks need to be chosen to execute based on the results of an upstream task. We call this `branching` in Airflow, and it uses a particular Operator `BranchPythonOperator` to handle this use case.

`BranchPythonOperator` takes a Python function as an input. The function must return a list of task IDs that the DAG should proceed with based on some logic.

To demonstrate branching, let's create a DAG that uses Python [random.choice](https://docs.python.org/3/library/random.html#random.choice) function to decide which type of dummy transform it will execute.

`code/dags/5_branching_dag.py`
```python
{{#include ../../../code/dags/5_branching_dag.py}}
```

![branching dag](airflow-branching-dag.png)

From the historical runs, we can see that different transform tasks were run.

![branching dag runs](airflow-branching-dag-results.png)

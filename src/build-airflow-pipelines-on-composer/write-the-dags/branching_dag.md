# Branching DAG

When designing data pipelines, there may be use cases that require more complex task flows than _Task A > Task B > Task C_. For example, let's say that there is a use case where different tasks need to be chosen to execute based on the results of an upstream task. We call this `branching` in Airflow, and it uses a particular Operator `BranchPythonOperator` to handle this use case.

The `BranchPythonOperator` takes a Python function as an input. The function must return a list of task IDs for the DAG to process using the function.

To give you an example of branching, let's create a DAG that uses Python [random.choice](https://docs.python.org/3/library/random.html#random.choice) function to decide which type of no-op transform it will execute.

Create a file named `5_branching_dag.py` that contains the following code:

```python
{{#include ../../../code/dags/5_branching_dag.py}}
```

![Branching dag](airflow-branching-dag.png)

From the historical runs, we can see that different transform tasks were run.

![Branching dag runs](airflow-branching-dag-results.png)

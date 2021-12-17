# PythonOperator and TaskFlow Dag

Tasks that use `PythonOperator` executes Python callables/functions. You can pass parameters to the function via the op_kwargs parameter.

Airflow 2.0 adds a new style of authoring dags called the [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/2.0.0/concepts.html#taskflow-api) which removes a lot of the boilerplate around creating `PythonOperator`, managing dependencies between task and accessing XCom values.

Let's create a DAG that uses both `PythonOperator` and TaskFlow API to show how to create tasks using Python functions.

In the below DAG, the first task uses `PythonOperator` to print the task context including the parameter(`my_keyword`) that is passed in. The second task and third tasks are created using TaskFlow decorator. These tasks run Python functions without using  `PythonOperator`.


`code/dags/7_python_operator_and_taskflow_dag.py`
```python
{{#include ../../code/dags/7_python_operator_and_taskflow_dag.py}}
```

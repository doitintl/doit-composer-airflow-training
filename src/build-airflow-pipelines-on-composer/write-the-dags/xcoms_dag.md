# Xcoms DAG

Sharing data between Tasks is a common use case in Airflow. For example, a Task calls an API to get the data filenames for today's data ingestion DAG. The following Tasks need to know these filenames to load the data.

XCom (short for cross-communication) is a native feature within Airflow. XComs allow tasks to exchange Task metadata or small amounts of data. XComs can be "pushed" (sent) or "pulled" (retrieved). When a task pushes an XCom, it makes it generally available to other tasks.

There are two ways to push a value to XCom.

1. Use `xcom_pull`
2. Return the value in your function, and it will be pushed to Xcom automatically.

When a Task (An instance of an Operator) is running, it will get a copy of the Task Instance passed to it. When `python_callable` is used inside a `PythonOperator` Task, you can get the task instance object via `ti = kwargs['ti']`. After that, we can call the `xcom_pull` function to retrieve the Xcom value.

Let's create a DAG to exchange value between tasks.

Create a file named `6_xcoms_dag.py` that contains the following code:

```python
{{#include ../../../code/dags/6_xcoms_dag.py}}
```

![Xcoms dag](airflow-xcoms-dag.png)

From Airflow UI, there is a tab next to `Log` called XCom that shows XCom values.

![Xcoms push](airflow-xcoms-push.png)

Let's check the `pull_task`. Yes, the value was retrieved.

![Xcoms pull](airflow-xcoms-pull.png)

XCom values are stored in Airflow database and are shown on UI or logs. It is important not to store sensitive information and large data in them.

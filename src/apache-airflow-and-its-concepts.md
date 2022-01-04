# Apache Airflow and its concepts

## What is Airflow

Airflow is a platform to programmatically create, schedule, and monitor workflows.

You can use Airflow to create workflows as [Directed Acyclic Graphs](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAGs) of tasks. The Airflow scheduler executes your tasks on various workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed.

## Quick peek

![Airflow](https://airflow.apache.org/docs/apache-airflow/stable/_images/airflow.gif)

## Why Airflow is popular

- Workflows are defined as Python code, so they 
  - are more flexible
  - are testable
  - easy to reuse
  - can access the whole Python echo system
- Battery included platform
  - It provides libraries to connect
    - Popular database: MySQL, Postgres, MongoDB, Oracle, SQL Server, Snowflake, BigQuery
    - Services: Databricks, Datadog, ElasticSearch, Jenkins, Salesforce, SendGrid, Slack, Zendesk
- It can be deployed to public cloud platforms: AWS, GCP, Azure, etc
- Informational and feature-rich UI to visualize workflows' status, monitor progress, troubleshoot issues, trigger, and re-trigger workflows and tasks in them

## Beyond the Horizon

Airflow is **NOT** a data streaming solution. Workflows are expected to be mostly static or slowly changing. Below are a few example use cases of it:

- Daily - load batch files from different databases to a reporting database
- Daily/Weekly/Monthly - generate and deliver reports to stakeholders
- Daily -  re-train machine learning models with fresh data
- Hourly - back up data from a database
- Hourly - generate and send recommended products to customers based on customers activities - think spam emails you get from eBay
- On-demand(triggered) - send registration emails to newly registered customers

## Airflow concepts

- **DAG**: DAGs are collections of tasks and describe how to run a workflow written in Python. Pipelines are designed as a directed acyclic graph by dividing a pipeline into tasks that can be executed independently. Then these tasks are combined logically as a graph.
- **Task**: A Task defines a unit of work within a DAG; it is represented as a node in the DAG graph. Each task is an implementation of an Operator, for example, a PythonOperator to execute some Python code or a BashOperator to run a Bash command. After an operator is instantiated, it's referred to as a "task".
- **Task instance**: A task instance represents a specific run of a task characterized by a DAG, a task, and a point in time.
- **Operators**: Operators are atomic components in a DAG describing a single task in the pipeline. They determine what gets done in that task when a DAG runs. Airflow provides operators for common tasks. It is extensible so that you can define your own custom operators.
- **Sensor**: Sensors are special operators that repeatedly run until the predefined condition is fulfilled. For example a file sensor can wait until the file lands, then continue the workflow
- **Hooks**: Provide a uniform interface to access external services like GCS, BigQuery, PubSub, etc. Hooks are the building blocks for Operators/Sensors to interact with external services.
- **DAG run**: when a DAG is triggered, it is called a DAG run. It represents the instance of the workflow
- **Scheduler**: Airflow scheduler monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete
- **Executor**: Airflow Executors are the mechanism by which task instances get to run. The most popular Executor is Celery Executor

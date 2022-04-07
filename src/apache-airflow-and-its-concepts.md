# Apache Airflow and its concepts

## What is Airflow

Airflow is a platform to programmatically create, schedule, and monitor workflows.

You can use Airflow to create workflows as [Directed Acyclic Graphs](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAGs) of tasks. The Airflow scheduler executes your tasks on various workers while following the specified dependencies. Rich command-line utilities make performing complex surgeries on DAGs a snap. The rich user interface helps to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed.

## Quick peek

![Airflow](https://airflow.apache.org/docs/apache-airflow/stable/_images/airflow.gif)

## Why Airflow is popular

- You can define workflows as Python code, so that they:
  - Are more flexible
  - Are testable
  - Are reusable
  - Can access the whole Python echo system
- Battery included platform
  - Airflow provides libraries to connect
    - Popular database: MySQL, Postgres, MongoDB, Oracle, SQL Server, Snowflake and BigQuery
    - Services: Databricks, Datadog, ElasticSearch, Jenkins, Salesforce, SendGrid, Slack and Zendesk
- You can deploy Airflow to public cloud platforms: _Amazon Web Services_ (AWS), Azure, and _Google Cloud Platform_ (GCP)
- Informational and feature-rich UI to visualize workflows' status, monitor progress, troubleshoot issues, trigger, and re-trigger workflows and tasks in them

## Beyond the Horizon

Airflow is _not_ a data streaming solution. Workflows are expected to be mostly static or slowly changing. Below are a few example use cases of it:

- `Daily`&mdash;Load batch files from different databases to a reporting database
- `Daily/Weekly/Monthly`&mdash;Generate and deliver reports to stakeholders
- `Daily`&mdash;Re-train machine learning models with fresh data
- `Hourly`&mdash;Back up data from a database
- `Hourly`&mdash;Generate and send recommended products to customers based on customers activities - think spam emails you get from eBay
- `On-demand (triggered)`&mdash;Send registration emails to newly registered customers

## Airflow concepts

- `DAG`&mdash;A DAG is a collection of tasks and describe how to run a workflow written in Python. A pipeline is designed as a directed acyclic graph, in which the tasks can be executed independently. Then these tasks are combined logically as a graph.
- `Task`&mdash;A Task defines a unit of work within a DAG; it is represented as a <!-- textlint-disable terminology -->node<!-- textlint-enable --> in the DAG graph. Each task is an implementation of an Operator, for example, a PythonOperator to execute some Python code or a BashOperator to run a Bash command. After an operator is instantiated, it's called a _task_.
- `Task instance`&mdash;A task instance represents a specific run of a task characterized by a DAG, a task, and a point (execution_date).
- `Operators`&mdash;Operators are atomic components in a DAG describing a single task in the pipeline. They determine what gets done in that task when a DAG runs. Airflow provides operators for common tasks. It is extendable so that you can define your own custom operators.
- `Sensors`&mdash;Sensors are special operators that repeatedly run until the predefined condition is fulfilled. For example a file sensor can wait until the file lands, then continue the workflow
- `Hooks`&mdash;Provide a uniform interface to access external services like _Google Cloud Storage_ (GCS), BigQuery, PubSub, etc. Hooks are the building blocks for Operators/Sensors to interact with external services.
- `DAG run`&mdash;when a DAG is triggered, it is called a DAG run. It represents the instance of the workflow
- `Scheduler`&mdash;Airflow scheduler monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete
- `Executor`&mdash;Airflow Executors are the mechanism by which task instances get to run. The most popular Executor is Celery Executor

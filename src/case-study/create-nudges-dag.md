# Create nudges DAG

When designing a DAG, we often start with critical tasks such as loading the data, transformation, exporting the data, etc. Then iteratively, we add other tasks such as checking if the BigQuery Dataset exists or not, if today's load has happened, etc.

## Key tasks

To generate the nudges for the customers, we can load the daily exported CSV files to three tables in BigQuery. After that, we can run a SQL query that joins the three tables, create the nudge information, and store the results in another table.
The DAG looks like this:

![A diagram of the case study DAG](case-study-dag-1.png)

As the CSV files are on _Google Cloud Storage_ (GCS) and we need to load them to BigQuery, we need an Operator that can do GCS to BigQuery. GCS to BigQuery is a pretty generic job, let's search in [Astronomer Registry](https://registry.astronomer.io/) to see if Airflow has it in the built-in libraries:

![Screenshot showing the search UI](GCS-to-BQ-search.png)

Yes, we found the `GCSToBigQueryOperator`. Following it's [documentation](https://registry.astronomer.io/providers/google/modules/gcstobigqueryoperator/#example-dags), let's create our three data load tasks:

Create a file named `9_generate_nudges_dag.py` that contains the following code:

```python
{{#include ../../code/dags/9_generate_nudges_dag.py:68:111}}
```

The `generate_nudges` task runs a BigQuery query and saves the results in a BigQuery table. It may look like an ordinary job. But unfortunately, there isn't an existing Operator that does the job. We need to create a custom Operator. In this custom Operator, we can use the built-in `BigQueryHook` to interact with BigQuery. We can find its source code on [GitHub](https://github.com/apache/airflow/blob/main/airflow/providers/google/cloud/hooks/bigquery.py#L66).

Let's call the custom Operator `GenerateNudgesOperator`

Create a file named `generate_nudges_operator.py` that contains the following code:

```python
{{#include ../../code/plugins/operators/generate_nudges_operator.py}}
```

And the task looks like this:

```python
{{#include ../../code/dags/9_generate_nudges_dag.py:107:111}}
```

## Add other tasks

### Check BigQuery Dataset

As a safety measure, we should add a task to check if the BigQuery Dataset exists before loading the CSV files.

After checking the Airflow built-in Operators, there isn't a built-in one. Let's create another custom Operator called `CheckBigQueryDatasetOperator`. Because it needs to access BigQuery, we can use the `BigQueryHook` again.

Create a file named `check_bigquery_dataset_operator.py` that contains the following code:

```python
{{#include ../../code/plugins/operators/check_bigquery_dataset_operator.py}}
```

And the task looks like this:

```python
{{#include ../../code/dags/9_generate_nudges_dag.py:63:66}}
```

Now the DAG looks like this:

![A diagram of the changed DAG](case-study-dag-2.png)

### Avoid duplicated runs

It is always a good idea to check if today's run finishes. There are multiple ways to do that. If there are numerous data pipelines, you should build an API to record their runs. When a pipeline is kicked off, it checks if the run for that day has been finished by calling the API. If yes, this particular DAG run should not continue with the following tasks.

In our case study, as we only have one data pipeline, we can assume that:

- The email system sends the emails out every day
- The data pipeline uploads a file to GCS (using the current date as the filename)

With this assumption, a few tasks can be added to finalize the DAG.

![A diagram of the final DAG](case-study-dag-3.png)

Let's dig into the new tasks.

#### Get latest run date

As mentioned above, we can check if a file named as current date exists in the GCS bucket. To do this, we can use the `GCSListObjectsOperator` from Airflow built-in libraries. The task looks like this:

```python
{{#include ../../code/dags/9_generate_nudges_dag.py:50:54}}
```

From the [code](https://github.com/apache/airflow/blob/main/airflow/providers/google/cloud/operators/gcs.py#L279) on Github, it returns the URI of the file on GCS or empty array(if the file does not exist). In Airflow Operator, any value that is returned by `execute` function is stored in `xcom`.

Now we have a value in `xcom`, let's move on to the next task.

#### Check run date

In this task, we can use `BranchPythonOperator` to decide if this particular run should continue. The task looks like this:

```python
{{#include ../../code/dags/9_generate_nudges_dag.py:56:58}}
```

And the `branch_func`:

```python
{{#include ../../code/dags/9_generate_nudges_dag.py:29:37}}
```

From here, Airflow will decide if the DAG run should continue loading data or finish. To make the pipeline more user-friendly, we can use two `DummyOperator` to represent `kick_off_run` and `finish_run` tasks.

```python
{{#include ../../code/dags/9_generate_nudges_dag.py:60:61}}
```

## Summary

In this chapter, we've walked through designing and creating a DAG to load data from three CSV files and generate nudges in BigQuery. If you'd like to run it, you can run it yourself, be sure to replace the project ID and buckets in the DAG file.

```python
{{#include ../../code/dags/9_generate_nudges_dag.py:18:20}}
```

Or you can wait until the next chapter, in which I will cover the testing strategy, including a quick end-to-end test that can generate test files and trigger the DAG.

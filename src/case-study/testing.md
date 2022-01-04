# Testing

Just like any software program, Airflow pipelines need to be tested. In Airflow, we usually do unit tests and end-to-end tests to ensure Airflow pipelines work well before deployments.

In our project, [Pytest](https://docs.pytest.org/) is used as the test runner.

## Unit tests
When testing Airflow, the very first thing we'd like to do is to use the below test to make sure all the DAGs to be deployed don't have errors themselves. These include syntax errors, library import errors, etc.
```python
{{#include ../../code/tests/test_dags.py}}
```

If there are custom Operators, Hooks, and Sensors, they also need to be unit tested.
For example, with the `BigQueryHook` being mocked, the `CheckBigQueryDatasetOperator` can be tested like as the below:
```python
{{#include ../../code/tests/test_check_bigquery_dataset_operator.py}}
```

## End-to-end tests
With the unit tests ensuring DAGs and custom plugins are reasonable, we also need some kind of end-to-end tests to ensure the pipeline runs well.

Like any other end-to-end test, we generate some input, run the program, and check the output. To test our DAG, the test steps look like the below:

1. create and upload three CSV files to GCS
2. trigger Airflow DAG
3. wait for 30 seconds for the DAG to finish
4. check the nudge table is refreshed

Ideally, this test should be running in a test environment where there is a test Composer environment. Then we can trigger the DAG using Airflow REST API by following the Google document [here](https://cloud.google.com/composer/docs/access-airflow-api).

I understand that there may be expensive to host a test Composer because it needs to run 24/7. Therefore I recommend running Airflow locally(I will cover this in the next chapter) with `docker-compose` and using the below code to trigger the DAG:
```python
{{#include ../../code/e2e_tests/test_nudges.py:104:108}}
```

Now we have the tests ready, let's move on to the next topic - CI and CD.

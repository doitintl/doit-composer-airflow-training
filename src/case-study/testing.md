# Testing

Like any software, Airflow pipelines need to be tested. In Airflow, we usually do unit tests and end-to-end tests to ensure Airflow pipelines work well before deployments.

In our project, [Pytest](https://docs.pytest.org/) is used as the test runner.

## Unit tests

When testing Airflow, the first thing we'd like to do is to use the below test to make sure all the DAGs to be deployed don't have errors themselves. These include syntax errors, library import errors, etc.

```python
{{#include ../../code/tests/test_dags.py}}
```

If there are custom Operators, Hooks, and Sensors, they also need to be unit tested.

For example, with the `BigQueryHook` being mocked, the `CheckBigQueryDatasetOperator` can be tested like as the below:

```python
{{#include ../../code/tests/test_check_bigquery_dataset_operator.py}}
```

## End-to-end tests

With the unit tests ensuring DAGs and custom plugins are reasonable, we also need some end-to-end tests to ensure the pipeline runs well.

Like any other end-to-end tests, we generate some input, run the program, and check the output. To test our DAG, the test steps look like the below:

1. Create and upload three CSV files to _Google Cloud Storage_ (GCS)
2. Trigger Airflow DAG
3. Wait for 30 seconds for the DAG to finish
4. Check the nudge table is refreshed

Ideally, this test should be running in a test environment with a test Composer environment. Then we can trigger the DAG using the Airflow [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) API by following the Google document [here](https://cloud.google.com/composer/docs/access-airflow-api).

I understand that there may be expensive to host a test Composer because it needs to run 24/7. To save the cost, you can run Airflow locally (I will cover more details of this approach in the another chapter) with `docker-compose` and using the below code to trigger the DAG:

```python
{{#include ../../code/e2e_tests/test_nudges.py:104:108}}
```

Now we have the tests ready, let's move on to the next topic - CI and CD.

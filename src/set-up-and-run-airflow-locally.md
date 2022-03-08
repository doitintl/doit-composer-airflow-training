# Set up and run Airflow locally

There are a few ways to run Airflow locally:

1. run it in a Python virtual environment
2. run it using `docker-compose`
3. deploy it using Helm Chart

## Python virtual environment deployment

Airflow community created a [guide](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html). You basically create a SQLite database and run Airflow webserver and worker in two processes.

This setup is lightweight and suitable to test something quickly. It is not a production-ready setup because it only processes tasks sequentially.

## Docker-compose

Using `docker-compose` is the preferred way to run Airflow locally. Again, the Airflow community is kindly created a [guide](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) including a pre-baked `docker-compose.yaml` file!

When you do `docker-compose up`, a whole Airflow cluster is up, including:

- **airflow-scheduler** - The scheduler monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
- **airflow-webserver** - The webserver is available at [http://localhost:8080](http://localhost:8080]).
- **airflow-worker** - The worker that executes the tasks given by the scheduler.
- **airflow-init** - The initialization service.
- **flower** - The flower app for monitoring the environment. It is available at [http://localhost:5555](http://localhost:5555).
- **postgres** - The database.
- **redis** - The redis - broker that forwards messages from scheduler to worker.

All these services allow you to run Airflow with `CeleryExecutor`.

There is only one trick/bug that you should be aware of - Docker has this weird of creating volumes with root user. When running Airflow with `docker-compose`, there is a [GitHub issue](https://github.com/helm/charts/issues/23589) that includes a temp solution.
If you see errors after running `docker-comose up`: `Errno 13 - Permission denied: '/opt/airflow/logs/scheduler`, you need to stop the `docker-compose` and run `chmod -R 777 logs/`. You should be able to start your Airflow cluster again using `docker-comose up`.

## Helm Chart

How can we forget Kubernetes these days if we want to deploy something! If you would like to deploy Airflow to Kubernetes. [Here](https://airflow.apache.org/docs/helm-chart/stable/index.html) is a guide from the Airflow community.

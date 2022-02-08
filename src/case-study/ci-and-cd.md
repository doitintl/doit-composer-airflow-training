# CI and CD

At this point, we have the DAG and plugins ready and tested. What's next? Of course, you can upload them manually to Composer and have a working environment. However, in a proper Airflow project, we should have CI (continuous integration) and CD (continuous deployment) so that the development and operation activities can be smoother.

## CI
Typical CI tasks in Airflow pipelines include:
- **lint**: it highlights syntactical and stylistic problems in the Airflow pipeline Python code, which often helps you identify and correct subtle programming errors or unconventional coding practices that can lead to errors.
- **unit tests**: it runs the unit tests to ensure DAGs and plugins are working as expected.
- **end-to-end tests**: it makes sure the DAG works with all other integrated systems.

## CD
In the CD tasks, DAGs and plugins are uploaded to Composer. There may be another task to send Slack or email notifications.

There are multiple ways to upload DAGs to Composer. Google created a [guide](https://cloud.google.com/composer/docs/how-to/using/managing-dags) that shows different ways. However, I prefer to work with the Cloud Storage bucket directly using `gsutil rsync` to sync the DAG folder in my repo to the DAG folder on GCS. In this way, I don't need to think about if any DAG file should be deleted or not. The DAGs on Cloud Storage match what are in the repo.
```bash
gsutil rsync dags gs://my-composer-bucket/dags
```

Similarly, to upload the plugin files, I use `gsutil rsync` to sync them to the plugins folder on GCS.
```bash
gsutil rsync plugins gs://my-composer-bucket/plugins
```

Cool! We've covered all the information in this case study. Remember that I told you there is a way to run Airflow locally? Let's do it in the next chapter!

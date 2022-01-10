# Version support and deprecation

## Versions
Currently, there are two versions of Cloud Composer, versions 1 and 2(current in preview).

You can find the full list of Composer versions from [here](https://cloud.google.com/composer/docs/concepts/versioning/composer-versions). A typical version looks like this:

> composer-1.17.5-airflow-2.1.4

In the version identifier, `1.17.5` is the version of Composer, while `2.1.4` is the version of Airflow.

You can consider each `Composer` version contains all the close-sourced Google deployments and hosting code and each `Airflow` version contains the open-sourced code from Apache Airflow code that is hosted on Github [repository](https://github.com/apache/airflow).

## Support and deprecation

### Composer
Google supports Cloud Composer versions for a period of time after the version is released. 

Cloud Composer version support is defined as follows:

- 0-12 months from the release date: Cloud Composer environments running these versions are fully supported.
- 12-18 months from the release date: Cloud Composer environments running these versions are unsupported except to notify customers about security issues.
- 18+ months from the release date: Cloud Composer environments running these versions are unsupported and entirely user-managed.

### Airflow
A particular version of Apache Airflow found in Cloud Composer is **NOT** always an exact match of the corresponding version in upstream Airflow because Cloud Composer uses a patched version of Airflow.
[This repository](https://github.com/GoogleCloudPlatform/composer-airflow/tree/2.0.2) holds the code for every patched version of Airflow used in Composer, and it is useful to 
- find out if a specific commit from [Airflow open-source project](https://github.com/apache/airflow) is in the version of Composer
- reproduce issues locally
- check how an Operator/Sensor/Hook looks like in the version of Composer

In practice, to troubleshoot an Airflow issue from Cloud Composer, you may look into the above repo.

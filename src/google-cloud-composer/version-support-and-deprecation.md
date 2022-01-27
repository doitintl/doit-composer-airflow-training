# Version support and deprecation

## Versions
Currently, there are two versions of Cloud Composer: The GA version 1 and In-preview version 2.

You can find the full list of Composer versions [here](https://cloud.google.com/composer/docs/concepts/versioning/composer-versions). A typical version looks like this:

> composer-1.17.5-airflow-2.1.4

In the version identifier, `1.17.5` is the version of Composer, while `2.1.4` is the version of Airflow.

You can consider each `Composer` version contains all the close-sourced Google deployments and hosting code and each `Airflow` version contains the open-sourced code from Apache Airflow code that is hosted on Github [repository](https://github.com/apache/airflow).

## Understanding Composer vs. Airflow Versions

While there are two versions of Cloud Composer and two versions of Apache Airflow, each version of Composer *does not* directly map to a version of Airflow.

**Composer v1 has support for both Airflow v1 and v2, while Composer v2 only supports Airflow v2.**

As mentioned in Section 3.2, the primary difference between Composer 1 and 2 are in how Composer 2 has moved the web server from App Engine to GKE, thereby enabling Composer 2 to take advantage of GKE Autopilot for autoscaling. Composer 1, by contrast, does not support an autoscaling environment.

Airflow v1 vs. v2 is more about additional/improved functionality detailed at length [here](https://airflow.apache.org/blog/airflow-two-point-oh-is-here/). The most anticipated new features in Airflow include: Easier to author DAGs, 'massive' scheduler performance improvements, high-availability support for the job scheduler, and an improved UI.

## Support and deprecation

### Composer
Google supports Cloud Composer versions for a period of time after the version is released.

Cloud Composer version support is defined as follows:

- 0-12 months from the release date: Cloud Composer environments running these versions are fully supported.
- 12-18 months from the release date: Cloud Composer environments running these versions are unsupported except to notify customers about security issues.
- 18+ months from the release date: Cloud Composer environments running these versions are unsupported and entirely user-managed.

### Airflow
A particular version of Apache Airflow found in Cloud Composer is **NOT** always an exact match of the corresponding version in upstream Airflow because Cloud Composer uses a patched version of Airflow.
[This repository](https://github.com/GoogleCloudPlatform/composer-airflow/tree/2.0.2) contains the code for every patched version of Airflow used in Composer, and it is useful for:
- Finding out if a specific commit from the [Airflow open-source project](https://github.com/apache/airflow) is in the Composer version
- Reproducing issues locally
- Check how an Operator/Sensor/Hook looks like in the Composer version

When deep-dive troubleshooting an Airflow issue from Cloud Composer, you may want to look into Google's official composer-airflow repo.

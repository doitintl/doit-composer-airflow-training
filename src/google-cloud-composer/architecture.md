# Cloud Composer Architecture

In this section, we will talk about the architecture of Cloud Composer.

## Composer components

A Cloud Composer environment contains multiple components, below are some of the important ones:

- Airflow Webserver
  - It is a visual management interface powered by [Flask-AppBuilder](https://flask-appbuilder.readthedocs.io/)
  - It provides the ability to
    - view status of DAGs and their status
    - display logs from each DAG and worker
    - act on the DAG status (pause, unpause, trigger)
    - configure Airflow, such as variables, connections, etc
    - each view the code of DAGs
- Airflow scheduler
  - It monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete
  - Behind the scenes, the scheduler spins up a subprocess, which monitors and stays in sync with all DAGs in the specified DAG directory. Once per minute, by default, the scheduler collects DAG parsing results and checks whether any active task can be triggered
- Airflow worker
  - It executes individual tasks from DAGs by taking them from the Redis queue.
- Airflow database hosted on CloudSQL
  - It stores all the information of Airflow, including DAGs, task information, configs, etc
- Airflow buckets
  - When you create an environment, Cloud Composer creates a Cloud Storage bucket and associates the bucket with your Composer environment.
  - You can store custom code in the Cloud Storage bucket, including DAGs, plugins, and other resources.
  - Behind the scene, Composer uses [gcsfuse](https://github.com/GoogleCloudPlatform/gcsfuse) to sync all the content to Airflow workers and webserver.
  - You can find a Google [document](https://cloud.google.com/composer/docs/concepts/cloud-storage#folders_in_the_bucket) that shows the mapping list between the folders in the bucket to Airflow folders.
- Redis queue
  - It holds a queue of individual tasks from your DAGs. Airflow schedulers fill the queue; Airflow workers take their tasks from it

## Customer and tenant projects

Cloud Composer runs on both customer and tenant(Google-managed) projects; Composer distributes the environment's resources between a tenant and a customer project. The resources are deployed to different projects because of varying environment setups.
However, regardless of which environment setup and old and new Composer versions, there is a GKE cluster in the customer project that runs the Airflow workloads, a CloudSQL on tenant project, and a Cloud Storage bucket to store DAGs and plugins.

## Different Composer setups

Below are the different setups of Composer 1 and 2

### Composer 1

[Public IP](https://cloud.google.com/composer/docs/concepts/architecture#public-ip)
![Public IP](https://cloud.google.com/composer/docs/images/composer-1-public-ip-architecture.svg)

[Private IP](https://cloud.google.com/composer/docs/concepts/architecture#private-ip)
![Private IP](https://cloud.google.com/composer/docs/images/composer-1-private-ip-architecture.svg)

[Private IP with DRS](https://cloud.google.com/composer/docs/concepts/architecture#private-ip-drs)
If the [Domain Restricted Sharing (DRS) organizational policy](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints) is turned on in the project, then Cloud Composer uses the Private IP with DRS environment architecture.
![Private IP with DRS](https://cloud.google.com/composer/docs/images/composer-1-private-ip-drs-architecture.svg)

### Composer 2

[Public IP](https://cloud.google.com/composer/docs/composer-2/environment-architecture#public-ip)
![Public IP](https://cloud.google.com/composer/docs/images/composer-2-public-ip-architecture.svg)

[Private IP](https://cloud.google.com/composer/docs/composer-2/environment-architecture#private-ip)
![Private IP](https://cloud.google.com/composer/docs/images/composer-2-private-ip-architecture.svg)

### Comparison of Composer 1 and 2

Composer 2 is the future version of Composer. Most of the users are still using Composer 1 because Composer 2 is still in preview. We can expect Composer 1 to be retired soon, and Composer 2 will be the only supported one.
As you can see from the above architecture diagrams, there are a few things that are some differences between these two versions:

1. The significant improvement of Composer 2 is **autoscaling**; it leverages [GKE Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview) feature, meaning the Composer environment can be automatically scaled up to handle more workloads and scale down to reduce cost.
2. Composer 2 only supports Airflow 2 and Python 3.8+. Suppose there is a requirement of using Python 2(please don't!) and Airflow 1.10.*, Composer 1 is the only option.
3. In Composer 2, the Airflow Webserver is moved to GKE from App Engine running on the tenant project.

You can find more details of the differences between the two Composer versions from [here](https://cloud.google.com/composer/docs/composer-2/composer-versioning-overview#major-versions).

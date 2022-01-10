# Limitations

### Limited access to underline systems

Being a hosted service, Google manages all the infrastructure. As a customer, you don't have access to the underline systems and the database. Most of the time, it is excellent and worry-free.
However, it can be a pain when you bump into any issue that requires more deep investigations.

### Painful upgrade process

Each Composer version has one year of Google support. After that, it is recommended to upgrade to a newer supported version.
To upgrade the Composer version, Google provides a beta [feature](https://cloud.google.com/composer/docs/how-to/managing/upgrading). However, it only works if the old Composer version is not that old. Some Cloud Composer users are using out-of-support versions - some environments are more than two years old. The managed upgrading process that Google provides would most likely fail.
In this scenario, it is recommended that the customer creates a new Composer environment and migrate all the existing workflows to it.

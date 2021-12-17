# Limitations

### Limited access to underline systems

Being a hosted service, Google manages all the infrastructure. The customers don't need to access the underline systems and the database. Most of the time, it is good and worry-free.
However, when there are issues that require more deep investigations, it can be a pain.
There are some useful tips can command that will be shown in the later chapters.

### Painful upgrade process

Each Composer version has one year of Google support. After that, it is recommended to upgrade to the newer supported version.
Google provides a beta [feature](https://cloud.google.com/composer/docs/how-to/managing/upgrading) to upgrade the Composer version. However, it only works if the old Composer version is not that old. A lot of users are using out-of-support versions. Some Composers are more than two years. The managed upgrading process that Google provides would most likely fail.
In this case, it is recommended that the customer creates a new Composer environment and migrate all the existing workflows to it.
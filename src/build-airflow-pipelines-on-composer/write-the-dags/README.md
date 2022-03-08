# Write the DAGs

In this chapter, we will learn how to write the DAGs. We will use some of the fundamental Airflow concepts we learned to create these pipelines.

## Basics of writing a DAG

Airflow uses Python to define DAGs. A DAG file is nothing but a standard Python file.

To define a DAG, typically, there are five steps:

1. Import Python modules
2. Define default args
   - These args will get passed on to each Operator/Sensor
   - Args can be overridden on a per-task basis during Operator/Sensor initialization
3. Instantiate DAG / Create a DAG object
4. Define tasks
   - A task can be an instance of an Operator or a Sensor
5. Define task sequence and dependencies

Let's go ahead and write our first DAG!

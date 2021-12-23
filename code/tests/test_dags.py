from airflow.models import DagBag


def test_dag_loaded():
    dag_bag = DagBag(include_examples=False)
    assert dag_bag.import_errors == {}

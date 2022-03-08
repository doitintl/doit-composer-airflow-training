from airflow.models import BaseOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.utils.decorators import apply_defaults


class BigQueryGetResultsOperator(BaseOperator):

    template_fields = ['query']
    @apply_defaults
    def __init__(self, query, *args, **kwargs):
        self.query = query
        super(BigQueryGetResultsOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        bq = BigQueryHook(
            use_legacy_sql=False
        )
        conn = bq.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.query)
        query_results = cursor.fetchall()

        # Because query_results is a list of list, need to convert it is a list
        # Example: [[3.0], [1.0]] -> [3.0, 1.0]
        results = []
        for item in query_results:
            results.append(item[0])

        # return results will put the results into xcom as return value
        return results

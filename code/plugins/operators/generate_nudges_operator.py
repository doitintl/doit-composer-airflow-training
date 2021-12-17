from airflow.models import BaseOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.utils.decorators import apply_defaults


class GenerateNudgesOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        *,
        nudges_query: str,
        destination_dataset_table: str,
        gcp_conn_id: str = "google_cloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.gcp_conn_id = gcp_conn_id
        self.nudges_query = nudges_query
        self.destination_dataset_table = destination_dataset_table

    def execute(self, context):
        self.log.info(
            f"Generating nudges with query {self.nudges_query} and write into {self.destination_dataset_table}..."
        )

        hook = BigQueryHook(gcp_conn_id=self.gcp_conn_id, use_legacy_sql=False)

        hook.run_query(
            sql=self.nudges_query,
            destination_dataset_table=self.destination_dataset_table,
            write_disposition="WRITE_TRUNCATE",
        )

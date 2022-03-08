from airflow.models import BaseOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.utils.decorators import apply_defaults


class CheckBigQueryDatasetOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        *,
        dataset_id,
        gcp_conn_id="google_cloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.gcp_conn_id = gcp_conn_id
        self.dataset_id = dataset_id

    def execute(self, context):
        self.log.info(f"Checking dataset {self.dataset_id}...")

        hook = BigQueryHook(
            gcp_conn_id=self.gcp_conn_id,
        )

        # Check dataset exists
        datasets_list = hook.get_datasets_list()
        self.log.info(f"datasets_list: {datasets_list}")
        is_dataset_existed = False
        if datasets_list:
            datasets_id_list = [dataset.dataset_id for dataset in datasets_list]
            is_dataset_existed = self.dataset_id in datasets_id_list

        if is_dataset_existed:
            return True
        else:
            raise Exception(f"Dataset id {self.dataset_id} not found")

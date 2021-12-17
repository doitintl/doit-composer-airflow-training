from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class HelloOperator(BaseOperator):
    @apply_defaults
    def __init__(self, operator_param, *args, **kwargs):
        self.operator_param = operator_param
        super(HelloOperator, self).__init__(*args, **kwargs)
    
    def execute(self, context):
        greeting = f"Hello, {self.operator_param}!"
        self.log.info(greeting)
        return greeting
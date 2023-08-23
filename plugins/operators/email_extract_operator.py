from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import requests

class EmailExtractOperator(BaseOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        response = requests.get("https://jsonplaceholder.typicode.com/comments")
        comments = response.json()

        filtered_comments = [comment for comment in comments if comment['email'].endswith('us')]

        self.log.info("Extracted %d comments with emails ending with 'us'", len(filtered_comments))


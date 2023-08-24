from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import requests
import psycopg2

class EmailExtractOperator(BaseOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        response = requests.get("https://jsonplaceholder.typicode.com/comments")
        comments = response.json()

        filtered_comments = [comment for comment in comments if comment['email'].endswith('us')]

        self.log.info("Extracted %d comments with emails ending with 'us'", len(filtered_comments))

        connection = psycopg2.connect(
            host="postgres.cxubmpofrvqu.us-east-1.rds.amazonaws.com",
            port="5432",
            user="postgres",
            password="postgres",
            dbname="postgres"
        )

        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS extracted_emails (
                id SERIAL PRIMARY KEY,
                email TEXT NOT NULL,
                comment TEXT
            )
        """)

        for comment in filtered_comments:
            cursor.execute(
                "INSERT INTO extracted_emails (email, comment) VALUES (%s, %s)",
                (comment['email'], comment['body'])
            )

        connection.commit()
        cursor.close()
        connection.close()

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from operators.email_extract_operator import EmailExtractOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'extract_email_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

start_task = DummyOperator(task_id='start', dag=dag)

extract_task = PythonOperator(
    task_id='extract_emails',
    python_callable=EmailExtractOperator().execute,
    dag=dag,
)

start_task >> extract_task

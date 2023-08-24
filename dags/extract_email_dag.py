import os
import sys
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

current_dir = os.path.abspath(os.path.dirname(__file__))
plugins_folder = os.path.join(current_dir, '..', 'plugins')
sys.path.append(plugins_folder)

from plugins.operators.email_extract_operator import EmailExtractOperator


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
    schedule=timedelta(days=1),
)

start_task = EmptyOperator(task_id='start', dag=dag)

extract_task = EmailExtractOperator(
    task_id='extract_emails',
    dag=dag
)

start_task >> extract_task

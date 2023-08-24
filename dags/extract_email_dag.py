import os
import sys

# Печатаем текущие пути поиска перед всеми другими операциями
print("Current sys.path:", sys.path)

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# Получить абсолютный путь к текущей директории
current_dir = os.path.abspath(os.path.dirname(__file__))

# Сформировать путь к папке plugins (на уровень выше текущей директории)
plugins_folder = os.path.join(current_dir, '..', 'plugins')

# Добавить этот путь в список sys.path
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

extract_task = PythonOperator(
    task_id='extract_emails',
    dag=dag
)

start_task >> extract_task

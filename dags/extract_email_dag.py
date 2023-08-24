import os
import sys
from airflow import DAG
from airflow.operators.empty import EmptyOperator  # Импорт EmptyOperator
from datetime import datetime, timedelta

# Получить абсолютный путь к текущей директории
current_dir = os.path.abspath(os.path.dirname(__file__))

# Сформировать путь к папке plugins (на уровень выше текущей директории)
plugins_folder = os.path.join(current_dir, '..', 'plugins')

# Добавить этот путь в список sys.path
sys.path.append(plugins_folder)

# Теперь импортируйте ваш оператор и другие модули после добавления пути к sys.path
from airflow.operators.python import PythonOperator
from plugins.operators.email_extract_operator import EmailExtractOperator

# Печатаем текущие пути поиска
print(sys.path)

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
    python_callable=EmailExtractOperator().execute,  # Обратите внимание на добавление .execute
    dag=dag,
)

start_task >> extract_task

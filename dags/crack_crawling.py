from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# 프로젝트 경로 추가
sys.path.append('/opt/airflow/dags')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'crack_crawling',
    default_args=default_args,
    schedule=None,
    catchup=False
)

def run_crawling():
    from src.crack.main import main
    main()
    return "Crawling Operation Completed !"

crawling_task = PythonOperator(
    task_id='run_crawling',
    python_callable=run_crawling,
    dag=dag
)

def test_function():
    print("Hello from Airflow!")
    return "Success"

test_task = PythonOperator(
    task_id='test_task',
    python_callable=test_function,
    dag=dag
)
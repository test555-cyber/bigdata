from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "data_team",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

def calculate_daily_index(**context):
    """延迟导入避免循环依赖"""
    from jobs.daily_index import DailyIndexJob
    execution_date = context["execution_date"]
    job = DailyIndexJob()
    processed = job.run(execution_date)
    print(f"Processed {processed} categories for {execution_date}")

with DAG(
    dag_id="daily_price_index",
    default_args=default_args,
    description="电商价格指数日计算任务",
    schedule_interval="0 3 * * *",  # 每天凌晨3点运行
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["analytics", "price-index"],
) as dag:

    run_task = PythonOperator(
        task_id="calculate_daily_index",
        python_callable=calculate_daily_index,
        op_kwargs={},  # 显式传递参数（可选）
    )
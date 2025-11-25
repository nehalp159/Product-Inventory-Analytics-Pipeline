from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
}

with DAG(
    dag_id="inventory_etl",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",  # run once a day
    catchup=False,
    default_args=default_args,
    tags=["inventory", "etl"],
) as dag:

    run_etl = BashOperator(
        task_id="run_python_etl",
        bash_command=(
            'cd "/Users/nehalpawar/airflow" && '
            'python3 etl_inventory_sales.py'
        ),
    )

    run_etl


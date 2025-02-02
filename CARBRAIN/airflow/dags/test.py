from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define a simple Python function that will be used as a task
def my_python_task():
    print("Hello from Airflow!")

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 31),  # Set start date to today or another date
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'my_first_dag',  # DAG name
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=None,  # This DAG will not run on a schedule, you can set this to a cron expression if needed
)

# Define the task using PythonOperator
task1 = PythonOperator(
    task_id='hello_task',  # Task ID
    python_callable=my_python_task,  # Python function to execute
    dag=dag,  # The DAG this task belongs to
)

# Optionally, add more tasks or dependencies here (if needed)

# This example only has one task, but you can add more and set dependencies between them like:
# task1 >> task2  # Task1 runs before task2

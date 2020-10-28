from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators import MyFirstOperator, MyFirstSensor


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 10, 25, 0, 0, 0),
    'retries': 3,
    'retry_delay': timedelta(minutes=10)
}


dag = DAG(dag_id='my_first_dag',
        max_active_runs=5,
        schedule_interval='0 * * * *',
        default_args=default_args,
        catchup=False)


task1 = MyFirstOperator(task_id='first_task', param='some random text', dag=dag)

# task 2 breaks the dag due to unknown keyword arguments 
task2 = MyFirstSensor(task_id='second_task', poke_interval=30, dag=dag)

# task2 >> task1
task1

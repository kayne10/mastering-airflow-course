from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.operators.sensors import BaseSensorOperator
import logging as log
from datetime import datetime


class MyFirstSensor(BaseSensorOperator):

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #all sensors need poke function
    def poke(self, context):
        current_minute = datetime.now().minute
        if current_minute % 2 != 0:
            return False
        task_instance = context['task_instance']
        task_instance.xcom_push('minute', current_minute)
        return True


class MyFirstOperator(BaseOperator):

    @apply_defaults
    def __init__(self, param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.param = param

    #all operators need exectute function
    def execute(self, context):
        task_instance = context['task_instance']
        minute = task_instance.xcom_pull('second_task', key='minute')
        log.info(minute)
        log.info(self.param)


class MyFirstPlugin(AirflowPlugin):
    name = 'my_first_plugin'
    operators = [MyFirstOperator, MyFirstSensor]
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []

    
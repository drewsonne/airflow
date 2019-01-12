from airflow.plugins_manager import AirflowPlugin


class AWSPlugin(AirflowPlugin):
    name = 'aws'
    configuration_providers = []

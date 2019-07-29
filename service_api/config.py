import sys
import os
import json


def get_port(app_name):
    with open('port_config.json', 'r') as f:
        data = json.load(f)
        return data[app_name]


def get_pg_host():
    if os.getenv('DOCK_ENV'):
        return 'mydb'
    return 'localhost'


mq_host = 'rabbitmq' if os.getenv('DOCK_ENV') else 'localhost'


class CeleryConfig:
    broker_url = f'amqp://admin:686314@{mq_host}/warehousehost'
    result_backend = f'db+postgresql://admin:admin@{get_pg_host()}/whreports'
    imports = ['service_api.services.tasks']


def select_db_config():
    if 'test' in str(sys.argv[0]):
        db_config = {
            'host': f'{get_pg_host()}',
            'user': 'postgres',
            'password': 'admin',
            'database': 'test_db'
        }
    else:
        db_config = {
            'host': f'{get_pg_host()}',
            'user': 'postgres',
            'password': 'admin',
            'database': 'whreports'
        }

    return db_config


BASIC_DB_CONFIG = {
    'host': f'{get_pg_host()}',
    'user': 'postgres',
    'password': 'admin',
    'database': 'postgres'
}

DEFAULT_SERVICE_NAME = "whreports"

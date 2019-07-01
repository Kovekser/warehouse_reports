import sys
import inspect


class CeleryConfig:
    broker_url = 'amqp://admin:686314@localhost/warehousehost'
    result_backend = 'db+postgresql://admin:admin@localhost/whreports'
    imports = ['service_api.services.tasks']


def select_db_config():
    caller = inspect.currentframe().f_back.f_code.co_name

    if 'test' in str(sys.argv[0]):
        DB_CONFIG = {
            'host': 'localhost',
            'user': 'postgres',
            'password': 'admin',
            'database': 'rstatus_test_db'
        }
    elif caller == 'create_db':
        DB_CONFIG = {
            'host': 'localhost',
            'user': 'postgres',
            'password': 'admin',
            'database': 'postgres'
        }
    elif caller in ('select_statement', 'execute_statement'):
        DB_CONFIG = {
            'host': 'localhost',
            'user': 'postgres',
            'password': 'admin',
            'database': 'whreports'
        }

    return DB_CONFIG

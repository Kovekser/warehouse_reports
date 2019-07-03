import sys


class CeleryConfig:
    broker_url = 'amqp://admin:686314@localhost/warehousehost'
    result_backend = 'db+postgresql://admin:admin@localhost/whreports'
    imports = ['service_api.services.tasks']


def select_db_config():
    if 'test' in str(sys.argv[0]):
        db_config = {
            'host': 'localhost',
            'user': 'postgres',
            'password': 'admin',
            'database': 'test_db'
        }
    else:
        db_config = {
            'host': 'localhost',
            'user': 'admin',
            'password': 'admin',
            'database': 'whreports'
        }

    return db_config


BASIC_DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'admin',
    'database': 'postgres'
}

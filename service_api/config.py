class CeleryConfig:
    broker_url = 'amqp://admin:686314@localhost/warehousehost'
    result_backend = 'rpc://'
    imports = ['service_api.services.tasks']

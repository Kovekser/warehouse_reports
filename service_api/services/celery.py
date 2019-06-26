from celery import Celery


app = Celery('service_api',
             backend='rpc://',
             broker='amqp://admin:686314@localhost/warehousehost',
             include=['service_api.services.tasks'])
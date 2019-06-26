from celery import Celery

from service_api.config import CeleryConfig


app = Celery('service_api')
app.config_from_object(CeleryConfig)

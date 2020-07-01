# warehouse_reports
Service genereates CSV reports from JSON input. Has 3 endpoints:
- creates delayed tasks on report generating
- checks generating process status
- downloads report to harddrive

Technologies: Python, Sanic, Celery (RabbitMQ worker + PostgresSQL backend)
Service is a part of microservices architecture of Warehouse application. Communicates with other microservice via REST client.

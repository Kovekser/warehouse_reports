# warehouse_reports
Service genereates CSV reports from JSON input. Has 3 endpoints:
- creates delayed tasks on report generating
- checking generating process status
- downloading report to harddrive

Technologies: Python, Sanic, Celery (RabbitMQ worker + PostgresSQL backend)

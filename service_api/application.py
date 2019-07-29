from sanic.blueprints import Blueprint
from sanic.app import Sanic

from service_api.config import DEFAULT_SERVICE_NAME
from service_api.resources.smoke_resource import SmokeResource
from service_api.resources.report_resource import (GenerateReportResource,
                                                   StatusReportResource,
                                                   DownloadReportResource)


def create_app():
    app = Sanic(DEFAULT_SERVICE_NAME)
    api_prefix = f'/{DEFAULT_SERVICE_NAME}'
    api = Blueprint('whreports', url_prefix=api_prefix)

    api.add_route(SmokeResource.as_view(), "/smoke")
    api.add_route(GenerateReportResource.as_view(), "/report")
    api.add_route(StatusReportResource.as_view(), "/report/status/<task_id>")
    api.add_route(DownloadReportResource.as_view(), "/report/download/<task_id>")
    app.blueprint(api)
    import os
    return app

app = create_app()
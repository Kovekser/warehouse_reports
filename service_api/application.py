from sanic.app import Sanic

from service_api.resources.smoke_resource import SmokeResource
from service_api.resources.report_resource import (GenerateReportResource,
                                                   StatusReportResource,
                                                   DownloadReportResource)

def create_app():
    app = Sanic()
    app.add_route(SmokeResource.as_view(), "/smoke")
    app.add_route(GenerateReportResource.as_view(), "/report")
    app.add_route(StatusReportResource.as_view(), "report/status/<task_id>")
    app.add_route(DownloadReportResource.as_view(), "report/download/<task_id>")
    return app

app = create_app()
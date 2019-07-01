from sanic.app import Sanic

from service_api.resources.smoke_resource import SmokeResource
from service_api.resources.report_resource import GenerateReportResource, StatusReportResourse

def create_app():
    app = Sanic()
    app.add_route(SmokeResource.as_view(), "/smoke")
    app.add_route(GenerateReportResource.as_view(), "/report")
    app.add_route(StatusReportResourse.as_view(), "report/status/<task_id>")

    return app

app = create_app()
from sanic.views import HTTPMethodView
from sanic.response import json

from service_api.services.tasks import generate_csv_report
from service_api.forms import ReportInputSchema


class GenerateReportResource(HTTPMethodView):
    async def post(self, request):
        data, err = ReportInputSchema().load(request.json)
        if err:
            return json({'Errors': err}, status=404)
        try:
            result_msg = generate_csv_report.delay(data['rtype'], data['headers'], data['data'])
            return json(result_msg.get(timeout=2), status=200)
        except ValueError as err:
            return json({'error': str(err)}, status=404)

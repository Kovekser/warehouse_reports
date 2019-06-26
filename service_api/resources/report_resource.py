from sanic.views import HTTPMethodView
from sanic.response import json

from service_api.services.tasks import generate_csv_report


class GenerateReportResource(HTTPMethodView):
    async def post(self, request):
        rtype, headers, data = request.json['rtype'], request.json['headers'], request.json['data']
        # For Oleh: may be its better instead of the code line above to write
        # locals().update(request.json) - creates automatically vars rtype, headers, data
        result_msg = generate_csv_report.delay(rtype, headers, data)
        return json(result_msg.get(timeout=2), status=200)

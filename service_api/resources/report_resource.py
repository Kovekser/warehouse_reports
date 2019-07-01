from time import sleep, localtime
from sanic.views import HTTPMethodView
from sanic.response import json

from service_api.services.tasks import generate_csv_report
from service_api.forms import ReportInputSchema
from service_api.domain.status_reports import (get_proc_status_by_id,
                                               insert_proc)


class GenerateReportResource(HTTPMethodView):
    async def post(self, request):
        data, err = ReportInputSchema().load(request.json)
        if err:
            return json({'Errors': err}, status=404)

        result = generate_csv_report.delay(data['rtype'], data['headers'], data['data'])
        await insert_proc({'task_id': result.id,
                          'status': result.state,
                          'rtype': data['rtype']})

        return json({'msg': f'Process with id {result.id} was successfully launched',
                     'proc_id': result.id},
                    status=200)


class StatusReportResourse(HTTPMethodView):
    async def get(self, request, task_id):
        result = await get_proc_status_by_id(task_id)
        return json({'proc_status': result['status']})

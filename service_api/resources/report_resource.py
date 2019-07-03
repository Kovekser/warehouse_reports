from sanic.views import HTTPMethodView
from sanic.response import json, file

from service_api.services.tasks import generate_csv_report
from service_api.forms import ReportInputSchema
from service_api.domain.status_reports import (get_process_object_by_id,
                                               insert_process_object)


class GenerateReportResource(HTTPMethodView):
    async def post(self, request):
        data, err = ReportInputSchema().load(request.json)
        if err:
            return json({'Errors': err}, status=404)

        result = generate_csv_report.delay(data['report_type'], data['headers'], data['data'])
        await insert_process_object({'task_id': result.id,
                                     'status': result.state,
                                     'report_type': data['report_type']})

        return json({'msg': f'Process with id {result.id} was successfully launched',
                     'process_id': result.id},
                    status=200)


class StatusReportResource(HTTPMethodView):
    async def get(self, request, task_id):
        process_obj = await get_process_object_by_id(task_id)
        if process_obj['status'] == 'PENDING':
            return json({'process_status': process_obj['status'],
                         'msg': 'Report is not ready'}, status=200)
        elif process_obj['status'] == 'FAILED':
            return json({'process_status': process_obj['status'],
                         'msg': process_obj['details']}, status=404)
        elif process_obj['status'] == 'SUCCESS':
            return json({'process_status': process_obj['status']}, status=200)


class DownloadReportResource(HTTPMethodView):
    async def get(self, request, task_id):
        process_obj = await get_process_object_by_id(task_id)
        return await file(process_obj['file_name'], status=200,
                          headers={"Content-type": "text/csv",
                                   "Content-Disposition": f"inline; filename={process_obj['file_name']}"})

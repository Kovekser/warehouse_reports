from sanic.views import HTTPMethodView
from sanic.response import json, file

from service_api.services.tasks import generate_csv_report
from service_api.forms import ReportInputSchema
from service_api.domain.status_reports import (get_proc_status_by_id,
                                               insert_proc,
                                               download_file)


class GenerateReportResource(HTTPMethodView):
    async def post(self, request):
        data, err = ReportInputSchema().load(request.json)
        if err:
            return json({'Errors': err}, status=404)

        result = generate_csv_report.delay(data['report_type'], data['headers'], data['data'])
        await insert_proc({'task_id': result.id,
                          'status': result.state,
                          'report_type': data['report_type']})

        return json({'msg': f'Process with id {result.id} was successfully launched',
                     'process_id': result.id},
                    status=200)


class StatusReportResource(HTTPMethodView):
    async def get(self, request, task_id):
        result = await get_proc_status_by_id(task_id)
        return json({'process_status': result['status']})


class DownloadReportResource(HTTPMethodView):
    async def get(self, request, document_id):
        csv_file = await download_file(document_id)
        return await file(csv_file, status=200,
                    headers={"Content-type": "text/csv",
                             "Content-Disposition": f"inline; filename={csv_file}"})

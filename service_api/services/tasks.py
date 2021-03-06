import asyncio
import uvloop
from celery import shared_task

from service_api.domain.reports import CSVReports


@shared_task(bind=True)
def generate_csv_report(self, report_type, headers, data):
    result = run_in_new_loop(CSVReports(report_type, headers, data).generate_csv_report())
    return result


def run_in_new_loop(coroutine):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(coroutine)
    loop.close()
    return result

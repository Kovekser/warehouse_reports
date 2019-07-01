from celery.result import AsyncResult
from sqlalchemy import select

from service_api.models import ReportStatus
from service_api.services.db import select_statement, execute_statement


async def update_task_status(task_id):
    result = AsyncResult(task_id)
    if result.successful():
        await update_proc_status_by_id({'task_id': task_id,
                                        'status': 'SUCCESS',
                                        'file_name': result.get()['file_name']})
    elif result.failed():
        await update_proc_status_by_id({'task_id': task_id, 'status': 'FAILED'})
    else:
        await update_proc_status_by_id({'task_id': task_id, 'status': 'PENDING'})


async def get_proc_status_by_id(task_id):
    await update_task_status(task_id)
    statement = ReportStatus.select(). \
        where(ReportStatus.c.task_id == task_id)
    return await select_statement(statement)


async def insert_proc(data):
    statement = ReportStatus.insert().\
        values(**data)
    await execute_statement(statement)


async def update_proc_status_by_id(data):
    statement = ReportStatus.update().\
        values(**data).\
        where(ReportStatus.c.task_id == data['task_id'])
    return await execute_statement(statement)


async def get_file_name_by_id(document_id):
    statement = select([ReportStatus.c.file_name]). \
        select_from(ReportStatus). \
        where(ReportStatus.c.task_id == document_id)
    process_status = await get_proc_status_by_id(document_id)

    if process_status['status'] == 'SUCCESS':
        return await select_statement(statement)


async def download_file(document_id):
    file_url = await get_file_name_by_id(document_id)
    return file_url['file_name']
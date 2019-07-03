from asynctest import patch, CoroutineMock, PropertyMock

from tests.domain_tests import BaseDomainTest
from service_api.domain.status_reports import (update_proc_status_by_id,
                                               insert_process_object,
                                               get_process_object_by_id,
                                               update_task_status)


class ReportsStatusTest(BaseDomainTest):

    @patch("service_api.domain.status_reports.update_task_status",
           new=CoroutineMock())
    async def test_insert_process_object(self):
        await insert_process_object({'task_id': '821d9bca-59b0-487e-9639-460b2805e3e2',
                                     'status': 'SUCCESS',
                                     'file_name': 'test_2019_07_01_07_46_24_127902.csv',
                                     'report_type': 'test'})
        result = await get_process_object_by_id('821d9bca-59b0-487e-9639-460b2805e3e2')

        self.assertEqual(6, len(result))
        self.assertEqual('821d9bca-59b0-487e-9639-460b2805e3e2', str(result.get('task_id')))
        self.assertEqual('SUCCESS', result.get('status'))
        self.assertEqual('test_2019_07_01_07_46_24_127902.csv', result.get('file_name'))

    @patch("service_api.domain.status_reports.update_task_status",
           new=CoroutineMock())
    async def test_update_proc_status_by_id(self):
        await insert_process_object({'task_id': '721d9bca-59b0-487e-9639-460b2805e3e2',
                                     'status': 'PENDING',
                                     'report_type': 'test'})
        result = await get_process_object_by_id('721d9bca-59b0-487e-9639-460b2805e3e2')

        self.assertEqual(6, len(result))
        self.assertEqual('721d9bca-59b0-487e-9639-460b2805e3e2', str(result.get('task_id')))
        self.assertEqual('PENDING', result.get('status'))
        self.assertEqual(None, result.get('file_name'))

        await update_proc_status_by_id({'task_id': '721d9bca-59b0-487e-9639-460b2805e3e2',
                                        'status': 'SUCCESS',
                                        'file_name': 'test_2019_07_01_07_46_24_127902.csv'})
        result = await get_process_object_by_id('721d9bca-59b0-487e-9639-460b2805e3e2')

        self.assertEqual(6, len(result))
        self.assertEqual('721d9bca-59b0-487e-9639-460b2805e3e2', str(result.get('task_id')))
        self.assertEqual('SUCCESS', result.get('status'))
        self.assertEqual('test_2019_07_01_07_46_24_127902.csv', result.get('file_name'))

    @patch("celery.result.AsyncResult.get")
    @patch("service_api.domain.status_reports.update_proc_status_by_id")
    @patch("celery.result.AsyncResult.failed")
    @patch("celery.result.AsyncResult.successful")
    async def test_update_task_status_success(self, task_successful_mock, task_failed_mock, update_mock, task_get_mock):
        task_id = '821d9bca-59b0-487e-9639-460b2805e3e2'
        task_successful_mock.return_value = True
        task_failed_mock.return_value = False
        task_get_mock.return_value = {'file_name': 'test_2019_07_01_07_46_24_127902.csv'}
        await update_task_status(task_id)

        update_mock.assert_called_once_with({'task_id': '821d9bca-59b0-487e-9639-460b2805e3e2',
                                             'status': 'SUCCESS',
                                             'file_name': 'test_2019_07_01_07_46_24_127902.csv'})

    @patch("celery.result.AsyncResult.info",
           new=PropertyMock(return_value="The length of row 1 doesn't match to the length of the header"))
    @patch("service_api.domain.status_reports.update_proc_status_by_id")
    @patch("celery.result.AsyncResult.failed")
    @patch("celery.result.AsyncResult.successful")
    async def test_update_task_status_failed(self, task_successful_mock, task_failed_mock, update_mock):
        task_id = '821d9bca-59b0-487e-9639-460b2805e3e2'
        task_successful_mock.return_value = False
        task_failed_mock.return_value = True
        await update_task_status(task_id)

        update_mock.assert_called_once_with({"task_id": "821d9bca-59b0-487e-9639-460b2805e3e2",
                                             "status": "FAILED",
                                             "details": "The length of row 1 doesn't match "
                                                        "to the length of the header"})

    @patch("service_api.domain.status_reports.update_proc_status_by_id")
    @patch("celery.result.AsyncResult.failed")
    @patch("celery.result.AsyncResult.successful")
    async def test_update_task_status_pending(self, task_successful_mock, task_failed_mock, update_mock):
        task_id = '821d9bca-59b0-487e-9639-460b2805e3e2'
        task_successful_mock.return_value = False
        task_failed_mock.return_value = False
        await update_task_status(task_id)

        update_mock.assert_called_once_with({"task_id": "821d9bca-59b0-487e-9639-460b2805e3e2",
                                             "status": "PENDING"})

from asynctest import patch, CoroutineMock, PropertyMock, Mock
from copy import deepcopy

from tests import BaseTestCase
from tests.resource_tests import REPORT_INPUT_MOCK, PROCESS_OBJ_MOCK
from service_api.services.celery import app


class SmokeResourceTest(BaseTestCase):
    def test_get_smoke(self):
        response = self.test_client.get('/smoke', gather_request=False)
        self.assertEqual(200, response.status)
        self.assertEqual({'Result': 'This is a smoke view'}, response.json)


class GenerateReportResourceTest(BaseTestCase):
    url = '/report'
    task_id = '11111111-2222-3333-4444-555555555555'

    # def setUp(self):
    #     app.conf.update(task_eager_propagates=True, task_always_eager=True, broker_url='memory://', backend='memory')

    def test_generate_report_empty_request(self):
        response = self.test_client.post(self.url, gather_request=False,
                                         json={})
        expected = {'Errors':
                        {'data': ['Missing data for required field.'],
                         'report_type': ['Missing data for required field.'],
                         'headers': ['Missing data for required field.']}
                    }

        self.assertEqual(404, response.status)
        self.assertEqual(expected, response.json)

    # @patch("service_api.resources.report_resource.insert_process_object")
    # def test_generate_report_success(self, insert_proc_mock):
    #     response = self.test_client.post(self.url, gather_request=False,
    #                                      json=REPORT_INPUT_MOCK)
    #
    #     insert_proc_mock.assert_called_once_with({'task_id': '11111111-2222-3333-4444-555555555555',
    #                                               'status': 'SUCCESS',
    #                                               'report_type': 'test'})
    #     self.assertEqual(200, response.status)
    #     self.assertEqual({'msg': f'Process with id 11111111-2222-3333-4444-555555555555 was successfully launched',
    #                       'process_id': '11111111-2222-3333-4444-555555555555'}, response.json)


class StatusReportResourceTest(BaseTestCase):
    task_id = '11111111-2222-3333-4444-555555555555'
    url = f'/report/status/{task_id}'
    test_case_failed = dict(deepcopy(PROCESS_OBJ_MOCK), **{'status': 'FAILED'})
    test_case_success = dict(deepcopy(PROCESS_OBJ_MOCK), **{'status': 'SUCCESS'})
    test_case_pending = dict(deepcopy(PROCESS_OBJ_MOCK), **{'status': 'PENDING'})

    @patch("service_api.resources.report_resource.get_process_object_by_id",
           new=CoroutineMock(return_value=test_case_pending))
    def test_get_status_pending(self):
        response = self.test_client.get(self.url, gather_request=False)

        self.assertEqual(200, response.status)
        self.assertEqual({'process_status': 'PENDING',
                         'msg': 'Report is not ready'},
                         response.json)

    @patch("service_api.resources.report_resource.get_process_object_by_id",
           new=CoroutineMock(return_value=test_case_failed))
    def test_get_status_failed(self):
        response = self.test_client.get(self.url, gather_request=False)

        self.assertEqual(404, response.status)
        self.assertEqual({'process_status': 'FAILED',
                          'msg': 'ValueError("dict contains fields not in fieldnames: \'d\'")'},
                         response.json)

    @patch("service_api.resources.report_resource.get_process_object_by_id",
           new=CoroutineMock(return_value=test_case_success))
    def test_get_status_success(self):
        response = self.test_client.get(self.url, gather_request=False)

        self.assertEqual(200, response.status)
        self.assertEqual({'process_status': 'SUCCESS'},
                         response.json)

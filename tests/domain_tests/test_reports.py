import os
from freezegun import freeze_time

from tests import BaseTestCase
from service_api.domain.reports import CSVReports


@freeze_time("2019-07-01 07:46:24.127902")
class CSVReportsTest(BaseTestCase):

    @classmethod
    def tearDownClass(cls):
        csv_filelist = [f for f in os.listdir(os.getcwd()) if f.endswith(".csv")]
        for f in csv_filelist:
            os.remove(os.path.join(os.getcwd(), f))

    def test_generate_csv_report_wrong_number_of_columns(self):
        with self.assertRaises(ValueError) as err:
            CSVReports(report_type='test',
                       head=["a", "b", "c"],
                       data=[{"a": 4, "b": 5, "c": 6, "d": 7}])
        self.assertEqual("The length of row 1 doesn't match to the length of the header", str(err.exception))

    async def test_generate_csv_report_wrong_data(self):
        with self.assertRaises(ValueError) as err:
            csv_reports = CSVReports(report_type='test',
                                     head=["a", "b", "c"],
                                     data=[{"a": 4, "b": 5, "d": 7}])
            await csv_reports.generate_csv_report()

        self.assertEqual("dict contains fields not in fieldnames: 'd'", str(err.exception))

    async def test_generate_csv_report_success(self):
        expected = {'msg': f'Report test_2019_07_01_07_46_24_127902.csv was successfully generated and downloaded to disc',
                    'file_name': 'test_2019_07_01_07_46_24_127902.csv'}
        csv_reports = CSVReports(report_type='test',
                                 head=["a", "b", "c"],
                                 data=[{"a": 4, "b": 5, "c": 7}])
        result = await csv_reports.generate_csv_report()

        self.assertTrue(os.path.exists('test_2019_07_01_07_46_24_127902.csv'))
        self.assertDictEqual(expected, result)

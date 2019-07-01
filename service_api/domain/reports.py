import csv
import os
from datetime import datetime


class CSVReports:
    def __init__(self, report_type, head, data):
        self.csv_name = f'{report_type}_{datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S_%f")}.csv'
        self.head = head
        self.__data = self.check_data(data, head)

    @classmethod
    def check_data(cls, data, head):
        """
        Function checks if there are rows with length more than length of header
        and deletes invalid rows if any
        """
        for i, row in enumerate(data):
            if len(row) != len(head):
                raise ValueError(f'The length of row {i+1} doesn\'t match to the length of the header')
        return data

    async def generate_csv_report(self):
        try:
            with open(self.csv_name, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.head, delimiter=',', quotechar='"')

                writer.writeheader()
                writer.writerows(self.__data)
            return {'msg': f'Report {self.csv_name} was successfully generated and downloaded to disc',
                    'file_name': self.csv_name}
        except ValueError as err:
            if os.path.exists(self.csv_name):
                os.remove(self.csv_name)
            raise ValueError(err)

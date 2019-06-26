import csv
import os
import logging
from datetime import datetime


class Reports:
    def __init__(self, rtype, head, data):
        self.csv_name = f'{rtype}_{datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")}.csv'
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
                del(data[i])
                logging.error(f'The length of row {i+1} doesn\'t match to the length of the header')
                continue
        return data

    async def download_csv_report(self):
        print('Starting downloading')
        try:
            with open(self.csv_name, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.head)

                writer.writeheader()
                writer.writerows(self.__data)
            return {'msg': f'Report {self.csv_name} was successfully downloaded to disc'}
        except ValueError as err:
            os.remove(self.csv_name)
            return {'error': str(err)}

# author: goodalg0s@gmail.com

import csv
import logging
from typing import NewType
from .map import NEM_FIELD_MAP
from pprint import pprint

ALLOWED_HEADERS = (
    '100',
    '250',
    '550'
)

logger = logging.getLogger(__name__)


class NemParser(object):

    def __init__(self, nemfile):
        self.nemfile = nemfile
        self.parsed_rows = []

    def read_csv(self) -> None:
        with open(self.nemfile, 'r') as f:
            csvrows = csv.reader(f, delimiter=',')

            for row in csvrows:
                header = row[0]

                if header in ALLOWED_HEADERS:
                    self.parse_row(header, row)

    def verify_row_length(self, header, row) -> bool:
        ''' return True if row has sufficient expected elements,
            otherwise False
        '''
        actual_length = len(row)
        expected_length = len(NEM_FIELD_MAP[header])

        if actual_length >= expected_length:
            return True
        return False

    def parse_row(self, header, row) -> dict:
        if self.verify_row_length(header, row) is False:
            return None

        try:
            fields = NEM_FIELD_MAP[header]
            record = {f: row[i] for i, f in enumerate(fields)}
            return record

        except Exception as e:
            print(f"!!!!!Parse Error: {e} ")
            print(f"Errored Row: {row}")

        print("\n")

    def run(self):
        self.read_csv()

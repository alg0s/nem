# author: goodalg0s@gmail.com

import csv
from .map import NEM_MAP


class NemParser(object):

    def __init__(self, nemfile):
        self.nemfile = nemfile
        self.reader = None
        self.parsed_rows = []

    def read_csv(self):
        with open(self.nemfile, 'r') as f:
            self.reader = csv.reader(f, delimiter=',')

            for r in self.rows:
                header = r[0]

                if header == '100':
                    self.parse_row_100(r)
                elif header == '250':
                    self.parse_row_250(r)
                elif header == '550':
                    self.parse_row_550(r)

    def verify_row_length(self, header, row):
        ''' return True if row has sufficient expected elements,
            otherwise False
        '''
        if len(row) >= len(NEM_MAP[header]):
            return True
        return False

    def parse_row_100(self, row):
        if self.verify_row_length is False:
            return None
        header = '100'
        columns = NEM_MAP[header]

    def parse_row_250(self, row):
        print("250: ", row)

    def parse_row_550(self, row):
        print("550: ", row)

    def run(self):
        self.read_csv()

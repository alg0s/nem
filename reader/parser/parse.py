# author: goodalg0s@gmail.com
import csv
import logging
from datetime import datetime
from decimal import Decimal
from .map import NEM_FIELD_MAP
from .schema import Schema
from reader.models import (
    NemFile,
    Record100,
    Record250,
    Record550,
    ReaderRun,
    ReaderError,
    NemFileError,
)
from reader.errors import (
    FieldParseError,
    RowParseError,
    InvalidRowError,
)
from pathlib import Path

# logger = logging.getLogger(__name__)


ALLOWED_DATETIME_FORMAT = {
    8: '%Y%m%d',
    12: '%Y%m%d%H%M',
    14: '%Y%m%d%H%M%S',
}

ALLOWED_STRING_FORMAT = (
    'varchar',
    'char',
)

END_OF_FILE_INDICATOR = '900'


class Field(object):
    ''' Represent a single field in a NEM file row

        Attributes:
        -----------
            :value: str
                value of the field imported
            :parsed_value: str|int|datetime
                parsed valued of the value
            :sequence: int
                sequence of the field in the row imported
            :length: int
                length of the string
            :record_type: str
                name of the record type (row type)
            :name: str
                name of the field as defined in the Schema
            :data_type: str
                data type of the field as defined in the Schema
    '''

    def __init__(self, sequence: int, value: str, record_type: str):
        self.value = value
        self.sequence = sequence
        self.record_type = record_type
        self.length = len(value)
        self.parsed_value = None

        defined = Schema.get_field(record_type, sequence)
        if defined is None:
            raise FieldParseError("Invalid Field Sequence")

        self.name = defined['name']
        self.data_type = defined['data_type']
        self.defined_length = defined['length']
        self.parse()

    def __str__(self):
        return self.name + '-' + self.data_type + ': ' + self.value

    def _is_length_valid(self) -> bool:
        if self.defined_length is None:
            return True
        if self.data_type in ['datetime', 'date']:
            return self.length in ALLOWED_DATETIME_FORMAT
        return self.length <= self.defined_length

    def _parse_datetime(self) -> datetime:
        value = self.value.replace(" ", "")
        datetime_format = ALLOWED_DATETIME_FORMAT[self.length]
        try:
            return datetime.strptime(value, datetime_format)
        except ValueError:
            raise FieldParseError(
                f"Unable to parse datetime field: {self.value}"
            )

    def _parse_numeric(self) -> int:
        # clean value
        value = self.value.replace(" ", "")
        try:
            if self.name == 'quantity':
                return Decimal(value)
            else:
                return int(value)
        except ValueError:
            raise FieldParseError(
                f"Unable to parse numeric field: {self.value}"
            )

    def get_parsed_value(self):
        return self.parsed_value

    def get_name(self):
        return self.name

    def parse(self):
        if self.value != '':
            if self._is_length_valid() is False:
                raise FieldParseError(
                    f"Invalid value length: {self.value}, expected: {self.defined_length}"
                )
            if self.data_type in ALLOWED_STRING_FORMAT:
                self.parsed_value = self.value
            elif self.data_type in ['date', 'datetime']:
                self.parsed_value = self._parse_datetime()
            elif self.data_type == 'numeric':
                self.parsed_value = self._parse_numeric()


class Row(object):
    ''' Represent a row in a NEM file

        Attributes:
        -----------
            :record_type: str
                type of the row, indicated by the first value, i.e 100, 250, 550
            :values: list of str
                list of string values imported from the NEM file
            :fields: list of Field instances
                list of Field instances containing the parsed value
            :nemfile: NemFile
                the NEM file instance containing the row
            :parent_pk: int
                Primary key of the parent row, i.e 100 for 250, or 250 for 550
            :expected_row_length: int
                the expected length of the row defined in the schema
    '''

    def __init__(self, values: list, nemfile: NemFile):
        self.nemfile = nemfile
        self.values = values
        self.record_type = values[0]
        self.expected_row_length = Schema.get_expected_row_length(
            self.record_type)
        self.fields = []

    def length(self):
        return len(self.values)

    def is_valid_row_length(self) -> bool:
        ''' return True if row has sufficient expected elements, otherwise False '''

        actual_length = self.length()
        expected_length = Schema.get_expected_row_length(self.record_type)

        if actual_length != expected_length:
            NemFileError.objects.create(
                nemfile=self.nemfile,
                description=", ".join([
                    f"Invalid Row Length: expected {expected_length}",
                    f"actual {actual_length}",
                    f"row: {self.values}"
                ])
            )
            return False
        return True

    def is_valid_record_type(self) -> bool:
        if self.record_type not in Schema.get_record_types():
            NemFileError.objects.create(
                nemfile=self.nemfile,
                description=f"Invalid Record Type: {self.record_type}"
            )
            return False
        return True

    def parse(self):
        # 1. validate record type
        if self.is_valid_record_type() is False:
            raise InvalidRowError(f"Invalid Record Indicator: {self.values}")

        # 2. validate row length
        if self.is_valid_row_length() is False:
            raise InvalidRowError(f"Invalid Row Length: {self.values}")

        # 3. parse fields in the row
        try:
            self.fields = [Field(sequence, value, self.record_type)
                           for sequence, value in enumerate(self.values)]

        except FieldParseError as e:
            NemFileError.objects.create(nemfile=self.nemfile, description=e)
            raise RowParseError(f"Unable to parse: {self.values}: {e}")

    def to_dict(self) -> dict:
        ''' return a dict of field name and parsed value '''

        rdict = {f.get_name(): f.get_parsed_value() for f in self.fields}
        rdict['nemfile'] = self.nemfile
        return rdict


class NemParser(object):
    ''' Handle reading a NEM CSV file, parsing data and importing into the database.

        Ingestion Policy:
        -----------------
            NemParser has a strict data ingestion policy: only non-corrupted NEM file 
            shall be imported into the database. It means that if the parser finds 
            any errors during the process, either from the row or the field, it will
            not save the data into the database. It will log the errors in two tables
            ReaderError and NemFileError. This will help avoid having to cleaning up 
            the data when one or more rows have been incorrect or corrupted. 

        Error Handling:
        ---------------
            If there is an error occurs during the parsing process, the file's data
            shall not be ingested into the database, and the ReaderRun table shall
            record an Failed run of the file. This is to make sure that only proper
            data are imported and no file is ingested twice.

        Attributes:
        -----------
            :filepath: str
                file path of the NEM file being processed
            :filename: str
                file name extracted from the input file path
            :parsed_rows: list of Row instances
                list of parsed rows
            :invalid_rows: list of list of str
                list of invalid rows that can't be processed
            :total_rows: int
                total number of rows in the NEM file
    '''

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = self._get_filename(filepath)
        self.parsed_rows = []
        self.invalid_rows = []
        self.total_rows = 0

    def _get_filename(self, filepath):
        filename = Path(filepath).name
        return filename

    def run(self):
        # 1. create NemFile
        nemfile, created = NemFile.objects.get_or_create(
            name=self.filename,
        )
        if created is True:
            nemfile.path = self.filepath
            nemfile.save()

        # 2. create ReaderRun
        reader_run = ReaderRun.objects.create(
            nemfile=nemfile,
        )

        with open(self.filepath, 'r') as f:
            csvreader = csv.reader(f, delimiter=',')

            # 3. process each row
            for row in csvreader:
                self.total_rows += 1
                record_type = row[0]

                if record_type == END_OF_FILE_INDICATOR:
                    continue

                try:
                    r = Row(row, nemfile)
                    r.parse()
                    self.parsed_rows.append(r)
                except (InvalidRowError, RowParseError) as e:
                    self.invalid_rows.append(row)
                    ReaderError.objects.create(
                        reader_run=reader_run,
                        description=e,
                    )

            # 3. save records to database
            number_invalid_rows = len(self.invalid_rows)

            # update ReaderRun
            reader_run.number_invalid_records = number_invalid_rows
            reader_run.total_records = self.total_rows

            if number_invalid_rows > 0:
                reader_run.status = 'F'
            else:
                reader_run.status = 'S'

                # previous_types stores the primary key of each record type in the NEM file
                previous_type_rows = {}

                for r in self.parsed_rows:
                    rdict = r.to_dict()

                    # check parent type
                    parent_type = Schema.get_parent_type(r.record_type)

                    if parent_type in previous_type_rows:
                        parent_key = 'record' + parent_type
                        rdict[parent_key] = previous_type_rows[parent_type]

                    saved_row = None

                    # save to database
                    if r.record_type == '100':
                        saved_row = Record100.objects.create(**rdict)
                    elif r.record_type == '250':
                        saved_row = Record250.objects.create(**rdict)
                    elif r.record_type == '550':
                        saved_row = Record550.objects.create(**rdict)

                    if saved_row is not None:
                        previous_type_rows[r.record_type] = saved_row

            # 4. Update ReaderRun
            reader_run.save()

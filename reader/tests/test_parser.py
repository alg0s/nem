# author: goodalg0s@gmail.com
from django.test import TestCase
from django.db.utils import IntegrityError
from reader.parser import (
    Field,
    Row,
    NemParser
)
from reader.parser import Schema


class Field_Test(TestCase):

    def setUp(self):
        pass

    def test_01_invalid_length(self):
        pass

    def test_02_raise_FieldParserError_invalid_numeric(self):
        pass

    def test_03_raise_FieldParserError_invalid_datetime(self):
        pass

    def test_04_valid_field_parsed(self):
        pass


class Row_Test(TestCase):

    def setUp(self):
        pass

    def test_01_invalid_row_length(self):
        pass

    def test_02_invalid_record_type(self):
        pass

    def test_03_valid_row_parsed(self):
        pass

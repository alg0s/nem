# author: goodalg0s@gmail.com
from django.test import TestCase
from django.db.utils import IntegrityError
from .factories import (
    NemFile_Factory,
)


class NemFile_Test(TestCase):

    def test_01_retrieve(self):
        nem = NemFile_Factory.create(name='sample.csv')
        self.assertEqual(nem.name, 'sample.csv')

    def test_02_unique_name(self):
        nem = NemFile_Factory.create(name='sample.csv')
        with self.assertRaises(IntegrityError):
            NemFile_Factory.create(name=nem.name)

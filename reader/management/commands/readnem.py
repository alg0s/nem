# author: goodalg0s@gmail.com

from django.core.management.base import (
    BaseCommand,
    CommandError
)
from reader.parser import NemParser


class Command(BaseCommand):
    ''' Read a NEM file, parse and store to the database

    Arguments:
    ----------

    '''

    help = "Read a NEM file and store into the database"

    def add_arguments(self, parser):
        parser.add_argument('-a', '--path', type=str,
                            required=True, help="NEM file path")

    def handle(self, *args, **options):
        ''' validate arguments, file extension and read the file '''

        filepath = options['path']

        if not filepath.endswith('.csv'):
            raise CommandError(f"Incorrect File Extension: {filepath}")

        print(f"Reading file {filepath}...")

        NemParser(filepath).run()

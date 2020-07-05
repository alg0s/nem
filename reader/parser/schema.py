# author: goodalg0s@gmail.com
import os
import yaml
import logging

logger = logging.getLogger(__name__)


SCHEMA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'schema.yaml'
)


class NemSchema:
    ''' Represent a defined schema of NEM file 

        Attributes:
        -----------
            :author:
                defined in schema.yaml
            :created_at:
                defined in schema.yaml
            :data: (dict)
                dictionary with schema details
    '''

    def __init__(self):
        self.author = None
        self.created_at = None
        self.data = self._load()
        self.data_dict = self._to_dict()

    def _load(self):
        with open(SCHEMA_FILE) as f:
            return yaml.full_load(f)

    # TODO: to delete
    def _to_dict(self):
        data = {}
        record_types = self.data['record_types']

        # transform a list of fields into a dict
        for rtype, field_list in record_types.items():
            fields = {
                field['name']: {
                    k: v for k, v in field.items() if k != 'name'
                }
                for field in field_list
            }
            data[rtype] = fields
        return data

    def get_field(self, record_type, sequence) -> dict:
        ''' return details of a field 
            return None if field sequence is out of indices
        '''
        try:
            return self.data['record_types'][record_type][sequence]
        except KeyError:
            print(
                f"Unable to find sequence in record type: {sequence} - {record_type}")

    def get_expected_row_length(self, record_type) -> int:
        ''' return expected row length of a record type '''
        return len(self.data['record_types'][record_type])

    def get_record_types(self) -> list:
        ''' return record types defined in the schema '''
        return self.data['record_types'].keys()

    def get_parent_type(self, record_type) -> str:
        ''' return the parent record type for a record type '''
        try:
            return self.data['parent_types'][record_type]
        except KeyError:
            return None


Schema = NemSchema()

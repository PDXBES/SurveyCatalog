from dataio.db_data_io import DbDataIo
from config import Config
import arcpy
try:
    from typing import List, Any, Dict
except:
    pass

class GenericObject(object):
    def __init__(self, config):
        self.config = config
        self.id = None
        self.parent_id = None
        self.input_field_attribute_lookup = None

    @classmethod
    def initialize_with_current_id(cls, config, db_data_io):
        # type: (Config, DbDataIo) -> GenericObject
        generic_object = cls(config)
        generic_object_current_id = db_data_io.retrieve_current_id(cls)
        generic_object.id = generic_object_current_id
        return generic_object

    @staticmethod
    def input_field_attribute_lookup():
        pass
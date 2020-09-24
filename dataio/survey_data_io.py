import os
import arcpy
import json
import traceback
from businessclasses.config import Config
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWRITE, S_IWGRP, S_IWOTH
import xml.etree.ElementTree as ET
try:
    from typing import List, Any
except:
    pass
from businessclasses.survey_return import SurveyReturn


from db_data_io import DbDataIo
from object_data_io import ObjectDataIo


class SurveyDataIo(ObjectDataIo):
    def __init__(self, config, db_data_io):
        # type: (Config, DbDataIo) -> None
        self.config = config
        self.db_data_io = db_data_io

    def copy_geometry_to_memory(self, input_table, output_table_name, db_data_io, model, id_field, object_type):
        db_data_io.copy_to_memory(input_table, output_table_name)
        output_table = db_data_io.workspace + "\\" + output_table_name
        db_data_io.add_ids(output_table, id_field, object_type)
        db_data_io.add_parent_id(output_table, "MODEL_ID", model.id)

    #TODO - change to survey_point
    def append_survey_return(self, model):
        input_gdb = model.model_path + "\\" + "EmgaatsModel.gdb"
        input_table = input_gdb + "\\" + "Storages"
        output_table_name = "in_memory_table_storage"
        output_table = self.db_data_io.workspace + "\\" + output_table_name
        id_field = "model_catalog_storage_id"
        object_type = SurveyReturn
        self.copy_geometry_to_memory(input_table, output_table_name, self.db_data_io, model, id_field, object_type)
        self.db_data_io.append_table_to_db(output_table, self.config.storage_sde_path)

        arcpy.Delete_management(output_table)



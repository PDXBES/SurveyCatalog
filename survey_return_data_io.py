import arcpy
from config import Config

try:
    from typing import List, Any
except:
    pass

from survey_return import SurveyReturn
from survey_point import SurveyPoint
from db_data_io import DbDataIo
from object_data_io import ObjectDataIo


class SurveyReturnDataIo(ObjectDataIo):
    def __init__(self, config, db_data_io):
        # type: (Config, DbDataIo) -> None
        self.config = config
        self.db_data_io = db_data_io

    #TODO - check mod
    def copy_geometry_to_memory(self, input_table, output_table_name, db_data_io, survey_return, id_field, object_type):
        db_data_io.copy_to_memory(input_table, output_table_name)
        output_table = db_data_io.workspace + "\\" + output_table_name
        db_data_io.add_ids(output_table, id_field, object_type)
        db_data_io.add_parent_id(output_table, "Survey_Return_ID", survey_return.id)

    #TODO - change to survey_point
    def append_survey_return(self, survey_return):
        #input_gdb = survey_return.survey_return_path + "\\" + "EmgaatsModel.gdb"
        #input_table = input_gdb + "\\" + "Storages"
        #input_table can be in memory OR file version of geocoded/formatted raw survey
        input_table = r"\\besfile1\asm_projects\E11098_Council_Crest\survey\mgmt_process\data\working_delete.gdb\SurveyPoints"
        output_table_name = "in_memory_table_survey_points"
        output_table = self.db_data_io.workspace + "\\" + output_table_name
        id_field = "Survey_Point_ID"
        object_type = SurveyPoint
        self.copy_geometry_to_memory(input_table, output_table_name, self.db_data_io, survey_return, id_field, object_type)
        self.db_data_io.append_table_to_db(output_table, self.config.survey_points_path)

        arcpy.Delete_management(output_table)



import os
import arcpy
from config import Config
from generic_object import GenericObject
from collections import OrderedDict
import datetime

try:
    from typing import List, Any
except:
    pass

class SurveyReturn(GenericObject):

    def __init__(self, config):
        # type: (Config) -> None
        self.id = 0
        self.parent_model_id = 0


    #TODO - don't know if I need field_attr_lookup
    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Model_ID"] = "id"
        field_attribute_lookup["Parent_Model_ID"] = "parent_model_id"
        field_attribute_lookup["Model_Request_ID"] = "model_request_id"
        field_attribute_lookup["Project_Phase_ID"] = "project_phase_id"
        field_attribute_lookup["Engine_Type_ID"] = "engine_type_id"
        field_attribute_lookup["Create_Date"] = "create_date"
        field_attribute_lookup["Created_by"] = "created_by"
        field_attribute_lookup["Deploy_Date"] = "deploy_date"
        field_attribute_lookup["Extract_Date"] = "extract_date"
        field_attribute_lookup["Run_Date"] = "run_date"
        field_attribute_lookup["Model_Name"] = "model_name"
        field_attribute_lookup["Model_Path"] = "model_path"
        field_attribute_lookup["Model_Purpose_ID"] = "model_purpose_id"
        field_attribute_lookup["Model_Calibration_file"] = "model_calibration_file"
        field_attribute_lookup["Model_Status_ID"] = "model_status_id"
        field_attribute_lookup["Model_Alteration_file"] = "model_alteration_file"
        field_attribute_lookup["Project_Num"] = "project_num"
        field_attribute_lookup["Shape@"] = "model_geometry"
        return field_attribute_lookup
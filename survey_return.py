from config import Config
from generic_object import GenericObject
from collections import OrderedDict

try:
    from typing import List, Any
except:
    pass

class SurveyReturn(GenericObject):

    def __init__(self, config):
        # type: (Config) -> None
        self.id = 0
        self.parent_model_id = 0
        self.survey_return_path = None


    #TODO - don't know if I need field_attr_lookup
    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Survey_Return_ID"] = "id"
        field_attribute_lookup["Survey_Name"] = "survey_name"
        field_attribute_lookup["Survey_Date"] = "survey_date"
        field_attribute_lookup["Project_Number"] = "project_number"
        field_attribute_lookup["Raw_Survey_Path"] = "raw_survey_path"
        return field_attribute_lookup

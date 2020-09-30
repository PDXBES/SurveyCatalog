import arcpy
import sys

try:
    from typing import List, Any
except:
    pass

from survey_return import SurveyReturn
from survey_return_data_io import SurveyReturnDataIo
from config import Config
from db_data_io import DbDataIo


class SurveyCatalogDbDataIo(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.current_id_database_table_path = self.config.survey_catalog_current_id_table_path
        self.workspace = "in_memory"

    # NOT USED AS FAR AS I CAN TELL
    #def retrieve_current_model_id(self):
    #    current_model_id = self.retrieve_current_id(SurveyReturn)
    #    return current_model_id

    def add_survey(self, survey_return, survey_return_data_io):
        # type: (SurveyReturn, SurveyReturnDataIo) -> None

        editor = survey_return_data_io.start_editing_session(self.config.survey_catalog_database)
        try:

            # append to SurveyTracking
            self.append_object_to_db(survey_return,
                                     SurveyReturn.input_field_attribute_lookup(),
                                     self.config.survey_tracking_path,
                                     self.config.survey_tracking_path)
            # append to SurveyPoints
            survey_return_data_io.append_survey_return(survey_return)

            survey_return_data_io.stop_editing_session(editor, True)
        except:
            survey_return_data_io.stop_editing_session(editor, False)
            arcpy.AddMessage("DB Error while adding model. Changes rolled back.")
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])
            arcpy.AddMessage(e.args[1])
            arcpy.AddMessage(e.args[2])


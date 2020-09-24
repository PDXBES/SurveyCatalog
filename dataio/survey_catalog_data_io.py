
try:
    from typing import List, Any
except:
    pass

from businessclasses.survey_return import SurveyReturn
from dataio.survey_data_io import SurveyDataIo
from businessclasses.config import Config
from dataio.db_data_io import DbDataIo


class SurveyCatalogDbDataIo(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.current_id_database_table_path = self.config.survey_catalog_current_id_table_path
        self.workspace = "in_memory"

    def retrieve_current_model_id(self):
        current_model_id = self.retrieve_current_id(SurveyReturn)
        return current_model_id

    def add_model(self, survey_return, survey_data_io):
        # type: (SurveyReturn, SurveyDataIo) -> None

        # append to SurveyTracking
        self.append_object_to_db(survey_return, SurveyReturn.input_field_attribute_lookup(), self.config.survey_tracking_path,
                                 self.config.survey_tracking_path)
        # append to MappedSurveyNodes
        survey_data_io.append_model_network(survey_return)

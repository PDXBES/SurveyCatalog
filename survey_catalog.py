try:
    from typing import List, Any
except:
    pass

from config import Config
from survey_return import SurveyReturn
#from dataio.survey_catalog_data_io import SurveyCatalogDbDataIo


class SurveyCatalog:
    survey_returns = None  # type: List[SurveyReturn]

    def __init__(self, config):
        # type: (Config) -> None
        self.survey_returns = []
        self.config = config

    def add_survey_return(self, survey_return):
        # type: (SurveyReturn) -> None
        self.check_for_duplicate_survey_return(survey_return)
        #self.check_for_valid_model(survey_return)
        self.survey_returns.append(survey_return)

    def check_for_duplicate_survey_return(self, model):
        # type: (SurveyReturn) -> None
        if model in self.survey_returns:
            raise Exception



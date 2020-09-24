try:
    from typing import List, Any
except:
    pass

from config import Config
#from dataio.survey_catalog_data_io import SurveyCatalogDbDataIo


class SurveyCatalog:
    returns = None  # type: List[SurveyReturn]

    def __init__(self, config):
        # type: (Config) -> None
        self.survey_returns = []
        self.config = config





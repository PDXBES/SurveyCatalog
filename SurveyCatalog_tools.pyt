import arcpy
#from survey_return import SurveyReturn
from survey_catalog import SurveyCatalog
from survey_return import SurveyReturn
from survey_catalog_data_io import SurveyCatalogDbDataIo
from survey_return_data_io import SurveyReturnDataIo

from config import Config
#from dataio import utility
#from dataio.utility import Utility
#from businessclasses import config

#reload(arcpy)
#reload(config)
#reload(utility)


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Survey Catalog Tools"
        self.alias = "Survey Catalog Tools"

        # List of tool classes associated with this toolbox
        self.tools = [Survey_Registration]

class Survey_Registration(object):
    def __init__(self):
        self.label = "Survey Registration"
        self.description = "Tool for geocoding, formatting and registering raw survey returns"
        self.config = Config()
        self.survey_catalog = SurveyCatalog(self.config)
        self.survey_catalog_data_io = SurveyCatalogDbDataIo(self.config)
        self.survey_return_data_io = SurveyReturnDataIo(self.config, self.survey_catalog_data_io)
        #self.utility = utility.Utility()

        arcpy.AddMessage("Init")

#        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        arcpy.AddMessage("Get parameter info")

        survey_directory = arcpy.Parameter(
            displayName="Survey Directory",
            name="survey_directory",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        survey_directory.filter.list = ["File System", "Local Database"]

        params = [survey_directory]

        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed.
        Where we put the logic in to enable/disable fields
        """
        arcpy.AddMessage("Update Parameters")

        survey_path_parameter = parameters[0]

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

#should validate the parent model id before we run execute
    def execute(self, parameters, messages):
        arcpy.AddMessage("Execute")

        self.survey_return = SurveyReturn.initialize_with_current_id(self.config, self.survey_catalog_data_io)
        self.survey_return.parent_model_id = 0

        survey_path_parameter = parameters[0]

        self.survey_return.survey_return_path = survey_path_parameter

        self.survey_catalog.add_survey(self.survey_return)

        EMGAATS_Survey_Registration_function(self.survey_catalog, self.config)


def EMGAATS_Survey_Registration_function(survey_catalog, config):
    # type: (SurveyCatalog, Config) -> None
    survey_catalog_data_io = SurveyCatalogDbDataIo(config)
    survey_return_data_io = SurveyReturnDataIo(config, survey_catalog_data_io)
    survey_return = survey_catalog.survey_returns[0]
    try:
        arcpy.AddMessage("Adding Survey...")



        survey_catalog_data_io.add_survey(survey_return, survey_return_data_io)
        arcpy.AddMessage("Survey Added")
    except:
        arcpy.AddError("Survey could not be registered")
        arcpy.ExecuteError()



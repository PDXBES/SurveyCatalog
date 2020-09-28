#-------------------------------------------------------------------------------
# Name:        survey_notes_formatter
# Purpose:     to format notes
#
# Created:     28/07/2020
# Copyright:   IMS - M&GIS 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import sys
import os
import config_orig


# ----------------------------------------------------------------------------------------------

def list_field_names(input_fc):
    field_names = []
    fields = arcpy.ListFields(input_fc)
    for field in fields:
        field_names.append(field.name)
    return field_names

def start_editing_session(workspace_path):
    editor = arcpy.da.Editor(workspace_path)
    editor.startEditing(False, True)
    editor.startOperation()
    return editor

def stop_editing_session(workspace_editor, save_changes):
    workspace_editor.stopOperation()
    workspace_editor.stopEditing(save_changes)

def retrieve_current_id(self, object_type):
    # type: (GenericObject) -> int
    current_id = self._retrieve_block_of_ids(object_type, 1)
    return current_id

def _retrieve_block_of_ids(self, object_type, number_of_ids):
    if number_of_ids > 0:
        field_names = ["Object_Type", "Current_ID"]
        cursor = arcpy.da.UpdateCursor(config_orig.survey_catalog_current_id_table_path, field_names)
        for row in cursor:
            object_name, current_id = row
            if object_type.__name__ == object_name:
                next_id = current_id + number_of_ids
                break
        cursor.updateRow([object_name, next_id])
        del cursor
    else:
        raise Exception()
    return current_id

def add_parent_id(self, in_memory_table, parent_id_field, parent_id):
    arcpy.AddField_management(in_memory_table, parent_id_field, "LONG")
    arcpy.CalculateField_management(in_memory_table, parent_id_field, parent_id, "PYTHON_9.3")

def add_ids(self, in_memory_table, unique_id_field, object_type):
    number_of_ids = int(arcpy.GetCount_management(in_memory_table)[0])
    current_id = self._retrieve_block_of_ids(object_type, number_of_ids)
    next_id = current_id + number_of_ids
    arcpy.AddField_management(in_memory_table, unique_id_field, "LONG")
    cursor = arcpy.da.UpdateCursor(in_memory_table, unique_id_field)
    for row in cursor:
        if current_id == next_id:
            raise Exception
        row[0] = current_id
        cursor.updateRow(row)
        current_id += 1
    del cursor

# TODO - need to assign universal unique IDs to all survey records
# TODO - need to assign unique IDs to each survey session (put in SurveyTracking)

# SurveyPoints part ----------------------------------------------

def geocode_survey_file(survey_file):
    try:
        xy_event = arcpy.MakeXYEventLayer_management(survey_file, "Field3", "Field2", "in_memory\survey_data", config_orig.OCRS_sp_ref)
    except:
        xy_event = arcpy.MakeXYEventLayer_management(survey_file, "Easting", "Northing", "in_memory\survey_data", config_orig.OCRS_sp_ref)
    arcpy.Delete_management(os.path.join(config_orig.temp_working_gdb, "survey_xy")) #if file DNE this just moves on - nice
    survey_xy = arcpy.FeatureClassToFeatureClass_conversion(xy_event, config_orig.temp_working_gdb, "survey_xy")
    return survey_xy

def add_notes_fields(input_fc):

        # note - when field already exists method just moves on

        arcpy.AddField_management(input_fc, "Point", "LONG")

        arcpy.AddField_management(input_fc, "Northing", "DOUBLE")

        arcpy.AddField_management(input_fc, "Easting", "DOUBLE")

        arcpy.AddField_management(input_fc, "Rim_Elevation", "DOUBLE")

        arcpy.AddField_management(input_fc, "Notes", "TEXT", "", "", 250)

        arcpy.AddField_management(input_fc, "UnitID", "TEXT", "", "", 6)

        arcpy.AddField_management(input_fc, "X_Section", "TEXT", "", "", 6)

        arcpy.AddField_management(input_fc, "P_Code", "TEXT", "", "", 6)

        arcpy.AddField_management(input_fc, "BES_Code", "TEXT", "", "", 15)

        arcpy.AddField_management(input_fc, "Description", "TEXT", "", "", 60)

        arcpy.AddField_management(input_fc, "Material", "TEXT", "", "", 10)

        arcpy.AddField_management(input_fc, "Other", "TEXT", "", "", 60)

        arcpy.AddField_management(input_fc, "Final_Code", "TEXT", "", "", 10)

        arcpy.AddField_management(input_fc, "Gen_Code", "TEXT", "", "", 10)

def calc_standard_fields(input_fc):
    for item in config_orig.field_lookup.items():
        if item[0] in list_field_names(input_fc):
            with arcpy.da.UpdateCursor(input_fc, [item[0], item[1]]) as cursor:
                for row in cursor:
                    if row[0] is not None:
                        row[1] = row[0]
                    cursor.updateRow(row)

def calc_fields_from_notes(input_fc):

    # going to assume that raw txt are using or have been formatted to use real field names

    with arcpy.da.UpdateCursor(input_fc, config_orig.notes_fields) as cursor:
        for row in cursor:
            otherlist = []
            for item in row[0].split(" "):
                if len(item) == 6 and item[:3].isalpha() and item[3:].isdigit():
                    row[1] = item
                elif item[:2] == "BL" and item[2:].isdigit():
                    row[2] = item
                elif item in config_orig.P_code.keys():
                    row[3] = item
                    row[4] = config_orig.P_code[item]
                elif item in config_orig.BES_list.keys(): # need to account for multiple?
                    row[5] = item
                    row[4] = config_orig.BES_list[item]
                elif item in config_orig.Material_list:
                    row[6] = item
                else:
                    if item != " " and item is not None:
                        otherlist.append(str(item))
            if len(otherlist) != 0:
                row[7] = str(otherlist).strip('[]')
            cursor.updateRow(row)

def calc_final_field(input_fc):
    with arcpy.da.UpdateCursor(input_fc, ["P_Code", "BES_Code", "Final_Code"]) as cursor:
        for row in cursor:
            if row[0] != None:
                row[2] = row[0]
            else:
                 row[2] = row[1]
            cursor.updateRow(row)

# def calc_unitID_for_low_point(input_fc):

# on hold until I can work out the logic

#     with arcpy.da.UpdateCursor(input_fc, ["X_Section", "Final_Code", "UnitID"]) as cursor:
#         for row in cursor:
#             pass

# -----------------------------------------------------------------------

# SurveyTracking part -------------------------------------------

def survey_file_name_date(survey_file):
    # assumes they keep naming the file using same format - super fragile
    date = os.path.basename(survey_file).split(" ")[0]
    return date

def survey_file_name_project_number(survey_file):
    # assumes they keep naming the file using same format - super fragile
    project_number = os.path.basename(survey_file).split(" ")[1][:5]
    return project_number

def survey_file_name_survey_name(survey_file):
    # assumes they keep naming the file using same format - super fragile
    proj_no = survey_file_name_project_number(survey_file)
    survey_name = os.path.basename(input).split(".")[0].partition(proj_no)[2]
    return survey_name

def insert_tracking_values(tracking_file, survey_file):
    cursor = arcpy.da.InsertCursor(tracking_file, ["Survey_Name", "Survey_Date", "Project_Number", "Raw_Survey_Path"])
    cursor.insertRow((survey_file_name_survey_name(survey_file),
                      survey_file_name_date(survey_file),
                      survey_file_name_project_number(survey_file),
                      survey_file))
    del cursor


# Main -----------------------------------------------------------

def register_survey_notes(survey_file):
    print "Starting Survey Notes Registration..."

    editor = start_editing_session(config_orig.survey_catalog_database)

    try:
        print "Geocoding survey file"
        survey_xy = geocode_survey_file(survey_file)

        print "Adding notes fields"
        add_notes_fields(survey_xy)

        print "Filling standard fields (if needed)"
        calc_standard_fields(survey_xy)

        if all(item in list_field_names(survey_xy) for item in config_orig.notes_fields):
            print "Parsing/ filling notes fields"
            calc_fields_from_notes(survey_xy)
        else:
            Exception()
            print "Required fields are missing!"

        print "Filling Final_Code field"
        calc_final_field(survey_xy)

        print "Appending result to SurveyPoints"
        arcpy.Append_management(survey_xy, config_orig.survey_points_path, "NO_TEST")

        print "Inserting values into SurveyTracking"
        insert_tracking_values(config_orig.survey_tracking_path, survey_file)

        print "...Survey Notes Registration Finished"

        stop_editing_session(editor, True)
    except:
        stop_editing_session(editor, False)
        arcpy.AddMessage("DB Error while adding survey. Changes rolled back.")
        e = sys.exc_info()[1]
        arcpy.AddMessage(e.args[0])
        arcpy.AddMessage(e.args[1])
        arcpy.AddMessage(e.args[2])


# ------ for testing/ running ----------------------------

raw_return_folder = r"\\besfile1\asm_projects\E11098_Council_Crest\survey\mgmt_process\data\survey_raw"
file = r"2020-08-13 11098GF COUNCIL SMK.txt"
input = os.path.join(raw_return_folder, file)
register_survey_notes(input)

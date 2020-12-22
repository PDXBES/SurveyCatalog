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


def retrieve_current_id(object_type):
    current_id = _retrieve_block_of_ids(object_type, 1)
    return current_id


def _retrieve_block_of_ids(object_type, number_of_ids):
    current_id = ""
    if number_of_ids > 0:
        field_names = ["Object_Type", "Current_ID"]
        cursor = arcpy.da.UpdateCursor(config_orig.survey_catalog_current_id_table_path, field_names)
        for row in cursor:
            object_name, row_current_id = row
            if object_type == object_name:
                current_id = row_current_id
                next_id = row_current_id + number_of_ids
                #break
                cursor.updateRow([object_name, next_id])
        del cursor
    else:
        raise Exception()
    return current_id


def add_ids(in_memory_table, unique_id_field, object_type):
    number_of_ids = int(arcpy.GetCount_management(in_memory_table)[0])
    current_id = _retrieve_block_of_ids(object_type, number_of_ids)
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


def survey_return_already_registered(survey_file):
    already_registered = False
    with arcpy.da.SearchCursor(config_orig.survey_tracking_path, "Raw_Survey_Path") as cursor:
        for row in cursor:
            if row[0] == survey_file:
                already_registered = True
    return already_registered


def survey_return_exists(survey_file):
    exists = False
    if os.path.exists(survey_file):
        exists = True
    return exists


def survey_return_is_valid(survey_file):
    valid = False
    if survey_return_already_registered(survey_file) is False and survey_return_exists(survey_file):
        valid = True
    return valid


def add_long_field(input_fc, field_name):
    if field_name not in list_field_names(input_fc):
        arcpy.AddField_management(input_fc, field_name, "LONG")


def add_double_field(input_fc, field_name):
    if field_name not in list_field_names(input_fc):
        arcpy.AddField_management(input_fc, field_name, "DOUBLE")


def add_text_field(input_fc, field_name, length):
    if field_name not in list_field_names(input_fc):
        arcpy.AddField_management(input_fc, field_name, "TEXT", "", "", length)

# SurveyPoints part ----------------------------------------------

def geocode_survey_file(survey_file):
    try:
        xy_event = arcpy.MakeXYEventLayer_management(survey_file, "Field3", "Field2", "in_memory\survey_data", config_orig.OCRS_sp_ref)
    except:
        xy_event = arcpy.MakeXYEventLayer_management(survey_file, "Easting", "Northing", "in_memory\survey_data", config_orig.OCRS_sp_ref)
    arcpy.Delete_management(os.path.join(config_orig.temp_working_gdb, "survey_xy")) #if file DNE this just moves on - nice
    survey_xy = arcpy.FeatureClassToFeatureClass_conversion(xy_event, config_orig.temp_working_gdb, "survey_xy")
    return survey_xy


def add_required_fields(input_fc):

        # note - when field already exists method just moves on - APPARENTLY NOT TRUE

        add_long_field(input_fc, "Survey_Return_ID")

        add_long_field(input_fc, "Survey_Point_ID")

        add_long_field(input_fc, "Point")

        add_double_field(input_fc, "Northing")

        add_double_field(input_fc, "Easting")

        add_double_field(input_fc, "Rim_Elevation")

        add_text_field(input_fc, "Notes", 250)

        add_text_field(input_fc, "UnitID", 6)

        add_text_field(input_fc, "X_Section", 6)

        add_text_field(input_fc, "P_Code", 6)

        add_text_field(input_fc, "BES_Code", 15)

        add_text_field(input_fc, "Description", 60)

        add_text_field(input_fc, "Material", 10)

        add_text_field(input_fc, "Other", 60)

        add_text_field(input_fc, "Final_Code", 10)

        add_text_field(input_fc, "Gen_Code", 10)


def calc_survey_return_id_field(input_fc, current_id):
    with arcpy.da.UpdateCursor(input_fc, "Survey_Return_ID") as cursor:
        for row in cursor:
            row[0] = current_id
            cursor.updateRow(row)


def calc_standard_fields(input_fc):
    for item in config_orig.field_lookup.items():
        if item[0] in list_field_names(input_fc):
            with arcpy.da.UpdateCursor(input_fc, [item[0], item[1]]) as cursor:
                for row in cursor:
                    if row[0] is not None:
                        if "_REF" not in str(row[0]):
                            row[1] = row[0]
                    cursor.updateRow(row)

def point_field_cleanup(input_fc):
    with arcpy.da.UpdateCursor(input_fc, "Point") as cursor:
        for row in cursor:
            if "_REF" in str(row[0]):
                cursor.deleteRow()

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

# SurveyTracking part -------------------------------------------

def survey_file_base_name(survey_file):
    base_name = os.path.basename(input).split(".")[0]
    return base_name


def split_base_name(survey_file):
    split_name = survey_file_base_name(survey_file).split(" ")
    return split_name


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def survey_file_name_date(survey_file):
    # assumes they keep naming the file using same format - super fragile
    date = split_base_name(survey_file)[0]
    return date


def survey_file_name_project_number(survey_file):
    # assumes they keep naming the file using same format - super fragile
    project_number = split_base_name(survey_file)[1][:5]
    return project_number


def survey_file_name_survey_name(survey_file):
    # assumes they keep naming the file using same format - super fragile
    survey_name = find_between(survey_file_base_name(survey_file),
                               survey_file_name_project_number(survey_file),
                               survey_file_name_user_initials(survey_file))
    return survey_name.strip()


def survey_file_name_user_initials(survey_file):
    # assumes they keep naming the file using same format - super fragile
    user_initials = split_base_name(survey_file)[-1]
    return user_initials


def insert_tracking_values(tracking_file, survey_file, current_id):
    cursor = arcpy.da.InsertCursor(tracking_file, ["Survey_Return_ID", "Survey_Name", "Survey_Date", "Project_Number", "Raw_Survey_Path", "Surveyor"])
    cursor.insertRow((current_id,
                      survey_file_name_survey_name(survey_file),
                      survey_file_name_date(survey_file),
                      survey_file_name_project_number(survey_file),
                      survey_file,
                      survey_file_name_user_initials(survey_file)
                      ))
    del cursor


# Main -----------------------------------------------------------


def register_survey_notes(survey_file):

    current_id = retrieve_current_id("Survey_Return")

    print "Starting Survey Notes Registration..."

    if survey_return_is_valid(survey_file):

        editor = start_editing_session(config_orig.survey_catalog_database)

        try:
            print "Geocoding survey file"
            survey_xy = geocode_survey_file(survey_file)

            print "Adding required fields"
            add_required_fields(survey_xy)

            print "Assigning IDs to the Survey Points"
            add_ids(survey_xy, "Survey_Point_ID", "Survey_Point")
            calc_survey_return_id_field(survey_xy, current_id)

            print "Filling standard fields (if needed)"
            calc_standard_fields(survey_xy)

            print "Point field cleanup (if needed)"
            point_field_cleanup(survey_xy)

            if all(item in list_field_names(survey_xy) for item in config_orig.notes_fields):
                print "Parsing/ filling notes fields"
                calc_fields_from_notes(survey_xy)
            else:
                Exception()
                print "Required fields are missing!"

            print "Filling Final_Code field"
            calc_final_field(survey_xy)

            print "Appending survey to SurveyPoints"
            arcpy.Append_management(survey_xy, config_orig.survey_points_path, "NO_TEST")

            print "Inserting values into SurveyTracking"
            insert_tracking_values(config_orig.survey_tracking_path, survey_file, current_id)

            print "...Survey Notes Registration Finished"

            stop_editing_session(editor, True)
        except:
            stop_editing_session(editor, False)
            arcpy.AddMessage("DB Error while adding survey. Changes rolled back.")
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])
            arcpy.AddMessage(e.args[1])
            arcpy.AddMessage(e.args[2])
    else:
        print "Problem with the input survey file"
        print "No survey will be registered"




# ------ for testing/ running ----------------------------

raw_return_folder = r"\\besfile1\asm_projects\E11098_Council_Crest\survey\mgmt_process\data\survey_raw"

#file = r"2020-07-23 11098GD ADJ CAB EDIT SMK.txt"
#file = r"2020-07-24 11098GB COUNCIL GPS ADJ SMK.txt"
#file = r"2020-07-24 11098GE COUNCIL SMK.txt"
#file = r"2020-06-12 11098 Dosch Ditches and Inlets Test SMK.txt"
#file = r"2020-08-13 11098GC COUNCIL SMK.txt"
#file = r"2020-08-13 11098GF COUNCIL SMK.txt"

#file = r"2020-12-14 11098GG COUNCIL SMK.txt"
#file = r"2020-12-18 11098GH COUNCIL SMK.txt"
file = r"2020-12-18 11098GI COUNCIL SMK.txt"


input = os.path.join(raw_return_folder, file)
register_survey_notes(input)

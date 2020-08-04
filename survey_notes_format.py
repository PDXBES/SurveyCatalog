#-------------------------------------------------------------------------------
# Name:        survey_notes_formatter
# Purpose:
#
# Author:      dashney
#
# Created:     28/07/2020
# Copyright:   (c) dashney 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
from businessclasses import config


# ----------------------------------------------------------------------------------------------

def list_field_names(input_fc):
    field_names = []
    fields = arcpy.ListFields(input_fc)
    for field in fields:
        field_names.append(field.name)
    return field_names

# TODO - need to assign universal unique IDs to all survey records
# TODO - need to assign unique IDs to each survey session (put in SurveyTracking)

def geocode_survey_file(survey_file):
    try:
        xy_event = arcpy.MakeXYEventLayer_management(survey_file, "Field3", "Field2", "in_memory\survey_data", config.OCRS_sp_ref)
    except:
        xy_event = arcpy.MakeXYEventLayer_management(survey_file, "Easting", "Northing", "in_memory\survey_data", config.OCRS_sp_ref)
    arcpy.Delete_management(os.path.join(config.temp_working_gdb, "survey_xy"))
    survey_xy = arcpy.FeatureClassToFeatureClass_conversion(xy_event, config.temp_working_gdb, "survey_xy")
    return survey_xy

def add_notes_fields(input_fc):

        # note - when field already exists method just moves on

        arcpy.AddField_management(input_fc, "UnitID", "TEXT", "", "", 6)

        arcpy.AddField_management(input_fc, "X_Section", "TEXT", "", "", 6)

        arcpy.AddField_management(input_fc, "P_Code", "TEXT", "", "", 6)

        arcpy.AddField_management(input_fc, "Description", "TEXT", "", "", 60)

        arcpy.AddField_management(input_fc, "BES_Code", "TEXT", "", "", 15)

        arcpy.AddField_management(input_fc, "Material", "TEXT", "", "", 10)

        arcpy.AddField_management(input_fc, "Other", "TEXT", "", "", 60)

        arcpy.AddField_management(input_fc, "Final_Code", "TEXT", "", "", 10)

        arcpy.AddField_management(input_fc, "Gen_Code", "TEXT", "", "", 10)


def calc_fields_from_notes(input_fc):

    # going to assume that raw txt are using or have been formatted to use real field names

    config.notes_fields.insert(0, "Notes")

    with arcpy.da.UpdateCursor(input_fc, config.notes_fields) as cursor:
        for row in cursor:
            otherlist = []
            for item in row[0].split(" "):
                if len(item) == 6 and item[:3].isalpha() and item[3:].isdigit():
                    row[1] = item
                elif item[:2] == "BL" and item[2:].isdigit():
                    row[2] = item
                elif item in config.P_code.keys():
                    row[3] = item
                    row[4] = confignotes_fields.insert(0, "Notes").P_code[item]
                elif item in config.BES_list.keys(): # need to account for multiple?
                    row[5] = item
                    row[4] = config.BES_list[item]
                elif item in config.Material_list:
                    row[6] = item
                else:
                    if item != " " and item != None:
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

# on hold until I can work out the logic
def calc_unitID_for_low_point(input_fc):
    with arcpy.da.UpdateCursor(input_fc, ["X_Section", "Final_Code", "UnitID"]) as cursor:
        for row in cursor:
            pass
def format_survey_notes(input_fc):
    print "Starting Survey Notes Formatter..."

    print "Geocoding survey file"
    survey_xy = geocode_survey_file(input_fc)

    print "Adding new fields"
    add_notes_fields(survey_xy)

    if all(item in list_field_names(survey_xy) for item in notes_fields):
        print "Parsing fields"
        calc_fields_from_notes(survey_xy)
    else:
        Exception
        print "Required fields are missing!"
    print "Filling Final_Code field"
    calc_final_field(survey_xy)

    print "Appending result to MappedSurvey"
    arcpy.Append_management(survey_xy, config.mapped_survey, "NO_TEST") # not sure if this works as is

    print "...Survey Notes Formatter Finished"

# ------ for testing/ running ----------------------------
gdb = r"\\besfile1\asm_projects\E11098_Council_Crest\survey\mgmt_process\data\survey_dev_testing.gdb"
fc = r"survey_11098GD_20200723"
input = os.path.join(gdb, fc)
format_survey_notes(input)

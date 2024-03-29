#-------------------------------------------------------------------------------
# Name:        config
# Purpose:
#
# Author:      dashney
#
# Created:     31/07/2020
# Copyright:   (c) dashney 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import os

# file refs #
survey_data = r"\\besfile1\ISM_PROJECTS\Planning_Survey\data"
raw_data = os.path.join(survey_data, "survey_raw")
#survey_catalog_database = r"\\besfile1\asm_projects\E11098_Council_Crest\survey\mgmt_process\data\Survey_Catalog.gdb"
survey_catalog_database = os.path.join(survey_data, "Survey_Catalog.gdb")
survey_tracking_path = os.path.join(survey_catalog_database, "SurveyTracking")
survey_points_path = os.path.join(survey_catalog_database, "SurveyPoints")
survey_catalog_current_id_table_path = os.path.join(survey_catalog_database, "Current_ID")
temp_working_gdb = r"C:\temp\SurveyCatalog_working.gdb"
OCRS_sp_ref = os.path.join(survey_data, "OCRS Portland NAD 1983 (2011) LCC (Intl Feet).prj")


# list of values that we want to capture but that are not in the P code (but maybe should be?)
BES_dict = {"CROWN": "Crown", "THALWAG": "Thalweg", "THALWEG": "Thalweg", "TR": "Trash Rack",
            "SNF": "Searched Not Found"}

Material_list = ["DIRT", "GRAVEL"]

#notes_fields = ["Notes", "P_Code", "BES_Code", "Description", "X_Section", "Material", "Other"]
# the old one
notes_fields = ["Notes", "Unit_ID", "X_Section", "P_Code", "Description", "BES_Code", "Material", "Other"]


# current structure of EJs survey return txt file
#field_lookup = {
#"Field1" : "Point",
#"Field2" : "Northing",
#"Field3" : "Easting",
#"Field4" : "Rim_Elevation",
#"Field5" : "Notes1",
#"Field6" : "Unit_ID",
#"Field7" : "Notes2"
#}

# the old one
field_lookup = {
"Field1" : "Point",
"Field2" : "Northing",
"Field3" : "Easting",
"Field4" : "Rim_Elevation",
"Field5" : "Notes1"
}

# P codes provided by PBOT
# prob better if read in from a file
P_code_dict = {
'AHEAD' : '"AHEAD" - Text',
'AL' : 'Arrow - Left Turn',
'AR' : 'Arrow - Right Turn',
'AS' : 'Arrow - Straight',
'ASL' : 'Arrow - Straight and Left',
'ASR' : 'Arrow - Straight and Right',
'ASS' : 'Arrow - Straight (Small)',
'BB' : 'Circular Bike Boulevard Marker',
'BDOH' : 'BuilDing OverHang',
'BH' : 'BoreHole',
'BIKE' : 'BIKE Rack',
'BKR' : 'BiKeR Symbol',
'BL' : 'Break Line',
'BLDG' : 'BuiLDinG Line',
'BLP' : 'Bike Signal LooP',
'BM' : 'BenchMark',
'BOL' : 'BOLlard / Post',
'BSCH' : 'Back Sight CHeck',
'BUS' : '"BUS" - Text',
'CBX' : 'Communications BoX - Below Ground',
'CCB' : 'Communications CaBinet - Above Ground',
'CGUT' : 'Combination Curb/GUTter - Edge of Concrete in Street',
'CLB' : 'Crosswalk "Ladder" Style Boundary',
'CLR' : 'CLeaRance of Bridge',
'CMH' : 'Communications ManHole',
'CO' : 'CleanOut',
'COL' : 'COLumn',
'COM' : 'COMmunications Line',
'CP' : 'Control Point',
'CR' : 'Curb Ramp',
'CRB' : 'CuRB - Top Back',
'CRBE' : 'CuRB - Extruded',
'CRBRD' : 'Roof Drain at Curb',
'CRSR' : 'Communications RiSeR - Above Ground',
'CVT' : 'Communications VaulT - Below Ground',
'CWM' : 'Com Line Warning Marker',
'DCL' : 'Ditch CenterLine',
'DF' : 'Drinking/Water Fountain',
'DIA' : 'DIAmond Symbol',
'DOOR' : 'DOOR',
'DSPT' : 'DownSPouT',
'DWY' : 'DriveWaY',
'DY' : 'Double Yellow - Solid (4")',
'EAC' : 'Edge of AC',
'EB' : 'Edge of Brush/Vegetation',
'EBG' : 'Edge of BridGe',
'EBR' : 'Edge of BRick',
'ECC' : 'Edge of ConCrete',
'EGL' : 'Edge of GraveL',
'EGS' : 'Edge of GrasS',
'EL' : 'Elevation Shot',
'ERK' : 'Edge of RocK',
'EW' : 'Edge of Water',
'EWL' : 'Edge of WeTLand',
'FCL' : 'FenCe Line',
'FDC' : 'Fire Department Connection',
'FF' : 'Fuel Filler Cap',
'FFE' : 'First Floor Elevation - no Basement',
'FFEB' : 'First Floor Elevation - with Basement',
'FH' : 'Fire Hydrant',
'FO' : 'FiberOptic Line',
'GL' : 'Gas Line',
'GM' : 'Gas Meter',
'GPS' : 'GPS Point',
'GPST' : 'GatePoST',
'GR' : 'Guard Rail / Hand Rail',
'GRSR' : 'Gas RiSeR - Above Ground',
'GRT' : 'GRaTe - Irregular Field Inlet / Strip Drain (draw line)',
'GUT' : 'GUTter',
'GUY' : 'GUY Anchor',
'GV' : 'Gas Valve',
'GVT' : 'Gas VaulT - Below Ground',
'GWM' : 'Gas Warning  Marker',
'HEDG' : 'HEDGe',
'HORS' : 'HORSe Ring',
'HUMP' : 'Speed HUMP Outline',
'IE' : 'Invert Elevation of Pipe',
'INBE' : 'INlet - BEehive',
'INEE' : 'INlet - Double (End to End)',
'INF' : 'INlet - Field - Square/Rectangular',
'INR' : 'INlet - Field - Round',
'INSG' : 'INlet - Standard LarGer New Style',
'INSS' : 'INlet - Double (Side by Side)',
'INST' : 'INlet - STandard - Smaller Old Style',
'INSW' : 'INlet - Recessed Under SideWalk',
'IRBX' : 'IRrigation BoX - Below Ground',
'IRRSR' : 'IRrigation RiSeR - Above Ground',
'JBX' : 'Junction BoX',
'LID' : 'Sewer MH LID',
'LIM' : 'LIMit of Topo Boundary',
'LIP' : 'LIP of Driveway',
'LOOPD' : 'Traffic Control LOOP - Diamond',
'LOOPR' : 'Traffic Control LOOP - Round',
'MBX' : 'MailBoX',
'MON' : 'MONument for Property',
'MTR' : 'MoniToRing Point',
'OH' : 'OverHead Wire',
'ONLYB' : '"ONLY" - Text (Big)',
'ONLYS' : '"ONLY" - Text (Small)',
'PBX' : 'Power BoX - Below Ground',
'PCB' : 'Power CaBinet - Above Ground',
'PED' : 'PEDestrian Signal Pole',
'PIEZ' : 'PIEZometer',
'PKBN' : 'ParK BeNch',
'PKL' : 'ParKing Stall Marker - "L"',
'PKM' : 'ParKing Meter',
'PKP' : 'ParKing Stall Marker - "+"',
'PKT' : 'ParKing Stall Marker - "T"',
'PLAY' : 'PLAY Equipment',
'PLTG' : 'PLanTinG Box - Edge',
'PM' : 'Power Meter',
'PMH' : 'Power ManHole',
'PO' : 'POle (Wires, no Light)',
'POL' : 'POle (Wires and Light)',
'PRSR' : 'Power RiSeR - Above Ground',
'PVT' : 'Power VaulT - Below Ground',
'PWM' : 'Power Warning  Marker',
'PWR' : 'PoWeR Line',
'RP' : 'Reference Point',
'RRCB' : 'RailRoad CaBinet',
'RROH' : 'RailRoad Crossing Signal OverHead',
'RRSW' : 'RailRoad SWitch',
'RRT' : 'RailRoad Track',
'RRWL' : 'RailRoad Warning Light (Crossing)',
'RXR' : 'Railroad Crossing Symbol',
'SCH' : '"SCHool" - Text',
'SDLY' : 'Striping - Double  - Dashed / SoLid Yellow (4")',
'SDMW' : 'Striping - Dashed Medium White (8")',
'SDW' : 'Striping - Dashed White (4")',
'SDY' : 'Striping - Dashed Yellow (4")',
'SED' : 'SEDimentary Manhole',
'SEW' : 'SEWer Line - Sanitary/Combination',
'SHAR' : 'Bike Blvd Marker w/ double arrow',
'SHMP' : 'Speed HuMP Pavement Marker',
'SHR' : 'SHRub',
'SIGN' : 'SIGN',
'SL' : 'Street Light  (No Wires)',
'SMH' : 'Sanitary/Combination ManHole',
'SPH' : 'SPrinkler Head',
'SSLW' : 'Striping - Solid Large White (12")',
'SSMW' : 'Striping - Solid Medium White (8")',
'SSW' : 'Striping - Solid White (4")',
'SSXLW' : 'Striping - Solid EXtra Large White (24")',
'SSY' : 'Striping - Solid Yellow (4")',
'STM' : 'STorM Line',
'STMH' : 'STorm ManHole',
'STOP' : '"STOP" - Text',
'STUM' : 'STUMp',
'STWY' : 'STairWaY',
'SUMP' : 'SUMP Manhole',
'TFC' : 'Top Face of Curb',
'TLW' : 'Traffic Loop Wire',
'TOES' : 'TOE of Slope',
'TOPPI' : 'TOP of PIpe',
'TOPS' : 'TOP of Slope',
'TRCB' : 'TRaffic CaBinet',
'TRD' : 'TRee - Deciduous',
'TRE' : 'TRee - Evergreen',
'TRPL' : 'TRaffic Signal PoLe',
'TRRK' : 'TRash RacK',
'UCB' : 'Unknown CaBinet - Above Ground',
'UMH' : 'Unknown ManHole',
'URSR' : 'Unknown RiSeR - Above Ground',
'UV' : 'Unknown Valve or Junction Box - Below Ground',
'UVT' : 'Unknown VaulT - Below Ground',
'WB' : 'Wall - Top Back',
'WF' : 'Wall - Bottom Face',
'WKB' : 'SideWalK - Back',
'WKF' : 'SideWalK - Front',
'WL' : 'Water Line',
'WM' : 'Water Meter',
'WMH' : 'Water ManHole',
'WP' : 'Working Point',
'WRSR' : 'Water RiSeR / Stand Pipe - Above Ground',
'WV' : 'Water Valve',
'WVT' : 'Water VaulT - Below Ground',
'WWM' : 'Water Warning Marker',
'XING' : '"XING" - Text',
'YL' : 'Yard Light',
'Z' : 'Impact Attenuator'
}


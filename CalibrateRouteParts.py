

'''
Created on Feb 20, 2019
tool to correctly order and measure multipart routes in roads and highways
for the KDOT target network local roads 
end dates ~99K calibration points and results in ~158K new calibration points with incremented gaps
\\GISDATA\arcGIS\GISdata\KDOT\KHUB\Implementation3\python\workspace-eclipse\PyDev106\KhubI3RouteCleanup2019


@author: kyleg
'''
#test route 02350326401 04550033400
from arcpy import (Delete_management, DeleteFeatures_management, RemoveJoin_management, MakeFeatureLayer_management, FeatureClassToFeatureClass_conversion, AddJoin_management, MakeRouteEventLayer_lr, GetParameterAsText, FeatureVerticesToPoints_management, MultipartToSinglepart_management, AddXY_management, Sort_management, Dissolve_management, CreateRoutes_lr, LocateFeaturesAlongRoutes_lr, AddField_management, SelectLayerByAttribute_management, CalculateField_management, Append_management)
from locref import GenerateRoutes
from arcpy import CopyFeatures_management, SelectLayerByLocation_management, MakeXYEventLayer_management, Frequency_analysis, SelectLayerByAttribute_management, GetCount_management
from arcpy import env
from arcpy.management import MakeFeatureLayer
from pandas.io.pytables import Selection
from mpmath import ones
env.overwriteOutput = 1

routeID = GetParameterAsText(0)

inTargetRoutes = r"TargetRoutesLocals"

inTargetRoutes = r"TargetMultipartLocals"
processingworkspace=r"C:/temp/routeparts.gdb"

env.workspace = processingworkspace
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "TargetRoutes"
   

#def RebuildRouteEW():
    
SingleRoute = "TargetRoute"+routeID
SingleRoute = inTargetRoutes # for all locals
selTheRoute = "RouteId = '"+routeID+"'"
FeatureClassToFeatureClass_conversion(inTargetRoutes, processingworkspace, SingleRoute, selTheRoute, '#', "")
#MakeFeatureLayer_management(r'C:/temp/RouteParts.gdb/TargetRoute04550033400', 'TargetRoute04550033400' )
MakeFeatureLayer_management(processingworkspace+"/"+SingleRoute, SingleRoute)
MultipartToSinglepart_management(SingleRoute, processingworkspace+"/SP")
FeatureVerticesToPoints_management("SP", processingworkspace+"/"+"SPstart", "START")
FeatureVerticesToPoints_management("SP", processingworkspace+"/"+"SPend", "END")
print("adding XY coordinates to start points")
AddXY_management("SPstart")

AddXY_management("SPend")
# for best results calculate the geometry lat long decimal degrees in the XY coordinates to eliminate projection longitude bias
#add steps here to compare differences between max and min X and Y coordinates
#use that information to step through the correct sorting order
MakeFeatureLayer_management(processingworkspace+"/SP", "SP")
MakeFeatureLayer_management(processingworkspace+"/SPstart", "SPstart")
AddJoin_management("SP", "OBJECTID", "SPstart", "OBJECTID", "KEEP_ALL")


Dissolve_management("SP", "C:/temp/RouteParts.gdb/SPXYRange", "SP.RouteId;SP.County;SP.Prefix;SP.RouteNum;SP.Suffix;SP.UniqueId;SP.InvDir", "SPstart.POINT_X RANGE;SPstart.POINT_Y RANGE", "MULTI_PART", "DISSOLVE_LINES")

SelectLayerByAttribute_management("SP", "NEW_SELECTION", "1=1")


MakeFeatureLayer_management("SPXYRange", "XRoutes", "RANGE_SPstart_POINT_X >RANGE_SPstart_POINT_Y", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;SP_RouteId SP_RouteId VISIBLE NONE;SP_County SP_County VISIBLE NONE;SP_Prefix SP_Prefix VISIBLE NONE;SP_RouteNum SP_RouteNum VISIBLE NONE;SP_Suffix SP_Suffix VISIBLE NONE;SP_UniqueId SP_UniqueId VISIBLE NONE;SP_InvDir SP_InvDir VISIBLE NONE;RANGE_SPstart_POINT_X RANGE_SPstart_POINT_X VISIBLE NONE;RANGE_SPstart_POINT_Y RANGE_SPstart_POINT_Y VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE")
MakeFeatureLayer_management("SPXYRange", "YRoutes", "RANGE_SPstart_POINT_Y >RANGE_SPstart_POINT_X", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;SP_RouteId SP_RouteId VISIBLE NONE;SP_County SP_County VISIBLE NONE;SP_Prefix SP_Prefix VISIBLE NONE;SP_RouteNum SP_RouteNum VISIBLE NONE;SP_Suffix SP_Suffix VISIBLE NONE;SP_UniqueId SP_UniqueId VISIBLE NONE;SP_InvDir SP_InvDir VISIBLE NONE;RANGE_SPstart_POINT_X RANGE_SPstart_POINT_X VISIBLE NONE;RANGE_SPstart_POINT_Y RANGE_SPstart_POINT_Y VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE")

AddJoin_management("SP", "SP.RouteId", "XRoutes", "SP_RouteId", "KEEP_COMMON")
SelectLayerByAttribute_management("SP", "NEW_SELECTION", "1=1")
RemoveJoin_management("SP", "SPXYRange")
Sort_management("SP", processingworkspace+"/"+"SPSortedX", "POINT_X ASCENDING;POINT_Y ASCENDING", "UR")
SelectLayerByAttribute_management("SP", "CLEAR_SELECTION", "")
#RemoveJoin_management("SP", "SPXYRange")
AddJoin_management("SP", "SP.RouteId", "YRoutes", "SP_RouteId", "KEEP_COMMON")
SelectLayerByAttribute_management("SP", "NEW_SELECTION", "1=1")
RemoveJoin_management("SP", "SPXYRange")
Sort_management("SP", processingworkspace+"/"+"SPSortedY", "POINT_Y ASCENDING;POINT_X ASCENDING", "UR")

Dissolve_management("SPSortedX", processingworkspace+"/"+"SPSortedMPX", "SP_LRSFromDate;SP_LRSToDate;SP_RouteId;SP_County;SP_Prefix;SP_RouteNum;SP_Suffix;SP_UniqueId;SP_InvDir", "", "MULTI_PART", "DISSOLVE_LINES")
Dissolve_management("SPSortedY", processingworkspace+"/"+"SPSortedMPY", "SP_LRSFromDate;SP_LRSToDate;SP_RouteId;SP_County;SP_Prefix;SP_RouteNum;SP_Suffix;SP_UniqueId;SP_InvDir", "", "MULTI_PART", "DISSOLVE_LINES")
print("creating route based on shape length")
CreateRoutes_lr("SPSortedMPX", "SP_RouteId", processingworkspace+"/"+"RebuiltX", "LENGTH", "", "", "LOWER_LEFT", "0.00018939393", "0", "IGNORE", "INDEX")
CreateRoutes_lr("SPSortedMPY", "SP_RouteId", processingworkspace+"/"+"RebuiltY", "LENGTH", "", "", "LOWER_LEFT", "0.00018939393", "0", "IGNORE", "INDEX")

#ended here 2/21/2019 
#following steps take time if doing all locals
LocateFeaturesAlongRoutes_lr("SPstart", "RebuiltX", "SP_RouteId", "0 Feet", processingworkspace+"/"+"CPNewMeasX", "RID POINT MEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
LocateFeaturesAlongRoutes_lr("SPend", "RebuiltX", "SP_RouteId", "0 Feet", processingworkspace+"/"+"CPNewMeasEndX", "RID POINT MEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
LocateFeaturesAlongRoutes_lr("SPstart", "RebuiltY", "SP_RouteId", "0 Feet", processingworkspace+"/"+"CPNewMeasY", "RID POINT MEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
LocateFeaturesAlongRoutes_lr("SPend", "RebuiltY", "SP_RouteId", "0 Feet", processingworkspace+"/"+"CPNewMeasEndY", "RID POINT MEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "CPNewMeasX"
MakeXYEventLayer_management("CPNewMeasX", "POINT_X", "POINT_Y", "CPNewMeasX_Layer", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")
MakeXYEventLayer_management("CPNewMeasY", "POINT_X", "POINT_Y", "CPNewMeasY_Layer", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")
MakeXYEventLayer_management("CPNewMeasEndX", "POINT_X", "POINT_Y", "CPNewMeasEndX_Layer", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")
MakeXYEventLayer_management("CPNewMeasEndY", "POINT_X", "POINT_Y", "CPNewMeasEndY_Layer", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

#MakeRouteEventLayer_lr(processingworkspace+"/RebuiltX", "SP_RouteId", "CPNewMeasX", "RID POINT meas", "CPNewMeasEventsX", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
#MakeRouteEventLayer_lr(processingworkspace+"/RebuiltX", "SP_RouteId", "CPNewMeasEndX", "RID POINT meas", "CPNewMeasEndEventsX", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
#MakeRouteEventLayer_lr(processingworkspace+"/RebuiltY", "SP_RouteId", "CPNewMeasY", "RID POINT meas", "CPNewMeasEventsY", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
#MakeRouteEventLayer_lr(processingworkspace+"/RebuiltY", "SP_RouteId", "CPNewMeasEndY", "RID POINT meas", "CPNewMeasEndEventsY", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "CPNewMeasX_Layer"
FeatureClassToFeatureClass_conversion("CPNewMeasX_Layer", "C:/temp/routeparts.gdb", "CPNewMeasEventsX", "RID = RouteId")      
FeatureClassToFeatureClass_conversion("CPNewMeasY_Layer", "C:/temp/routeparts.gdb", "CPNewMeasEventsY", "RID = RouteId")  
FeatureClassToFeatureClass_conversion("CPNewMeasEndX_Layer", "C:/temp/routeparts.gdb", "CPNewMeasEndEventsX", "RID = RouteId")  
FeatureClassToFeatureClass_conversion("CPNewMeasEndY_Layer", "C:/temp/routeparts.gdb", "CPNewMeasEndEventsY", "RID = RouteId")  
 
SelectLayerByLocation_management("CPNewMeasEndEventsX", "INTERSECT", "CPNewMeasEventsX", "", "NEW_SELECTION", "NOT_INVERT")    
DeleteFeatures_management("CPNewMeasEndEventsX")

SelectLayerByLocation_management("CPNewMeasEndEventsY", "INTERSECT", "CPNewMeasEventsY", "", "NEW_SELECTION", "NOT_INVERT")    
DeleteFeatures_management("CPNewMeasEndEventsY")
    
    
AddField_management("CPNewMeasEventsX", "Measure", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
AddField_management("CPNewMeasEventsY", "Measure", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
AddField_management("CPNewMeasEndEventsX", "Measure", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
AddField_management("CPNewMeasEndEventsY", "Measure", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
SelectLayerByAttribute_management("CPNewMeasEventsX", "NEW_SELECTION", "MEAS >0")
#increment the measure across the start point
CalculateField_management("CPNewMeasEventsX", "Measure", "[MEAS]+0.0000001", "VB", "")
SelectLayerByAttribute_management("CPNewMeasEventsX", "CLEAR_SELECTION", "")

SelectLayerByAttribute_management("CPNewMeasEventsY", "NEW_SELECTION", "MEAS >0")
#increment the measure across the start point
CalculateField_management("CPNewMeasEventsY", "Measure", "[MEAS]+0.0000001", "VB", "")
SelectLayerByAttribute_management("CPNewMeasEventsY", "CLEAR_SELECTION", "")

AddField_management("CPNewMeasEventsX", "NetworkID", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
AddField_management("CPNewMeasEventsY", "NetworkID", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
CalculateField_management("CPNewMeasEventsX", "NetworkID", "1", "VB", "")
CalculateField_management("CPNewMeasEventsY", "NetworkID", "1", "VB", "")

    
AddField_management("CPNewMeasEndEventsX", "NetworkID", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
CalculateField_management("CPNewMeasEndEventsX", "NetworkID", "1", "VB", "")
AddField_management("CPNewMeasEndEventsY", "NetworkID", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
CalculateField_management("CPNewMeasEndEventsY", "NetworkID", "1", "VB", "")


    #by not adding the incremented value to the end of the route I am losing 0.0000001 miles per route part.
    #to not lose the 0.006 inches per part, we would need to add to the end measure, and consider the number of parts
    #rather than program that in, it is assumed acceptable to lose 0.006 inches per part
CalculateField_management("CPNewMeasEndEventsX", "LRSFromDate", '"1/1/2018"', "VB", "")
CalculateField_management("CPNewMeasEndEventsY", "LRSFromDate", '"1/1/2018"', "VB", "")

CalculateField_management("CPNewMeasEventsX", "LRSFromDate", '"1/1/2018"', "VB", "")
CalculateField_management("CPNewMeasEventsY", "LRSFromDate", '"1/1/2018"', "VB", "")

   
from arcpy import SpatialJoin_analysis, AddIndex_management, Merge_management, FindIdentical_management, Statistics_analysis
#delete duplicates and keep one:
Merge_management(inputs="CPNewMeasEndEventsY;CPNewMeasEndEventsX;CPNewMeasEventsY;CPNewMeasEventsX", output="C:/temp/routeparts.gdb/CalibrationPoints_MultipartLocals")
FindIdentical_management(in_dataset="CalibrationPoints_MultipartLocals", out_dataset="C:/temp/routeparts.gdb/cp_identicals", fields="RID;MEAS;POINT_X;POINT_Y;Measure", xy_tolerance="", z_tolerance="0", output_record_option="ONLY_DUPLICATES")
Statistics_analysis(in_table="cp_identicals", out_table="C:/temp/routeparts.gdb/cp_identicals_to_delete", statistics_fields="IN_FID MIN", case_field="FEAT_SEQ")
AddJoin_management(in_layer_or_view="CalibrationPoints_MultipartLocals", in_field="OBJECTID", join_table="cp_identicals", join_field="IN_FID", join_type="KEEP_COMMON")
SelectLayerByAttribute_management(in_layer_or_view="CalibrationPoints_MultipartLocals", selection_type="NEW_SELECTION", where_clause="1=1")
AddJoin_management(in_layer_or_view="CalibrationPoints_MultipartLocals", in_field="cp_identicals.FEAT_SEQ", join_table="cp_identicals_to_delete", join_field="FEAT_SEQ", join_type="KEEP_COMMON")
SelectLayerByAttribute_management(in_layer_or_view="CalibrationPoints_MultipartLocals", selection_type="REMOVE_FROM_SELECTION", where_clause="cp_identicals_to_delete.MIN_IN_FID = cp_identicals.IN_FID")
RemoveJoin_management(in_layer_or_view="CalibrationPoints_MultipartLocals", join_name="cp_identicals_to_delete")
RemoveJoin_management(in_layer_or_view="CalibrationPoints_MultipartLocals", join_name="cp_identicals")
DeleteFeatures_management(in_features="CalibrationPoints_MultipartLocals")
    
    
    
#    select calibration points to end date
#    135138 by spatial Selection
#spatial join new cps to old ones, out put all
#select the matching route IDs from teh SJ
#join FID ot OID from the matched SJ/route combos
#select the CP's from the join (all form common join)
#remove teh join
#end date the  CP's
#Cp def query for locals - (FromDate is null or FromDate<=CURRENT_TIMESTAMP) and (ToDate is null or ToDate>CURRENT_TIMESTAMP) AND Substring(RouteId, 4, 1) = '6'


SpatialJoin_analysis(target_features="Calibration_Points_Local", join_features="CalibrationPoints_MultipartLocals", out_feature_class="C:/temp/routeparts.gdb/CalibrationPoints_EndDateSJ", join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", '#' , match_option="INTERSECT", search_radius="", distance_field_name="")
SelectLayerByAttribute_management(in_layer_or_view="CalibrationPoints_EndDateSJ", selection_type="NEW_SELECTION", where_clause="RouteId <> RID or RID is null")
DeleteFeatures_management(in_features="CalibrationPoints_EndDateSJ")
# copy CP layer with no def query

AddIndex_management(in_table="CalibrationPoints_EndDateSJ", fields="TARGET_FID", index_name="tfid", unique="UNIQUE", ascending="ASCENDING")

#select the 
SelectLayerByAttribute_management(in_layer_or_view="CalibrationPoints_EndDateSJ", selection_type="NEW_SELECTION", where_clause="RouteId <> RID or RID is null")
#we have to remove a time def query fron the CP's to efficiently execute these join and select operations
AddJoin_management(in_layer_or_view="Calibration_Points_nodef", in_field="OBJECTID", join_table="CalibrationPoints_EndDateSJ", join_field="TARGET_FID", join_type="KEEP_ALL")
#this selction is really taking a long time???? --- add index to targetfid - yeah that helps a TON
SelectLayerByAttribute_management(in_layer_or_view="Calibration_Points_nodef", selection_type="NEW_SELECTION", where_clause="CalibrationPoints_EndDateSJ.TARGET_FID IS NOT NULL")
RemoveJoin_management(in_layer_or_view="Calibration_Points_nodef", join_name="")


#in edit session end date the existing calibration points
print("end dating calibration points for route " + str(routeID))
SelectLayerByAttribute_management(r"tCalibration_Point", "NEW_SELECTION", selTheRoute)

CalculateField_management(r"tCalibration_Point", "ToDate", '"1/1/2018"', "VB", "")
#since hte CP's were created buy lat/long, need to project merged CP's to the target projection before appending
#

    #Append_management(processingworkspace+"/CPNewMeasEvents", "tCalibration_Point", "NO_TEST", 'FromDate "FromDate" true true false 8 Date 0 0 ,First,#,CPNewMeas Events,LRSFromDate,-1,-1;ToDate "ToDate" true true false 8 Date 0 0 ,First,#;NetworkId "NetworkId" true true false 2 Short 0 5 ,First,#,CPNewMeas Events,NetworkID,-1,-1;RouteId "RouteId" true true false 255 Text 0 0 ,First,#,CPNewMeas Events,RouteId,-1,-1;Measure "Measure" true true false 8 Double 8 38 ,First,#,CPNewMeas Events,NewMeasure,-1,-1;created_user "created_user" false true false 255 Text 0 0 ,First,#,CPNewMeas Events,created_user,-1,-1;created_date "created_date" false true false 8 Date 0 0 ,First,#,CPNewMeas Events,created_date,-1,-1;last_edited_user "last_edited_user" false true false 255 Text 0 0 ,First,#,CPNewMeas Events,last_edited_user,-1,-1;last_edited_date "last_edited_date" false true false 8 Date 0 0 ,First,#,CPNewMeas Events,last_edited_date,-1,-1', subtype="")
    #Append_management(processingworkspace+"/CPNewMeasEndEvents", "tCalibration_Point", "NO_TEST", 'FromDate "FromDate" true true false 8 Date 0 0 ,First,#,CPNewMeasEnd Events,LRSFromDate,-1,-1;ToDate "ToDate" true true false 8 Date 0 0 ,First,#;NetworkId "NetworkId" true true false 2 Short 0 5 ,First,#,CPNewMeasEnd Events,NetworkID,-1,-1;RouteId "RouteId" true true false 255 Text 0 0 ,First,#,CPNewMeasEnd Events,RouteId,-1,-1;Measure "Measure" true true false 8 Double 8 38 ,First,#,CPNewMeasEnd Events,MEAS,-1,-1;created_user "created_user" false true false 255 Text 0 0 ,First,#,CPNewMeasEnd Events,created_user,-1,-1;created_date "created_date" false true false 8 Date 0 0 ,First,#,CPNewMeasEnd Events,created_date,-1,-1;last_edited_user "last_edited_user" false true false 255 Text 0 0 ,First,#,CPNewMeasEnd Events,last_edited_user,-1,-1;last_edited_date "last_edited_date" false true false 8 Date 0 0 ,First,#,CPNewMeasEnd Events,last_edited_date,-1,-1', subtype="")

    #Might need to make an event layer here first
    #Append_management("CPNewMeas Events", "Target ALRS\tCalibration_Point", "NO_TEST", 'LRSFromDate "LRSFromDate" true true false 8 Date 0 0 ,First,#;LRSToDate "LRSToDate" true true false 8 Date 0 0 ,First,#;NetworkId "NetworkId" true true false 2 Short 0 5 ,First,#,CPNewMeas Events,NetworkID,-1,-1;RouteId "RouteId" true true false 255 Text 0 0 ,First,#,CPNewMeas Events,RouteId,-1,-1;Measure "Measure" true true false 8 Double 8 38 ,First,#,CPNewMeas Events,NewMeasure,-1,-1;created_user "created_user" false true false 255 Text 0 0 ,First,#,CPNewMeas Events,created_user,-1,-1;created_date "created_date" false true false 8 Date 0 0 ,First,#,CPNewMeas Events,created_date,-1,-1;last_edited_user "last_edited_user" false true false 255 Text 0 0 ,First,#,CPNewMeas Events', subtype="")
    #Append_management("CPNewMeasEnd Events'", "Target ALRS\tCalibration_Point", "NO_TEST", 'LRSFromDate "LRSFromDate" true true false 8 Date 0 0 ,First,#,CPNewMeasEnd Events,SPstart_LRSFromDate,-1,-1;ToDate "ToDate" true true false 8 Date 0 0 ,First,#;NetworkId "NetworkId" true true false 2 Short 0 5 ,First,#,CPNewMeasEnd Events,NetworkID,-1,-1;RouteId "RouteId" true true false 255 Text 0 0 ,First,#,CPNewMeasEnd Events,RID,-1,-1;Measure "Measure" true true false 8 Double 8 38 ,First,#,CPNewMeasEnd Events,MEAS,-1,-1;created_user "created_user" false true false 255 Text 0 0 ,First,#;created_date "created_date" false true false 8 Date 0 0 ,First,#;last_edited_user "last_edited_user" false true false 255 Text 0 0 ,First,#;last_edited_date "last_edited_date" false true false 8 Date 0 0 ,First,#', subtype="")
    #

GenerateRoutes(inTargetRoutes)
    #Delete_management(processingworkspace+"/"+"CPNewMeas Events", data_type="")
    #Delete_management(processingworkspace+"/"+"CPNewMeasEnd Events", data_type="")
    #Delete_management(processingworkspace+"/"+"RouteFrequency", data_type="")
    #Delete_management(processingworkspace+"/"+"CPNewMeas", data_type="")
    #Delete_management(processingworkspace+"/"+"CPNewMeasEnd", data_type="")
    #Delete_management(processingworkspace+"/"+"SPend", data_type="")
    #Delete_management(processingworkspace+"/"+"SPstart", data_type="")
    #Delete_management(processingworkspace+"/"+"SPSortedMP", data_type="")
    #Delete_management(processingworkspace+"/"+"Rebuilt", data_type="")
    #Delete_management(processingworkspace+"/"+"SPSorted", data_type="")
    #Delete_management(processingworkspace+"/"+"SP", data_type="")
    #Delete_management(in_data="Target ALRS\tTargetRoutesCurrentPartsTest", data_type="")
    #Delete_management(in_data="Target ALRS\TargetRoutesCurrentTest", data_type="")
    

def CountMultipartRoutes():
    CopyFeatures_management(inTargetRoutes, "C:/temp/RouteParts.gdb/TargetRoutesCurrent", "", "0", "0", "0")
    MultipartToSinglepart_management("C:/temp/RouteParts.gdb/TargetRoutesCurrent", "C:/temp/RouteParts.gdb/TargetRoutesCurrentParts")
    Frequency_analysis("TargetRoutesCurrentParts", "C:/temp/RouteParts.gdb/RouteFrequency", "RouteId;ORIG_FID", "SHAPE_Length")
    SelectLayerByAttribute_management("RouteFrequency", "NEW_SELECTION", "FREQUENCY >1")
    print(str(GetCount_management("RouteFrequency")))
    
 

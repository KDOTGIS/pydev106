'''
Created on Apr 17, 2019
define fields that are abstract fields for point and polygon event models and delete them from the geodatabase
@author: kyleg
'''

from arcpy import CreateFileGDB_management, ListFeatureClasses, DeleteField_management, env, DisableEditorTracking_management

gdb = r'C:\temp\KHUB3_2019062601sansab.gdb'

env.workspace = gdb
print env.workspace

LinearAbstractClassFields = ["EventID", "RouteID", "FromMeasure", "ToMeasure",  "LRSFromDate", "LRSToDate", "LocError", "InventoryStartDate", "SourceCIT"]
PointAbstractClassFields = ["EventID", "RouteID", "Measure", "LRSFromDate", "LRSToDate","InventoryStartDate", "LocError", "SourceCIT"]

EditTrackingAbstractFields = ["CreatedUser", "CreatedDate", "LastEditedUser", "LastEditedDate"]

LinearEvents = ListFeatureClasses("ev*", "Polyline")
for fcline in LinearEvents:
    print fcline
    DisableEditorTracking_management (fcline)
    DeleteField_management(fcline, LinearAbstractClassFields)
    DeleteField_management(fcline, EditTrackingAbstractFields)

PointEvents = ListFeatureClasses("ev*", "Point")
for fcpt in PointEvents:
    print fcpt
    DisableEditorTracking_management (fcpt)
    DeleteField_management(fcpt, PointAbstractClassFields)
    DeleteField_management(fcpt, EditTrackingAbstractFields)





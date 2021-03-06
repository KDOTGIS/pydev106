'''
Created on Apr 17, 2019
define fields that are abstract fields for point and polygon event models and delete them from the geodatabase
@author: kyleg
'''
from arcpy.mapping import ListTableViews
print ("started")
from arcpy import CreateFileGDB_management, ListFeatureClasses, DeleteField_management, env, DisableEditorTracking_management, Rename_management, ListTables
print ("arcpy tools imported")
gdb = r'Database Connections\RHDevXML@sqlgis.sde'
dbnameowner = 'Khub_20190805.RH.'
env.workspace = gdb
print env.workspace
print("workspace set")
LinearAbstractClassFields = ["EventID", "RouteID", "FromMeasure", "ToMeasure",  "LRSFromDate", "LRSToDate", "LocError", "InventoryStartDate", "SourceCIT"]
PointAbstractClassFields = ["EventID", "RouteID", "Measure", "LRSFromDate", "LRSToDate","InventoryStartDate", "LocError", "SourceCIT"]
TabularAbstractClassFields = ["EventID", "RouteID", "FromMeasure", "ToMeasure", "Measure", "LRSFromDate", "LRSToDate", "LocError", "InventoryStartDate", "SourceCIT"]

EditTrackingAbstractFields = ["CreatedUser", "CreatedDate", "LastEditedUser", "LastEditedDate"]
#.RH.
print ("field lists created")
'''
RenameFeatures = ListFeatureClasses(dbnameowner+"KHUB_RH_*")
print ("lists fc created")
for rhfeatures in RenameFeatures:
    print(rhfeatures, rhfeatures[25:])
    Rename_management(rhfeatures, rhfeatures[25:])


LinearEvents = ListFeatureClasses(dbnameowner+"ev*", "Polyline")
for fcline in LinearEvents:
    print(fcline)
    DisableEditorTracking_management (fcline)
    DeleteField_management(fcline, LinearAbstractClassFields)
    DeleteField_management(fcline, EditTrackingAbstractFields)

PointEvents = ListFeatureClasses(dbnameowner+"ev*", "Point")
for fcpt in PointEvents:
    print(fcpt)
    DisableEditorTracking_management (fcpt)
    DeleteField_management(fcpt, PointAbstractClassFields)
    DeleteField_management(fcpt, EditTrackingAbstractFields)
'''

TableEvents = ListTables()
for tables in TableEvents:
    print(tables)
    DisableEditorTracking_management (tables)
    DeleteField_management(tables, TabularAbstractClassFields)
    DeleteField_management(tables, EditTrackingAbstractFields)


'''
Created on Aug 14, 2019

@author: kyleg
'''

from arcpy import ExportXMLWorkspaceDocument_management
from config_dev import rh, rhdo
from KhubFCList import TestEvents, EventList, NetworksList, ALRS_Tables

def exportDevSchemaXML():
    for event in EventList:
        print(rh+"/"+rhdo+event)
        exportfeature = rh+"/"+rhdo+event
        ExportXMLWorkspaceDocument_management(exportfeature, r"C:/temp/KHDEV/"+event+".xml", "SCHEMA_ONLY", "NORMALIZED", "METADATA")
        '''
        
    for network in NetworksList:
        print(rh+"/"+rhdo+network)
        exportfeature = rh+"/"+rhdo+network
        ExportXMLWorkspaceDocument_management(exportfeature, r"C:/temp/KHDEV/"+network+".xml", "SCHEMA_ONLY", "NORMALIZED", "METADATA")    
        
    for table in ALRS_Tables:
        print(rh+"/"+rhdo+table)
        exportfeature = rh+"/"+rhdo+table
        ExportXMLWorkspaceDocument_management(exportfeature, r"C:/temp/KHDEV/"+table+".xml", "SCHEMA_ONLY", "NORMALIZED", "METADATA")    
'''
def importDevSchemaXML():
    from arcpy import ImportXMLWorkspaceDocument_management, Exists
    DBName = "KH04"
    TargetDB = r"C:/gisdata/DBConnections/Khub/KHDev/rh@"+DBName+".sde"
    '''for network in NetworksList:
        print(TargetDB+r"/"+DBName+".RH."+network)
        if Exists(TargetDB+r"/"+DBName+".RH."+network):
            print(TargetDB+r"/"+DBName+".RH."+network + " Exists")
        else:
            print(network)
            ImportXMLWorkspaceDocument_management(TargetDB, r"C:/temp/KHDEV/"+network+".xml", "SCHEMA_ONLY")
    '''
    for event in EventList:
        print(event)
        importfeature = event
        if Exists(TargetDB+r"/"+DBName+".RH."+importfeature):
            print(importfeature + " Exists")
        else:
            ImportXMLWorkspaceDocument_management(TargetDB, r"C:/temp/KHDEV/"+importfeature+".xml", "SCHEMA_ONLY")

def EnterpriseModel():    
    from arcpy import CreateEnterpriseGeodatabase_management, CreateDatabaseConnection_management, CreateDatabaseUser_management
    import getpass
    sapass = getpass('sysadmin password')
    sdepass = getpass('sde password')
    rhpass = getpass('RH password')
    DBName = "KH04"
    CreateEnterpriseGeodatabase_management("SQL_Server", "sqlgis\gdb_dev", DBName, "DATABASE_AUTH", "geo_admin", sapass, "SDE_SCHEMA", "sde", sdepass, "", "C:/gisdata/keycodes/License10.6/sysgen/keycodes")
    CreateDatabaseConnection_management("C:\gisdata\DBConnections\Khub\KHDev", "sde@"+DBName, "SQL_Server", "sqlgis\gdb_dev", "DATABASE_AUTH", "sde", sdepass, "SAVE_USERNAME", DBName)
    CreateDatabaseConnection_management("C:\gisdata\DBConnections\Khub\KHDev", "sa@"+DBName, "SQL_Server", "sqlgis\gdb_dev", "DATABASE_AUTH", "geo_admin", sapass, "SAVE_USERNAME", DBName)
    CreateDatabaseUser_management("C:\gisdata\DBConnections\Khub\KHDev\\"+"sa@"+DBName,  "DATABASE_AUTH", "RH", rhpass)
    CreateDatabaseConnection_management("C:\gisdata\DBConnections\Khub\KHDev", "rh@"+DBName, "SQL_Server", "sqlgis\gdb_dev", "DATABASE_AUTH", "rh", rhpass, "SAVE_USERNAME", DBName)

def exportSubsetDevSchemaXML():
    DBName = "KH04"
    exportfeature = r'C:\gisdata\DBConnections\Khub\KHDev\rh@'+DBName+'.sde'
    ExportXMLWorkspaceDocument_management(exportfeature, r"C:/temp/KHDEV/"+DBName+".xml", "SCHEMA_ONLY", "NORMALIZED", "METADATA")    
    
def DeleteAbstractFields():
    from arcpy import DeleteField_management, env, ListTables, DisableEditorTracking_management, Exists
    
    DBName = "KH04"
    DBOwn = "RH" 
    TargetDB = r"C:/gisdata/DBConnections/Khub/KHDev/rh@"+DBName+".sde"
    print ("arcpy tools imported")
    env.workspace = TargetDB
    print env.workspace
    print("workspace set")
    EditTrackingAbstractFields = ["CreatedUser", "CreatedDate", "LastEditedUser", "LastEditedDate"]
    LinearAbstractClassFields = ["EventID", "RouteID", "FromMeasure", "ToMeasure",  "LRSFromDate", "LRSToDate", "LocError", "InventoryStartDate", "SourceCIT"]
    PointAbstractClassFields = ["EventID", "RouteID", "Measure", "LRSFromDate", "LRSToDate","InventoryStartDate", "LocError", "SourceCIT"]
    TabularAbstractClassFields = ["EventID", "RouteID", "FromMeasure", "ToMeasure", "Measure", "LRSFromDate", "LRSToDate", "LocError", "InventoryStartDate", "SourceCIT"]
    DeleteFields = TabularAbstractClassFields+EditTrackingAbstractFields
    for event in EventList:
        if Exists(TargetDB+r"/"+DBName+".RH."+event):
            print(event + " Exists")
            DisableEditorTracking_management(event)
            DeleteField_management(event, TabularAbstractClassFields)
        else:
            print(event +" does not exist")


def ValidatetoFileGDB():
    from arcpy import ImportXMLWorkspaceDocument_management, Exists, CreateFileGDB_management, Delete_management
    xmlIn = r"C:\temp\ValidateThis.xml"
    gdbname = "Validated"
    GDB_In = r"C:/temp/"+gdbname
    gdbin = GDB_In+".gdb"
    if Exists(gdbin):
        Delete_management(gdbin, "Workspace")
        CreateFileGDB_management(r"C:/temp", gdbname, "CURRENT")
        print("new geodatabase created")
    else:
        CreateFileGDB_management(r"C:/temp", gdbname, "CURRENT")
    ImportXMLWorkspaceDocument_management(gdbin, xmlIn, import_type="SCHEMA_ONLY")
    print("validated")

def StageLinearEventTemplate():
    EventName = "ev_LegacyRoute"
    #EventType = "Polyline" # Polyline or Point
    from arcpy import AddField_management, CreateFeatureclass_management, env
    env.XYResolution = "0.0001 Feet"
    env.XYTolerance = "0.003280833333333 Feet"
    env.MResolution = "0.000000018939394"
    env.MTolerance = "0.000000621369949"
    stagedb = r"C:/gisdata/DBConnections/Khub/KHDev/rh@KH04.sde"
    CreateFeatureclass_management(stagedb, "ev_LineTemplate", "POLYLINE", "", "ENABLED", "ENABLED", "", "", "0", "0", "0")
    AddField_management(stagedb+r"/ev_LineTemplate", "EventID", "TEXT", "", "", "38", "EventID", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "RouteID", "TEXT", "", "", "38", "RouteID", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "FromMeasure", "Double", "38", "7", "", "FromMeasure", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "ToMeasure", "Double", "38", "7", "", "ToMeasure", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "InventoryStartDate", "Date", "", "", "", "InventoryStartDate", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "LRSFromDate", "Date", "", "", "", "LRSFromDate", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "LRSToDate", "Date", "", "", "", "LRSToDate", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "CreatedUser", "TEXT", "", "", "20", "CreatedUser", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "LastEditedUser", "TEXT", "", "", "20", "LastEditedUser", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "CreatedDate", "Date", "", "", "", "CreatedDate", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "LastEditedDate", "Date", "", "", "", "LastEditedDate", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(stagedb+r"/ev_LineTemplate", "SourceCIT", "TEXT", "", "", "20", "SourceCIT", "NULLABLE", "NON_REQUIRED", "dSourceCIT")
    AddField_management(stagedb+r"/ev_LineTemplate", "LocError", "TEXT", "", "", "100", "LocError", "NULLABLE", "NON_REQUIRED", "")

def StageNewEventLegacyRoute():
    from arcpy import AddField_management, CreateFeatureclass_management, env, Exists
    env.XYResolution = "0.0001 Feet"
    env.XYTolerance = "0.003280833333333 Feet"
    env.MResolution = "0.000000018939394"
    env.MTolerance = "0.000000621369949"
    stagedb = r"C:/gisdata/DBConnections/Khub/KHDev/rh@KH04.sde"
    template = stagedb+r"/ev_LineTemplate"
    newevent = "ev_LegacyRoute"
    newevent1 = stagedb+ r"/"+newevent
    if Exists(newevent):
        print("feature exists")
    else:
        CreateFeatureclass_management(stagedb, newevent, "POLYLINE", template, "ENABLED", "ENABLED", "", "", "0", "0", "0")
    AddField_management(newevent1, "LegacyCRND", "TEXT", "", "", "38", "LegacyCRND", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(newevent1, "BegCountyLogmile", "Double", "38", "7", "", "BegCountyLogmile", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(newevent1, "EndCountyLogmile", "Double", "38", "7", "", "EndCountyLogmile", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(newevent1, "Flip", "TEXT", "", "", "2", "Flip", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(newevent1, "Comment", "TEXT", "", "", "100", "Comment", "NULLABLE", "NON_REQUIRED", "")
    
def StageNewEventSurfaceType():
    from arcpy import AddField_management, CreateFeatureclass_management, env, Exists, CreateDomain_management, AddCodedValueToDomain_management
    Projection = r'\\gisdata\khub\documentation\NAD_83_Kansas_Lambert_Conformal_Conic_Feet.prj'
    env.XYResolution = "0.0001 Feet"
    env.XYTolerance = "0.003280833333333 Feet"
    env.MResolution = "0.000000018939394"
    env.MTolerance = "0.000000621369949"
    stagedb = r"C:/gisdata/DBConnections/Khub/KHDev/rh@KH04.sde"
    template = stagedb+r"/ev_LineTemplate"
    newevent = "ev_SurfaceType"
    newevent1 = stagedb+ r"/"+newevent
    if Exists(newevent):
        print("feature exists")
    else:
        CreateFeatureclass_management(stagedb, newevent, "POLYLINE", template, "ENABLED", "ENABLED", Projection)
    AddField_management(newevent1, "SurfaceType", "TEXT", "", "", "4", "Basic Surface Type", "NULLABLE", "NON_REQUIRED", "")
    #CreateDomain_management(stagedb, "dSurfaceType", "SurfaceType Generic", "TEXT", "CODED", "DUPLICATE", "DEFAULT")
    #AddCodedValueToDomain_management(stagedb, "dSurfaceType", "GRVL", "Gravel")
    #AddCodedValueToDomain_management(stagedb, "dSurfaceType", "PAVE", "Paved")
    #AddCodedValueToDomain_management(stagedb, "dSurfaceType", "PROP", "Proposed")
    #AddCodedValueToDomain_management(stagedb, "dSurfaceType", "SOIL", "Soil")

def StageNewEventNG911Segments():
    from arcpy import AddField_management, CreateFeatureclass_management, env, Exists, CreateDomain_management, AddCodedValueToDomain_management
    Projection = r'\\gisdata\khub\documentation\NAD_83_Kansas_Lambert_Conformal_Conic_Feet.prj'
    env.XYResolution = "0.0001 Feet"
    env.XYTolerance = "0.003280833333333 Feet"
    env.MResolution = "0.000000018939394"
    env.MTolerance = "0.000000621369949"
    stagedb = r"C:/gisdata/DBConnections/Khub/KHDev/rh@KH04.sde"
    template = stagedb+r"/ev_LineTemplate"
    newevent = "ev_NG911Segments"
    newevent1 = stagedb+ r"/"+newevent
    if Exists(newevent):
        print("feature exists")
    else:
        CreateFeatureclass_management(stagedb, newevent, "POLYLINE", template, "ENABLED", "ENABLED", Projection)
    AddField_management(newevent1, "Steward", "TEXT", "", "", "50", "NG911 Steward", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(newevent1, "SegID", "TEXT", "", "", "50", "SegmentID", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(newevent1, "AliasID", "TEXT", "", "", "50", "AliasID", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(newevent1, "SegmentSyncDate", "Date", "", "", "", "SyncDate", "NULLABLE", "NON_REQUIRED", "")
    
    #CreateDomain_management(stagedb, "dSurfaceType", "SurfaceType Generic", "TEXT", "CODED", "DUPLICATE", "DEFAULT")
    #AddCodedValueToDomain_management(stagedb, "dSurfaceType", "GRVL", "Gravel")
    #AddCodedValueToDomain_management(stagedb, "dSurfaceType", "PAVE", "Paved")
    #AddCodedValueToDomain_management(stagedb, "dSurfaceType", "PROP", "Proposed")
    #AddCodedValueToDomain_management(stagedb, "dSurfaceType", "SOIL", "Soil")
    
def AppendNewEventData():    
    from arcpy import Append_management, env, EnableEditorTracking_management
    from locref import AppendEvents
    stagedb = r"C:/gisdata/DBConnections/Khub/KHDev/rh@KH04.sde"
    template = stagedb+r"/ev_LineTemplate"
    newevent = "ev_LegacyRoute"
    newevent1 = stagedb+ r"/"+newevent
    sourcedata = "MainLineEvent_new"
    env.workspace = r"//gisdata/Planning/GIS/Temp/MainlineEvent.gdb"
    targetEvent = r"C:/gisdata/DBConnections/Khub/KHDev/rh@KHubdevKHUB.sde/KHUB.RH.ev_LegacyRoute"
    
    field_mapping='''EventID "EventID" true true false 38 Text 0 0 ,First,#,MainLineEvent_new,OBJECTID,-1,-1;
    RouteID "RouteID" true true false 38 Text 0 0 ,First,#,MainLineEvent_new,RouteId,-1,-1;
    FromMeasure "FromMeasure" true true false 8 Double 7 38 ,First,#,MainLineEvent_new,FromMeasure,-1,-1;
    ToMeasure "ToMeasure" true true false 8 Double 7 38 ,First,#,MainLineEvent_new,ToMeasure,-1,-1;
    InventoryStartDate "InventoryStartDate" true true false 8 Date 0 0 ,First,#;
    LRSFromDate "LRSFromDate" true true false 8 Date 0 0 ,First,#,MainLineEvent_new,LRSFromDate,-1,-1;
    LRSToDate "LRSToDate" true true false 8 Date 0 0 ,First,#,
    MainLineEvent_new,LRSToDate,-1,-1;CreatedUser "CreatedUser" true true false 20 Text 0 0 ,First,#;
    LastEditedUser "LastEditedUser" true true false 20 Text 0 0 ,First,#;CreatedDate "CreatedDate" true true false 8 Date 0 0 ,First,#;
    LastEditedDate "LastEditedDate" true true false 8 Date 0 0 ,First,#;SourceCIT "SourceCIT" true true false 20 Text 0 0 ,First,#;
    LocError "LocError" true true false 100 Text 0 0 ,First,#,MainLineEvent_new,LOC_ERROR,-1,-1;
    LegacyCRND "LegacyCRND" true true false 38 Text 0 0 ,First,#, MainLineEvent_new,LegacyRouteId,-1,-1;
    Comment "Comment" true true false 100 Text 0 0 ,First,#, MainLineEvent_new,DataReviewNotes,-1,-1;
    BegCountyLogmile "BegCountyLogmile" true true false 8 Double 7 38 ,First,#,MainLineEvent_new,County_BMP,-1,-1;
    EndCountyLogmile "EndCountyLogmile" true true false 8 Double 7 38 ,First,#,MainLineEvent_new,County_EMP,-1,-1;
    Flip "Flip" true true false 2 Text 0 0 ,First,#,MainLineEvent_new,FLIP,-1,-1;
    Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#'''
    Append_management(sourcedata, newevent1, "NO_TEST", field_mapping, subtype="")
    #register the event manually
    eventFieldMapping='''EventID "EventID" true true false 38 Text 0 0 ,First,#,ev_LegacyRoute,EventID,-1,-1;
    RouteID "RouteID" true true false 38 Text 0 0 ,First,#,ev_LegacyRoute,RouteID,-1,-1;
    FromMeasure "FromMeasure" true true false 8 Double 7 38 ,First,#,ev_LegacyRoute,FromMeasure,-1,-1;
    ToMeasure "ToMeasure" true true false 8 Double 7 38 ,First,#,ev_LegacyRoute,ToMeasure,-1,-1;
    InventoryStartDate "InventoryStartDate" true true false 8 Date 0 0 ,First,#,ev_LegacyRoute,InventoryStartDate,-1,-1;
    LRSFromDate "LRSFromDate" true true false 8 Date 0 0 ,First,#,ev_LegacyRoute,LRSFromDate,-1,-1;
    LRSToDate "LRSToDate" true true false 8 Date 0 0 ,First,#,ev_LegacyRoute,LRSToDate,-1,-1;
    CreatedUser "CreatedUser" true true false 20 Text 0 0 ,First,#,ev_LegacyRoute,CreatedUser,-1,-1;
    LastEditedUser "LastEditedUser" true true false 20 Text 0 0 ,First,#,ev_LegacyRoute,LastEditedUser,-1,-1;
    CreatedDate "CreatedDate" true true false 8 Date 0 0 ,First,#,ev_LegacyRoute,CreatedDate,-1,-1;
    LastEditedDate "LastEditedDate" true true false 8 Date 0 0 ,First,#,ev_LegacyRoute,LastEditedDate,-1,-1;
    SourceCIT "SourceCIT" true true false 20 Text 0 0 ,First,#,ev_LegacyRoute,SourceCIT,-1,-1;
    LegacyCRND "LegacyCRND" true true false 38 Text 0 0 ,First,#,ev_LegacyRoute,LegacyCRND,-1,-1;
    Comment "Comment" true true false 100 Text 0 0 ,First,#,ev_LegacyRoute,Comment,-1,-1;
    BegCountyLogmile "BegCountyLogmile" true true false 8 Double 7 38 ,First,#,ev_LegacyRoute,BegCountyLogmile,-1,-1;
    EndCountyLogmile "EndCountyLogmile" true true false 8 Double 7 38 ,First,#,ev_LegacyRoute,EndCountyLogmile,-1,-1;
    Flip "Flip" true true false 2 Text 0 0 ,First,#,ev_LegacyRoute,Flip,-1,-1'''
    
    AppendEvents(template, targetEvent, eventFieldMapping, "ADD", "GENERATE_EVENT_IDS", "GENERATE_SHAPES")
    EnableEditorTracking_management(targetEvent, "CreatedUser", "CreatedDate", "LastEditedUser", "LastEditedDate", "", "UTC")
    
    
def StageAndRegister():
    "The Stage new Event approach requires manual event registration, then appending event data"
    "This stage approach copies a pre-staged featuer class, allowing new event data to be registered without needing to then append"
    "it also aviods the field mapping process associated with appending staged data to hte new event"
    from arcpy import FeatureClassToFeatureClass_conversion, EnableEditorTracking_management, RegisterAsVersioned_management, env
    prestaged = r"C:/gisdata/DBConnections/Khub/KHDev/rh@KH04.sde/KH04.RH.ev_LegacyRoute"
    targetstaged = r"C:\gisdata\DBConnections\Khub\Khub\rh@KHTransKHUB.sde"
    targetstagedFC = "ev_LegacyRoute"
    env.XYResolution = "0.0001 Feet"
    env.XYTolerance = "0.003280833333333 Feet"
    env.MResolution = "0.000000018939394"
    env.MTolerance = "0.000000621369949"
    
    FeatureClassToFeatureClass_conversion(prestaged, targetstaged, targetstagedFC, "", "#", config_keyword="")
    EnableEditorTracking_management(targetstaged+"/KHUB.RH."+targetstagedFC, "CreatedUser", "CreatedDate", "LastEditedUser", "LastEditedDate", "", "UTC")
    RegisterAsVersioned_management(targetstaged+"/KHUB.RH."+targetstagedFC, "NO_EDITS_TO_BASE")


def main():
    #exportDevSchemaXML()
    #importDevSchemaXML()
    #EnterpriseModel()
    #exportSubsetDevSchemaXML()
    #DeleteAbstractFields()
    #ValidatetoFileGDB()
    #StageNewEvent()
    #AppendNewEventData()
    #StageAndRegister()
    #StageNewEventSurfaceType()
    StageNewEventNG911Segments()
    
main()

if __name__ == '__main__':
    pass
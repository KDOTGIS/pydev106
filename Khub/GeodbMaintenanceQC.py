'''
Created on Feb 20, 2019
@author: kyleg
'''

'''
KHUB geodatabase maintenance
Post Reconcile Analyze and Compress
Created on Feb 12, 2019
@author: kyleg
'''
#project publication database into webmerc
webmerc="""PROJCS[
    'WGS_1984_Web_Mercator_Auxiliary_Sphere',
    GEOGCS['GCS_WGS_1984',
    DATUM['D_WGS_1984',
    SPHEROID['WGS_1984',6378137.0,298.257223563]],
    PRIMEM['Greenwich',0.0],
    UNIT['Degree',0.0174532925199433]],
    PROJECTION['Mercator_Auxiliary_Sphere'],
    PARAMETER['False_Easting',0.0],
    PARAMETER['False_Northing',0.0],
    PARAMETER['Central_Meridian',0.0],
    PARAMETER['Standard_Parallel_1',0.0],
    PARAMETER['Auxiliary_Sphere_Type',0.0],
    UNIT['Meter',1.0]]"""
transform_method=r"WGS_1984_(ITRF00)_To_NAD_1983"

in_coor_system="""PROJCS[
    'NAD_83_Kansas_Lambert_Conformal_Conic_Feet',
    GEOGCS['GCS_North_American_1983',
    DATUM['D_North_American_1983',
    SPHEROID['GRS_1980',6378137.0,298.257222101]],
    PRIMEM['Greenwich',0.0],
    UNIT['Degree',0.0174532925199433]],
    PROJECTION['Lambert_Conformal_Conic'],
    PARAMETER['false_easting',1312333.333333333],
    PARAMETER['false_northing',0.0],
    PARAMETER['central_meridian',-98.25],
    PARAMETER['standard_parallel_1',37.5],
    PARAMETER['standard_parallel_2',39.5],
    PARAMETER['scale_factor',1.0],
    PARAMETER['latitude_of_origin',36.0],
    UNIT['Foot_US',0.3048006096012192]]"""

def CleanupProc():
    from arcpy import env, Exists, Delete_management
    from datetime import datetime, timedelta
    cleanupfiledate = datetime.now()-timedelta(days = 2)
    #target = "Prod"
    targetlist = ["Prod", "Test"]

    #print(deldbPublished)
    #print(deldbConcurrent)
    for target in targetlist:
        dbPublished = "Publish"+str(target)+str(cleanupfiledate.year).zfill(4)+str(cleanupfiledate.month).zfill(2)+str(cleanupfiledate.day).zfill(2)
        dbConcurrency = "Concurrent"+str(target)+str(cleanupfiledate.year).zfill(4)+str(cleanupfiledate.month).zfill(2)+str(cleanupfiledate.day).zfill(2)
        deldbPublished = "C:\\temp\\"+dbPublished+".gdb"
        deldbConcurrent = "C:\\temp\\"+dbConcurrency+".gdb"
        if Exists(deldbPublished):
            Delete_management(deldbPublished)
            print(deldbPublished + " deleted")
        else:
            print(deldbPublished + " does not exist")

        if Exists(deldbConcurrent):
            Delete_management(deldbConcurrent)
            print(deldbConcurrent+ " deleted")
        else:
            print(deldbConcurrent + " does not exist")
    
def Analyze():
    rh = r'C:\Users\planadm\GISDATA\DbConnections\Prod\RH@KHTransKhub.sde'
    sde = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHTransKHUB.sde'
    from arcpy import AnalyzeDatasets_management
    print("this function analyzes datasets for "+rh + " and " + sde)
    print("analyzing RH and SDE in source")
    AnalyzeDatasets_management(rh, "NO_SYSTEM", "RH.Calibration_Point;RH.Centerline;RH.Centerline_Sequence;RH.Lrs_Edit_Log;RH.Lrs_Event_Behavior;RH.Lrs_Locks;RH.Lrs_Metadata;RH.Redline;", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
    AnalyzeDatasets_management(sde, "SYSTEM", "", "NO_ANALYZE_BASE", "NO_ANALYZE_DELTA", "NO_ANALYZE_ARCHIVE")

def Compress():
    sde = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHTransKHUB.sde'
    from arcpy import Compress_management
    print("compressing "+ sde)
    Compress_management(sde)

def PostAndReconcile():
    sde = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHTransKHUB.sde'
    from arcpy import ReconcileVersions_management
    ReconcileVersions_management(sde, "ALL_VERSIONS", "sde.DEFAULT", "QCADMIN.QC_Lockroot", "LOCK_ACQUIRED", "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", "")
    print("lockroot reconciled to default without conflicts:")

def FullPostAndReconcileDefault():
    sde = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHTransKHUB.sde'
    from arcpy import ReconcileVersions_management, Compress_management, DisconnectUser, AcceptConnections
    print("post and reconcile version with version deletion for " +sde)
    AcceptConnections(sde, False)
    DisconnectUser(sde, "ALL")
    #verListSource = [ver for ver in ListVersions(SDESource) if ver.lower() != 'sde.default' and ver.lower() != 'rh.masterqc']
    print("reconciling MasterQC to Default")
    ReconcileVersions_management(sde, "ALL_VERSIONS", "sde.default", "QCADMIN.QC_Lockroot", "LOCK_ACQUIRED", "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION")
    Compress_management(sde)
    AcceptConnections(sde, True)

def FullPostAndReconcileSourcetoDefaultCollapseVersions():
    sde = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHTransKHUB.sde'
    from arcpy import ReconcileVersions_management, Compress_management, DisconnectUser, AcceptConnections, DeleteVersion_management
    print("post and reconcile version with version deletion for " +sde)
    AcceptConnections(sde, False)
    DisconnectUser(sde, "ALL")
    #verListSource = [ver for ver in ListVersions(SDESource) if ver.lower() != 'sde.default' and ver.lower() != 'rh.masterqc']
    for SourceVersion in rh:
        print(SourceVersion)
        ReconcileVersions_management(sde, "ALL_VERSIONS", "QCADMIN.QC_Lockroot", "RH."+SourceVersion, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION")
        try:
            DeleteVersion_management(sde, SourceVersion)
        except:
            print(SourceVersion+ " deleted after reconcile/post")
    print("reconciling MasterQC to Default")
    ReconcileVersions_management(sde, "ALL_VERSIONS", "sde.default", "RH.MasterQC", "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION")
    try:
        DeleteVersion_management(sde, "RH.MasterQC")
    except:
        print("MasterQC deleted after reconcile/post - OR - if this is the only message, then nothing was done because versions do not exist")
    Compress_management(sde)
    AcceptConnections(sde, True)

def RebuildIndexes():
    print('not set up yet')
    
def PublicateNetworkProd2Target(target):
    from arcpy import env
    from datetime import datetime
    from KhubFCList import NetworksList, EventList, IntersectionList, TestEvents
    from arcpy import (da, FeatureClassToFeatureClass_conversion, ChangePrivileges_management, AddMessage, MakeFeatureLayer_management, 
    AddWarning, Project_management, TruncateTable_management, Append_management, 
    ExecuteError, CreateTable_management, AddField_management, Exists, GetMessages, 
    DisconnectUser, Exists, CreateFileGDB_management, Delete_management)
    pub_event_list = EventList  #TestEvents/EventList - use test events for smaller events lists or testing
    pub_network_list = NetworksList
    
    env.overwriteOutput = True

    #Transactional Database connection to default to copy to publication
    RH_Database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\RH@KHTransKhub.sde'

    if target == 'Prod':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\geo@KHPub.sde'
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHPubProd.sde'
    elif target == 'Test':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\geo@KHPubTest.sde'
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\sde@KHPubtest.sde'
    else:
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\geo@KHPubDev.sde'    
        pub_sdedb = 'C:\Users\planadm\GISDATA\DbConnections\KHDev\sde@KHPubDev.sde'
        #RH_Database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\RH@Khub.sde'
        
    wsruncode = datetime.now()
    dbname = "Publish"+str(target)+str(wsruncode.year).zfill(4)+str(wsruncode.month).zfill(2)+str(wsruncode.day).zfill(2)
    ws= env.workspace=r"C:\\temp\\"+dbname+".gdb"
    if Exists(ws):
        try:
            Delete_management(ws)
        except: 
            raise LicenseError
            CreateFileGDB_management(r"C:/temp", dbname, "CURRENT")
    else:
        CreateFileGDB_management(r"C:/temp", dbname, "CURRENT") 
        
        
    print (pub_database)
    pub_database_path = pub_database
    env.workspace = pub_database
    

    status_table = (pub_database+r"/KHUBPub.GEO.Publication_Status")
    if not Exists(status_table):
        CreateTable_management(pub_database, "Publication_Status")
        AddField_management(status_table, "DATE", "DATE", "", "", "", "Date")
        AddField_management(status_table, "LAYER_NAME", "TEXT", "", "", "", "Layer Name")
        AddField_management(status_table, "STATUS", "TEXT", "", "", "", "Status")
        AddField_management(status_table, "MESSAGE", "TEXT", "", "", "", "Message")
    
    status_fields = ["DATE", "LAYER_NAME", "STATUS", "MESSAGE"]
    

    def update_status_table(status_table, data, fields, status_value, message_value):
        now = datetime.now()
        with da.InsertCursor(status_table, fields) as i_cur:  #@UnresolvedImport
            insert_values = (now, data, status_value, message_value)
            i_cur.insertRow(insert_values)
        del i_cur
            
    i = 1

    for event in pub_event_list:  #for testing add the [2] to enumerate the list of events
        try:
            event_name = event.split(".")[-1]
            print(RH_Database+r'/KHUB.RH.'+ event +" " +event_name)
            DisconnectUser(pub_sdedb, "ALL")
            FeatureClassToFeatureClass_conversion(RH_Database+r'/KHUB.RH.'+ event, ws, str(event_name)+"lyr", where_clause="""((LRSFromDate is null or LRSFromDate<=CURRENT_TIMESTAMP) and (LRSToDate is null or LRSToDate>CURRENT_TIMESTAMP)) or (LRSFromDate>CURRENT_TIMESTAMP and substring(RouteID,4,6) = '599999')""")
            Project_management((ws+r"/"+str(event_name)+"lyr"), (pub_database_path+r'/KHUBPub.GEO.'+event_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
            ChangePrivileges_management((pub_database_path+r'/KHUBPub.GEO.'+event_name), "readonly", View="GRANT", Edit="")
            AddMessage('{0} {1}: {2} {3} {4}'.format(event_name, "copied over publication database", i, "of", len(pub_event_list)))
            update_status_table(status_table, event_name, status_fields, "Overwrite in Publication Database", None)
                
            i += 1    
        except ExecuteError:
            AddWarning('{0} {1}: {2} {3} {4}'.format(event_name, "produced an error", i, "of", len(pub_event_list)))
            message = GetMessages(2)
            update_status_table(status_table, event_name, status_fields, "Error Occurred", message)
            i += 1
            del event
            continue

    for network in NetworksList:
        try:
            network_name = network.split(".")[-1]
            DisconnectUser(pub_sdedb, "ALL")
            FeatureClassToFeatureClass_conversion(RH_Database+r'/KHUB.RH.'+ network, ws, str(network_name), """((LRSFromDate is null or LRSFromDate<=CURRENT_TIMESTAMP) and (LRSToDate is null or LRSToDate>CURRENT_TIMESTAMP)) or (LRSFromDate>CURRENT_TIMESTAMP and substring(RouteID,4,6) = '599999')""")
            Project_management(ws+r"/"+str(network_name), (pub_database_path+r'/KHUBPub.GEO.'+network_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
            ChangePrivileges_management((pub_database_path+r'/KHUBPub.GEO.'+network_name), "readonly", View="GRANT", Edit="")
            AddMessage('{0} {1}'.format(network_name, "overwrote in publication database"))
            update_status_table(status_table, network_name, status_fields, "Overwrite in Publication Database", None)
                
        except ExecuteError:
            AddWarning('{0} {1}'.format(network_name, "produced an error"))
            message = GetMessages(2)
            update_status_table(status_table, network_name, status_fields, "Error Occurred", message)
            del network
            continue
            
    for intersec in IntersectionList:
        #intersections have different lrs date fields than the rest of the Roads and Highways LRS, so get them all to pub (for now)
        try:
            intersec_name = intersec.split(".")[-1]
            DisconnectUser(pub_sdedb, "ALL")

            Project_management(RH_Database+r'/KHUB.RH.'+ intersec, (pub_database_path+r'/KHUBPub.GEO.'+intersec_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
            AddMessage('{0} {1}'.format(intersec_name, "overwrote in publication database"))
            update_status_table(status_table, intersec_name, status_fields, "Overwrite in Publication Database", None)
                
        except ExecuteError:
            AddWarning('{0} {1}'.format(intersec_name, "produced an error"))
            message = GetMessages(2)
            update_status_table(status_table, intersec_name, status_fields, "Error Occurred", message)
            continue
            
            
            
def RecreatePubGDB(target):
    from arcpy import CreateEnterpriseGeodatabase_management, CreateDatabaseConnection_management, CreateDatabaseUser_management, DisconnectUser
    DBName = "KhubPub"
    if target == 'Prod':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\GeoAdmin@KHPubProd.sde'
        pubinstance = r"khdbpubprod\khubpub_prod"

    elif target == 'Test':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\GeoAdmin@KHPubTest.sde'
        pubinstance = r"khdbpubtest\khubpub_test"

    else:
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\GeoAdmin@KHPubDev.sde'   
        pubinstance = r"khdbpubdev\khubpub_dev"
        
    
    sapass = raw_input('sysadmin password')
    sdepass = raw_input('sde password')
    geopass = raw_input('Geo password')
    CreateEnterpriseGeodatabase_management("SQL_Server", pubinstance, DBName, "DATABASE_AUTH", "geo_admin", sapass, "SDE_SCHEMA", "sde", sdepass, "", r"C:\Users\planadm\GISDATA\keycodes\License10.6\sysgen\keycodes")
    CreateDatabaseUser_management(pub_database,  "DATABASE_USER", "geo", geopass)
    CreateDatabaseUser_management(pub_database,  "DATABASE_USER", "readonly", "readonly")
    #geo and readonly users are granted with appropriate privileges in the instance model database, which should therefore be passed to the geodatabse privilege when added to the geodatabase
    
def CreatePrimaryNetwork(target):
    # Create_Dominant_Routes.py (ArcMap Only)
    #  
    # Description: Create concurrency table (WITH STATE SYS INV DIR ROUTES ONLY)
    # and copies Prefixes 1,2,3 Routes to the local geodatabase C:\\\\temp\\CONCURRENT.gdb
    # https://community.esri.com/thread/227849-export-only-dominant-routes-from-lrs
    # 4/13/2020 added dominance dictionary for override of dominant side by side pairs
    # 4/16/2020 added prefix 8 and the ghost suffix for refined control over dominant routes
    # 4/49/2020 added support for dominant flag event control and also eliminated prefix 8 from queries
    # utilizes workspace C:\\\\temp\\CONCURRENT+YYYYMMDD.gdb - attempts to delete if not existing
    # ---------------------------------------------------------------------------
    from datetime import datetime
    #from DomList import OverrideDict
    
    if target == 'Prod':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\Geo@KHPub.sde'
        pubinstance = r"khdbpubprod\khubpub_prod"
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHPubProd.sde'
        tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
        RH_Database = tds

    elif target == 'Test':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\Geo@KHPubTest.sde'
        pubinstance = r"khdbpubtest\khubpub_test"
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\sde@KHPubtest.sde'
        tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
        RH_Database = tds

    else:
        target = 'Dev'
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\Geo@KHPubDev.sde'   
        pubinstance = r"khdbpubdev\khubpub_dev"
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\sde@KHPubDev.sde'
        tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
        RH_Database = tds
   
    from arcpy import (env, da, CreateFileGDB_management, AddMessage, AddWarning, Exists, MakeRouteEventLayer_lr, DisconnectUser,
    CheckExtension, CheckOutExtension, CreateRoutes_lr, ChangePrivileges_management, CopyFeatures_management, Delete_management, 
    MultipartToSinglepart_management, Copy_management, Merge_management, MakeTableView_management, Erase_analysis, ExecuteError, 
    GetMessages, LocateFeaturesAlongRoutes_lr, CheckInExtension, MakeFeatureLayer_management, FeatureClassToFeatureClass_conversion, 
    CreateTable_management, Append_management, AddField_management, CalculateField_management, TableToTable_conversion, Project_management,
    Dissolve_management, Statistics_analysis, AddJoin_management, RemoveJoin_management, AddIndex_management, SelectLayerByAttribute_management,
    OverlayRouteEvents_lr)
    from datetime import datetime

    wsruncode = datetime.now()
    dbname = "CONCURRENT"+str(target)+str(wsruncode.year).zfill(4)+str(wsruncode.month).zfill(2)+str(wsruncode.day).zfill(2)
    ws= env.workspace=r"C:\\temp\\"+dbname+".gdb"
    if Exists(ws):
        try:
            Delete_management(ws)
            CreateFileGDB_management(r"C:/temp", dbname, "CURRENT")
        except: 
            raise LicenseError
            CreateFileGDB_management(r"C:/temp", dbname, "CURRENT")
    else:
        CreateFileGDB_management(r"C:/temp", dbname, "CURRENT")

    env.MResolution = 0.000000018939394
    env.MTolerance = 0.000000621369949
    #arcpy.env.XYTolerance="0.003280833333333 US Survey Foot"
    #arcpy.env.XYResolution="0.0001 US Survey Foot"

    db_connection=RH_Database
    env.overwriteOutput= True;

    try:
        if CheckExtension ("Highways")== "Available":

        #Check out the Network Analyst extension
            CheckOutExtension("Highways")
        else:
            raise LicenseError
    except LicenseError:
        print ("Roads & Highways Extension not available")
        sys.exit()

    LRSCounty = db_connection+"\\KHUB.RH.LRS_County"
    KHUBRoutes = "KHUBRoutes"
    KHUBRoutesLyr="KHUBRoutesLyr"

    from locref import CalculateRouteConcurrencies
    whereClauseAll= "Prefix IN ('1','2','3','4','5','8')"
    MakeFeatureLayer_management (LRSCounty,KHUBRoutesLyr,whereClauseAll)
    CalculateRouteConcurrencies(KHUBRoutesLyr, ws+r"\\concurr_tbl_all", "", "FIND_DOMINANCE")
    AddIndex_management(ws+"\\concurr_tbl_all", "SectionId", "SectionIdx")
    AddField_management("concurr_tbl_all", "Prefix", "TEXT", "", "", "1", "", "NULLABLE", "NON_REQUIRED", "")

    CalculateField_management("concurr_tbl_all", "Prefix", "Mid( [RouteId],4,1 )", "VB", "")

    AddField_management(ws + "\\concurr_tbl_all", "DominantOverrideFlag", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    #dominance flag event is at C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde\KHUB.RH.ev_ConcurrentFlag

    #the DW table would be a nice feature addition
    #instead of selecting these segments individually use a spatial/LRS process to select segments from concurr all table

    TableToTable_conversion(db_connection+"\\KHUB.RH.ev_ConcurrentFlag", ws, "ConcurrentFlag")
    OverlayRouteEvents_lr(ws+r"\\ConcurrentFlag", "RouteID POINT measure", ws+r"\\concurr_tbl_all", "RouteId LINE FromMeasure ToMeasure", "INTERSECT", ws+r"\\ConcFlagsOverlayConcurrTbl", "RouteID POINT measure", "ZERO", "FIELDS", "INDEX")
    AddIndex_management(ws+"\\ConcFlagsOverlayConcurrTbl", "SectionId", "SectionId1")


    CalculateField_management("ConcFlagsOverlayConcurrTbl", "DominantFlag", "1", "VB", "")
    CalculateField_management("ConcFlagsOverlayConcurrTbl", "DominantOverrideFlag", "1", "VB", "")
    #Calcualte hte previously dominant values across the section to 0

    MakeTableView_management(ws+"\\ConcFlagsOverlayConcurrTbl", "ConcFlagsOverlayConcurrTbl_View")
    MakeTableView_management(ws+"\\concurr_tbl_all", "concurr_tbl_all_View")
    #this join may result in one to many or many to many results
    AddJoin_management("concurr_tbl_all_View", "SectionId", "ConcFlagsOverlayConcurrTbl_View", "SectionId", "KEEP_ALL")
    #join and select attribute and drop the joins out, and recalc flags
    #do it again because the first recalcalc will break second recalc logic
    #this method will not flag previously nonprimary routes as overriden
    #select and set the new dominant routes
    #SelectLayerByAttribute_management("concurr_tbl_all_View", "NEW_SELECTION", "ConcFlagsOverlayConcurrTbl.DominantOverrideFlag=1 AND ConcFlagsOverlayConcurrTbl.DominantFlag=1 AND ConcFlagsOverlayConcurrTbl.RouteID = concurr_tbl_all.RouteId")
    MakeTableView_management("concurr_tbl_all_View", "concurr_tbl_alt_View", "ConcFlagsOverlayConcurrTbl.DominantOverrideFlag=1 AND ConcFlagsOverlayConcurrTbl.DominantFlag=1 AND ConcFlagsOverlayConcurrTbl.RouteID = concurr_tbl_all.RouteId")
    SelectLayerByAttribute_management("concurr_tbl_alt_View", "NEW_SELECTION", "1=1")
    #RemoveJoin_management("concurr_tbl_alt_View", "")
    CalculateField_management("concurr_tbl_alt_View", "concurr_tbl_all.DominantFlag", "1", "VB", "")
    CalculateField_management("concurr_tbl_alt_View", "concurr_tbl_all.DominantOverrideFlag", "1", "VB", "")
    SelectLayerByAttribute_management("concurr_tbl_alt_View", "CLEAR_SELECTION")
    #RH dumb dominants to non dominant
    AddJoin_management("concurr_tbl_all_View", "SectionId", "ConcFlagsOverlayConcurrTbl", "SectionId", "KEEP_ALL")
    MakeTableView_management("concurr_tbl_all_View", "concurr_tbl_alt_View2", "concurr_tbl_all.DominantFlag = 1 AND ConcFlagsOverlayConcurrTbl.DominantOverrideFlag=1 AND ConcFlagsOverlayConcurrTbl.DominantFlag=1 AND ConcFlagsOverlayConcurrTbl.RouteID NOT LIKE concurr_tbl_all.RouteId")
    SelectLayerByAttribute_management("concurr_tbl_alt_View2", "NEW_SELECTION", "1 = 1")
    #RemoveJoin_management("concurr_tbl_all_View", "")
    CalculateField_management("concurr_tbl_alt_View2", "concurr_tbl_all.DominantFlag", "0", "VB", "")
    CalculateField_management("concurr_tbl_alt_View2", "concurr_tbl_all.DominantOverrideFlag", "1", "VB", "")
    SelectLayerByAttribute_management("concurr_tbl_alt_View2", "CLEAR_SELECTION")

    print ("concurrent table created")
    DisconnectUser(pub_sdedb, "ALL")
    if Exists(pub_database+r'/KHUBPub.GEO.RouteConcurrency'):  
        #make a copy to update in TDSOutput Route Concurrency in Tdsuser schema
        Delete_management(pub_database+r'/KHUBPub.GEO.RouteConcurrency')
    else:
        pass
    TableToTable_conversion(ws+"\\concurr_tbl_all", pub_database, "RouteConcurrency", "ToDate IS NULL")
    #make a copy to update in TDSOutput Route Concurrency in Tdsuser schema
    ChangePrivileges_management((pub_database+r'/KHUBPub.GEO.RouteConcurrency'), "readonly", View="GRANT", Edit="")
    FeatureClassToFeatureClass_conversion(KHUBRoutesLyr, ws, KHUBRoutes, "LRSToDate IS NULL AND Prefix IN ( '1', '2', '3','4','5') ")
    #edit 4/7/2020 add table, flag list of overrides to concurrent, and recalculate dominance overrides


    #CheckInExtension("Highways")
    print("copy fc completed")


    # Local variables:
    TargetRoutesPrefix1235 = ws+"\\KHUBRoutes"
    concurr_tbl = ws+"\\concurr_tbl_all"
    DominantFlag1Feat = ws+"\\DominantFlag1Feat"
    TargetRoutes_Erase = ws+"\\TargetRoutes_Erase"
    TargetRoutes_Erase_LocateFea = ws+"\\TargetRoutes_Erase_LocateFea"
    TargetRoutes_Erase_withMP = ws+"\\TargetRoutes_Erase_withMP"
    SegmentsToCreateRoutes = ws+"\\SegmentsToCreateRoutes"
    mergeset = ws+"\\mergeset"
    mergesetCopy = ws+"\\mergesetCopy"
    #DominantRoutesCreated = ws+"\\DominantRoutesCreated"
    DominantRoutesAll = ws+"\\DominantRoutesAll"
    DominantRtesSinglePart=ws+"\\DominantRtesSinglePart"

    concurr_tbl_View = "concurr_tbl_View"
    concurr_tbl_View_Events = "concurr_tbl_View Events"
    Output_Event_Table_Properties = "RID LINE FMEAS TMEAS"
    TargetRoutes_Erase_LocateFea_Events = "TargetRoutes_Erase_LocateFea_Events"
    mergesetCopy_Layer = "mergesetCopy_Layer"

    ##############################create Dominant route segments###########################################################

    # Process: Make Table View to select subset with query to include only  LRS_end_date is  null, dominant flag=1
    MakeTableView_management(concurr_tbl, concurr_tbl_View, "FromMeasure IS NOT NULL AND ToMeasure IS NOT NULL AND ToDate IS NULL AND DominantFlag = 1 AND RouteId NOT LIKE 'KTA*' AND Prefix IN ('1','2','3','4','5')")
    MakeRouteEventLayer_lr(TargetRoutesPrefix1235, "RouteId", concurr_tbl_View, "RouteId LINE FromMeasure ToMeasure", concurr_tbl_View_Events, "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
    CopyFeatures_management(concurr_tbl_View_Events, DominantFlag1Feat, "", "0", "0", "0")

    ###############Erase analysis to get route segments that do not carry any route##########################################

    # Process: Erase, input is all routes, erase feature is dominant routes#######################################
    Erase_analysis(TargetRoutesPrefix1235, DominantFlag1Feat, TargetRoutes_Erase, "")
    # Process: The noncarrying route segments are run thr LFAR-Locate Features Along Routes to get LRS milepoints, output is a table
    LocateFeaturesAlongRoutes_lr(TargetRoutes_Erase, TargetRoutesPrefix1235, "RouteId", "0 Feet", TargetRoutes_Erase_LocateFea, Output_Event_Table_Properties, "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    MakeRouteEventLayer_lr(TargetRoutesPrefix1235, "RouteId", TargetRoutes_Erase_LocateFea, "rid LINE fmeas tmeas", TargetRoutes_Erase_LocateFea_Events, "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
    CopyFeatures_management(TargetRoutes_Erase_LocateFea_Events, TargetRoutes_Erase_withMP, "", "0", "0", "0")
    print("completed erase fc, dominant fc")
    Copy_management(TargetRoutes_Erase_withMP, SegmentsToCreateRoutes, "FeatureClass")

    # Process: Add Field ToMeasure. LFAR GIVES IT AS TMEAS
    AddField_management(SegmentsToCreateRoutes, "ToMeasure", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management(SegmentsToCreateRoutes, "ToMeasure", "[TMEAS]", "VB", "")

    AddField_management(SegmentsToCreateRoutes, "FromMeasure", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management(SegmentsToCreateRoutes, "FromMeasure", "[FMEAS]", "VB", "")

    # Process: Merge output of erase, and the dominant rte seg, COMMON FIELDS WILL BE RouteId, FromMeasure,ToMeasure
    Merge_management([SegmentsToCreateRoutes,DominantFlag1Feat], mergeset)


                           
    print ("merge completed")

    CopyFeatures_management(mergeset, mergesetCopy, "", "0", "0", "0")
    MakeFeatureLayer_management(mergesetCopy, mergesetCopy_Layer, "\"Shape_Length\" > 0")

    CreateRoutes_lr(mergesetCopy_Layer, "RouteId", DominantRoutesAll, "TWO_FIELDS", "FromMeasure", "ToMeasure", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")

    print ("routes creation completed")

    #append local routes from transactioal to the mergeset
    MakeFeatureLayer_management(LRSCounty, "LRS_County_Layer678", "Prefix IN ('6', '7') AND LRSToDate is null")
    Append_management('LRS_County_Layer678', DominantRoutesAll, "NO_TEST")

    # Create singlepart features
    MultipartToSinglepart_management(DominantRoutesAll,DominantRtesSinglePart)
    AddField_management(DominantRtesSinglePart, "MinMeas", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(DominantRtesSinglePart, "MaxMeas", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management(DominantRtesSinglePart, "MaxMeas", "round(!Shape.extent.MMax!,7)  ", "PYTHON_9.3", "")
    CalculateField_management(DominantRtesSinglePart, "MinMeas", "round(!Shape.extent.MMin!,7)  ", "PYTHON_9.3", "")
    print ("single parts fc with measures created ")

    #more local variables for just the state route part
    TargetRoutesPrefix123 = ws+"\\SHSRoutes"
    whereClauseSHSPrimaryInv= "Substring(RouteId, 4, 1) in ('1', '2', '3') AND Substring(RouteID, 11, 1) = '0'"
    whereClauseSHS = "LRSToDate IS NULL AND Prefix in ('1', '2', '3')"
    SHSPI = ws+"\\SHSDomInv"
    countyDissolve = ws+ "\\LRS_County_Dissolve"
    StateRoutes=ws+"\\LRS_State"
    CntyDIOnState = ws+"\\CountyDomOnState"
    MinStatCntyDIOnState = ws+"\\CountyDomOnState_Statistics"
    #this above shouldnt really be a variable, see line 460 and the join at 469 and calculalte at 470.  The name needs to be 


    # Create State Routes from County Routes - adding @427 on 12/24/2019
    FeatureClassToFeatureClass_conversion(KHUBRoutesLyr, ws, "SHSRoutes", whereClauseSHS)
    FeatureClassToFeatureClass_conversion(DominantRoutesAll, ws, "SHSDomInv", whereClauseSHSPrimaryInv)
    #FeatureClassToFeatureClass_conversion (TargetRoutesPrefix1235, TargetRoutesPrefix123, whereClauseSHS)
    #dissolve needs to filter to just SHS, prefix 4 and 5 should not be included
    Dissolve_management(TargetRoutesPrefix123, countyDissolve, "Prefix;RouteNum;Suffix;UniqueId;InvDir", "", "MULTI_PART", "DISSOLVE_LINES")
    AddField_management(countyDissolve, "StateRouteID", "TEXT", "", "", "12", "", "NULLABLE", "NON_REQUIRED", "")
    MakeFeatureLayer_management(countyDissolve, "StateUnique", "UniqueID is not null")
    MakeFeatureLayer_management(countyDissolve, "StateMainline", "UniqueID is null")
    CalculateField_management("StateMainline", "StateRouteID", "[Prefix]+ Right([RouteNum],3)+ [Suffix]+ [InvDir]", "VB", "")
    CalculateField_management("StateUnique", "StateRouteID", "[Prefix]+ Right([RouteNum],3)+ [Suffix]+ [InvDir]+ [UniqueId]", "VB", "")
    AddField_management(countyDissolve, "FromMeas", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(countyDissolve, "ToMeas", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management(countyDissolve, "FromMeas", "0", "VB", "")
    CalculateField_management(countyDissolve, "ToMeas", "[Shape_Length]/5280", "VB", "")
    CreateRoutes_lr(countyDissolve, "StateRouteID", StateRoutes, "TWO_FIELDS", "FromMeas", "ToMeas", "LOWER_LEFT", "1", "0", "IGNORE", "INDEX")
    LocateFeaturesAlongRoutes_lr(SHSPI, StateRoutes, "StateRouteID", "0 Feet", CntyDIOnState, "RID LINE FMEAS TMEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    MakeTableView_management(CntyDIOnState, "CountyDomOnState_Matched", "Substring(RID, 2, 5) = Substring(RouteID, 7, 5) AND Substring(RID, 1, 1) = Substring( RouteId, 4, 1)", "", "#")
    Statistics_analysis("CountyDomOnState_Matched", MinStatCntyDIOnState, "FMEAS MIN;TMEAS MAX;OBJECTID COUNT", "RouteId;RID")
    #add index here
    #join the state measures into Dominant Routes All & SinglePart where they exist as state routes
    #also output, projected, the State Routes overlapping into the Publication Database as the State Route LRS - consider constructing Fields as used in the LRM System
    MakeFeatureLayer_management(DominantRtesSinglePart, "StateMeasures", whereClauseSHSPrimaryInv)
    AddField_management("StateMeasures", "FromState", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("StateMeasures", "ToState", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("StateMeasures", "FromCounty", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("StateMeasures", "ToCounty", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("StateMeasures", "FromCounty", "[MinMeas]", "VB")
    CalculateField_management("StateMeasures", "ToCounty", "[MaxMeas]", "VB")
    AddIndex_management("DominantRtesSinglePart", "RouteID", "RouteID1")
    AddIndex_management(MinStatCntyDIOnState, "RouteID", "RouteID2")
    MakeTableView_management(MinStatCntyDIOnState, "JoinStats")
    #AddJoin_management("StateMeasures", "RouteId", "JoinStats", "RouteId", "KEEP_ALL")
    #CalculateField_management("StateMeasures", "DominantRtesSinglePart.FromState", "[DominantRtesSinglePart.MinMeas] + [CountyDomOnState_Statistics.MIN_FMEAS]", "VB")
    #CalculateField_management("StateMeasures", "DominantRtesSinglePart.ToState", "[DominantRtesSinglePart.MaxMeas] + [CountyDomOnState_Statistics.MIN_FMEAS]", "VB")
    #RemoveJoin_management("StateMeasures", "CountyDomOnState_Statistics")
    #output these results to the publication database
    DisconnectUser(pub_sdedb, "ALL")
    Project_management(DominantRoutesAll, (pub_database+r'/KHUBPub.GEO.'+"LRS_County_Primary"), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
    FeatureClassToFeatureClass_conversion(DominantRoutesAll, pub_database, "LRS_County_Primary_LCC", "")
    FeatureClassToFeatureClass_conversion(DominantRtesSinglePart, pub_database, "LRS_County_PrimarySP_LCC", "")
    FeatureClassToFeatureClass_conversion(LRSCounty, pub_database, "LRS_Turnpike", "(LRSFromDate is null or LRSFromDate<=CURRENT_TIMESTAMP) and (LRSToDate is null or LRSToDate>CURRENT_TIMESTAMP) AND RouteID like 'KTA%'")
    #adding 5/18/20 creation of LRS_Siate feature class NETWORKS to pub
    #CreateRoutes_lr("KHubPub.GEO.ev_StateOnCounty", "StateRouteId", pub_database+r'/KHUBPub.GEO.'+"LRS_State_Primary_LCC", "TWO_FIELDS", "FromState", "ToState", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    Project_management(DominantRtesSinglePart, (pub_database+r'/KHUBPub.GEO.'+"LRS_County_PrimarySP"), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
    Project_management(StateRoutes, (pub_database+r'/KHUBPub.GEO.'+"LRS_State"), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
    ChangePrivileges_management((pub_database+r'/KHUBPub.GEO.LRS_County_Primary'), "readonly", View="GRANT", Edit="")
    ChangePrivileges_management((pub_database+r'/KHUBPub.GEO.LRS_County_PrimarySP'), "readonly", View="GRANT", Edit="")
    ChangePrivileges_management((pub_database+r'/KHUBPub.GEO.LRS_State'), "readonly", View="GRANT", Edit="")
    ChangePrivileges_management((pub_database+r'/KHUBPub.GEO.LRS_County_PrimarySP_LCC'), "readonly", View="GRANT", Edit="")
    ChangePrivileges_management((pub_database+r'/KHUBPub.GEO.LRS_County_Primary_LCC'), "readonly", View="GRANT", Edit="")
    status_table = (pub_database+r"/KHUBPub.GEO.Publication_Status")
    status_fields = ["DATE", "LAYER_NAME", "STATUS", "MESSAGE"]
    def update_status_table(status_table, data, fields, status_value, message_value):
        now = datetime.now()
        with da.InsertCursor(status_table, fields) as i_cur:  #@UnresolvedImport
            insert_values = (now, data, status_value, message_value)
            i_cur.insertRow(insert_values)
        del i_cur
            
    i = 1
    try:
         AddMessage('{0} {1}: {2} {3} {4}'.format("Primary Routes", "Primary routes updated in publication database", i, "of", len("Primary Routes")))
         update_status_table(status_table, "Primary Routes", status_fields, "Primary routes updated in publication database", None)
                

    except ExecuteError:
            AddWarning('{0} {1}: {2} {3} {4}'.format("Primary Routes", "produced an error", i, "of", len("Primary Routes")))
            message = GetMessages(2)
            update_status_table(status_table, "Primary Routes", status_fields, "Error Occurred", message)
            i += 1


    
def LYRS2Pub(target):
    # this function creates an output to publication of the pavement layers equivalent to LYRS in CANSYS.  There are over 96,000 records of pavement layers, and process takes over an hour to write the dataset to publication   
    from datetime import datetime
    #add datetime reporting/printing to check processing time on server
    #add logging and error messaging
    #add Change Privliege Management to add readonly privilege to output
    if target == 'Prod':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\Geo@KHPub.sde'
        pubinstance = r"khdbpubprod\khubpub_prod"
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHPubProd.sde'
        tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
        RH_Database = tds

    elif target == 'Test':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\Geo@KHPubTest.sde'
        pubinstance = r"khdbpubtest\khubpub_test"
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\sde@KHPubtest.sde'
        tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
        RH_Database = tds

    else:
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\Geo@KHPubDev.sde'   
        pubinstance = r"khdbpubdev\khubpub_dev"
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\sde@KHPubDev.sde'
        tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
        RH_Database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\RH@Khub.sde'
        
    from arcpy import env, MakeRouteEventLayer_lr, FeatureClassToFeatureClass_conversion, DisconnectUser, Delete_management, Exists
    
    env.MResolution = 0.000000018939394
    env.MTolerance = 0.000000621369949
    DisconnectUser(pub_sdedb, "ALL")
    if Exists(pub_database+r'/KHUBPub.GEO.ev_PavementLayers'):  
        Delete_management(pub_database+r'/KHUBPub.GEO.ev_PavementLayers')
    else:
        pass
    MakeRouteEventLayer_lr(tds+r"/KHUB.RH.LRS_County", "RouteId", tds+r"/KHUB.TDSUser.PS_PLV_Def", "RouteID LINE FromMeasure ToMeasure", r"PavementLayers", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
    FeatureClassToFeatureClass_conversion("PavementLayers", pub_database, "ev_PavementLayers")

def StateRefpost(target):
    #add state LRM derivations and add state route ID to reference post 
    from datetime import datetime

    if target == 'Prod':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\Geo@KHPub.sde'
        pubinstance = r"khdbpubprod\khubpub_prod"
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHPubProd.sde'
        tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
        RH_Database = tds

    elif target == 'Test':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\Geo@KHPubTest.sde'
        pubinstance = r"khdbpubtest\khubpub_test"
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\sde@KHPubtest.sde'
        tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
        RH_Database = tds

    else:
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\Geo@KHPubDev.sde'   
        pubinstance = r"khdbpubdev\khubpub_dev"
        pub_sdedb = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\sde@KHPubDev.sde'
        tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
        RH_Database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\RH@Khub.sde'
        
    from arcpy import (env, MakeRouteEventLayer_lr, FeatureClassToFeatureClass_conversion, DisconnectUser, Delete_management, Exists,
    CreateRoutes_lr)
    env.MResolution = 0.000000018939394
    env.MTolerance = 0.000000621369949
    env.overwriteOutput = True
    #the turnpike should have copied
    #create the LRS_State LCC layers
    CreateRoutes_lr(RH_Database+r"/KHUB.RH.ev_StateOnCounty", "StateRouteId", pub_database+r"\\KHubPub.GEO.LRS_State_LCC", "TWO_FIELDS", "FromState", "ToState", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    StatePrimaryInventory = "(LRSFromDate is null or LRSFromDate<=CURRENT_TIMESTAMP) and (LRSToDate is null or LRSToDate>CURRENT_TIMESTAMP) AND Substring(StateRouteId, 6, 1) = '0' AND (DominantFlag = '1' or DominantFlag is null)"
    MakeFeatureLayer_management(RH_Database+r"/KHUB.RH.ev_StateOnCounty", "ev_StateOnCounty_prim_inv", StatePrimaryInventory)
    CreateRoutes_lr("ev_StateOnCounty_prim_inv", "StateRouteId", pub_database+r"\LRS_State_Primary_LCC", "TWO_FIELDS", "FromState", "ToState", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    #locate the refposts along the state lrm primary inventory route
    LocateFeaturesAlongRoutes_lr("ev_ReferencePostlyr", "LRS_State_Primary_LCC", "StateRouteId", "50 Feet", "C:/temp/PublishProd20200518.gdb/RefpostState", out_event_properties="StateRouteId POINT State_Meas", route_locations="FIRST", distance_field="DISTANCE", zero_length_events="ZERO", in_fields="FIELDS", m_direction_offsetting="M_DIRECTON")
    #join the LFAR table and copy to pub with the joined fields
    #delete some of hte extra joined fields
    #LFAR refposts to the turnpike
    #join the LFAR to the state refposts
    #recalculate the turnpike route refposts measures and routes
    
    SelectLayerByAttribute_management(in_layer_or_view="KHubPub.GEO.ev_ReferencePost", selection_type="NEW_SELECTION", where_clause="RefpostKTA.StateRouteId = 'KTA10099900' AND KHubPub.GEO.ev_ReferencePost.ReferencePost < 240")

    
def maintest():
    #LYRS2Pub('Test')
    Analyze()
    PostAndReconcile()  ##enable for nightly run
    Compress()          ##enable for nightly run
    Analyze()

def main():
    Analyze()
    PostAndReconcile()  ##enable for nightly run
    Compress()          ##enable for nightly run
    Analyze()
    #RebuildIndexes() #in testing
    #RecreatePubGDB('Dev')
    #RecreatePubGDB('Prod')
    CreatePrimaryNetwork('Prod')
    PublicateNetworkProd2Target('Prod') ## update prod transactional data to publication in 'dev', 'test', or 'prod'
    #StateRefpost('Test')
    CreatePrimaryNetwork('Test')
    PublicateNetworkProd2Target('Test')  
    #PublicateNetworkProd2Target('Dev') 
    #CreatePrimaryNetwork('Dev')
    #LYRS2Pub('Prod')
    CleanupProc()
    
    print("run completed" )
def main2():
    #PublicateNetworkProd2Target('Prod')  
    #CreatePrimaryNetwork('Test')
    #PublicateNetworkProd2Target('Dev') 
    #CreatePrimaryNetwork('Dev')
	LYRS2Pub('Prod')
    #CleanupProc()

main()

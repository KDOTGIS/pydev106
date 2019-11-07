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
QC =  r'C:\Users\planadm\GISDATA\DbConnections\Prod\qc@KHTransKHUB.sde'
sde = r'C:\Users\planadm\GISDATA\DbConnections\Prod\sde@KHTransKHUB.sde'
tds = r'C:\Users\planadm\GISDATA\DbConnections\Prod\TDSUser@KHProd.sde'
rh = r'C:\Users\planadm\GISDATA\DbConnections\Prod\rh@KHTransKHUB.sde'

from arcpy import DisconnectUser, DeleteVersion_management, AcceptConnections, RebuildIndexes_management

def Analyze():

    from arcpy import AnalyzeDatasets_management
    print("this function analyzes datasets for "+rh + " and " + sde)
    print("analyzing RH and SDE in source")
    AnalyzeDatasets_management(rh, "NO_SYSTEM", "RH.Calibration_Point;RH.Centerline;RH.Centerline_Sequence;RH.Lrs_Edit_Log;RH.Lrs_Event_Behavior;RH.Lrs_Locks;RH.Lrs_Metadata;RH.Redline;", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
    AnalyzeDatasets_management(sde, "SYSTEM", "", "NO_ANALYZE_BASE", "NO_ANALYZE_DELTA", "NO_ANALYZE_ARCHIVE")

def Compress():
    from arcpy import Compress_management
    print("compressing "+ sde)
    Compress_management(sde)

def PostAndReconcile():
    from arcpy import ReconcileVersions_management
    ReconcileVersions_management(sde, "ALL_VERSIONS", "sde.DEFAULT", "QCADMIN.QC_Lockroot", "LOCK_ACQUIRED", "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", "")
    print("lockroot reconciled to default without conflicts:")

def FullPostAndReconcileDefault():
    from arcpy import ReconcileVersions_management, Compress_management
    print("post and reconcile version with version deletion for " +sde)
    AcceptConnections(sde, False)
    DisconnectUser(sde, "ALL")
    #verListSource = [ver for ver in ListVersions(SDESource) if ver.lower() != 'sde.default' and ver.lower() != 'rh.masterqc']
    print("reconciling MasterQC to Default")
    ReconcileVersions_management(sde, "ALL_VERSIONS", "sde.default", "QCADMIN.QC_Lockroot", "LOCK_ACQUIRED", "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION")
    Compress_management(sde)
    AcceptConnections(sde, True)

def FullPostAndReconcileSourcetoDefaultCollapseVersions():
    from arcpy import ReconcileVersions_management, Compress_management
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
    print('rebuilding source network indexes')
    RebuildIndexes_management(rh, "NO_SYSTEM", "KhubSourceNet.RH.Calibration_Point;KhubSourceNet.RH.Centerline;KhubSourceNet.RH.Centerline_Sequence;KhubSourceNet.RH.Lrs_Edit_Log;KhubSourceNet.RH.Lrs_Event_Behavior;KhubSourceNet.RH.Lrs_Locks;KhubSourceNet.RH.Lrs_Metadata;KhubSourceNet.RH.Redline;KhubSourceNet.RH.SourceRoutes", "ALL")
    print('rebuilding target network indexes')
    RebuildIndexes_management(sde, "SYSTEM", "ROADS.SDE.ALL_ROADS_STITCH_POINTS;ROADS.SDE.AUTHORITATIVEBOUNDARY_NG911;ROADS.SDE.All_Road_Centerlines;ROADS.SDE.All_Road_Centerlines_1ungeneralized;ROADS.SDE.All_Road_Centerlines_D1;ROADS.SDE.All_Road_Centerlines_D1_I25_Final;ROADS.SDE.All_Road_Centerlines_D1_I25_Final_add_np;ROADS.SDE.CMLRS_2017;ROADS.SDE.COUNTYBOUNDARY_NG911;ROADS.SDE.CRND;ROADS.SDE.CRND25;ROADS.SDE.CalibPtD1_detail;ROADS.SDE.CalibrationPointD1_point;ROADS.SDE.CalibrationPointSource;ROADS.SDE.CalibrationPointSourceOrig;ROADS.SDE.D1_UABInt;ROADS.SDE.END_COUNTY;ROADS.SDE.END_D1_COUNTY;ROADS.SDE.END_D1_C_D;ROADS.SDE.END_D1_C_Events;ROADS.SDE.END_D1_RM_D;ROADS.SDE.END_D1_RM_Events;ROADS.SDE.GATES_NG911;ROADS.SDE.HPMS_Ramps;ROADS.SDE.Junctions;ROADS.SDE.KhubEventsFeaturesFinal;ROADS.SDE.MARKUP_LINE;ROADS.SDE.MARKUP_POINT;ROADS.SDE.MUNICIPALBOUNDARY_NG911;ROADS.SDE.NG911_ROAD_CHANGES;ROADS.SDE.NSND;ROADS.SDE.Nusys25;ROADS.SDE.PARCELS_NG911;ROADS.SDE.RM_Routes;ROADS.SDE.ROADALIAS_NG911;ROADS.SDE.ROADCENTERLINE_NG911;ROADS.SDE.RiderJoin;ROADS.SDE.RiderSource;ROADS.SDE.Rural_Classified;ROADS.SDE.SOURCE_ROUTES;ROADS.SDE.SS_NonPrimarySegmentIDs;ROADS.SDE.START_COUNTY;ROADS.SDE.START_D1_COUNTY;ROADS.SDE.START_D1_C_D;ROADS.SDE.START_D1_C_Events;ROADS.SDE.START_D1_RM_D;ROADS.SDE.START_D1_RM_Events;ROADS.SDE.SourcePoint_GenerateNearTableIKURMC;ROADS.SDE.URBAN_BOUNDARIES;ROADS.SDE.nonMono_IKU;ROADS.SDE.nonMono_RMC;ROADS.sde.LOCAL_ROAD_NUMBERING;ROADS.sde.LOCAL_ROAD_NUMBERING_D1;ROADS.sde.NP_SourceRouteKey;ROADS.sde.NP_TargetRouteKey;ROADS.sde.NonZeroStartMeasure;ROADS.sde.SDE_compress_log;ROADS.sde.updateMP_MOD1;Roads.SDE.INTR_CANSYS;Roads.SDE.INTR_NUSYS;Roads.SDE.Nusys;Roads.SDE.VIDEOLOG_CURRENT_LANETRACE;Roads.SDE.VIDEOLOG_CURRENT_RAMPTRACE", "ALL")

def PublicateNetworkProd2Target(target):
    from arcpy import env
    from datetime import datetime
    env.overwriteOutput = True
    #project publication database into webmerc
    webmerc="""PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"""
    transform_method=r"WGS_1984_(ITRF00)_To_NAD_1983"
    in_coor_system="""PROJCS['NAD_83_Kansas_Lambert_Conformal_Conic_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['false_easting',1312333.333333333],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-98.25],PARAMETER['standard_parallel_1',37.5],PARAMETER['standard_parallel_2',39.5],PARAMETER['scale_factor',1.0],PARAMETER['latitude_of_origin',36.0],UNIT['Foot_US',0.3048006096012192]]"""
    #Transactional Database connection to default to copy to publication
    RH_Database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\RH@KHTransKhub.sde'
    
    if target == 'Prod':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\geo@KHPub.sde'
    elif target == 'Test':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\geo@KHPubTest.sde'
    else:
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\geo@KHPubDev.sde'    
    print (pub_database)
    pub_database_path = pub_database
    env.workspace = pub_database
    from KhubFCList import NetworksList, EventList, IntersectionList, TestEvents
    from arcpy import da, CopyFeatures_management, ChangePrivileges_management, AddMessage, MakeFeatureLayer_management, AddWarning, Project_management, TruncateTable_management, Append_management, ExecuteError, CreateTable_management, AddField_management, Exists, GetMessages
    pub_event_list = EventList  #TestEvents/EventList - use test events for smaller events lists or testing
    pub_network_list = NetworksList

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
            
            
            if event_name not in pub_event_list:
                MakeFeatureLayer_management(RH_Database+r'/KHUB.RH.'+ event, event, where_clause="""(LRSFromDate is null or LRSFromDate<=CURRENT_TIMESTAMP) and (LRSToDate is null or LRSToDate>CURRENT_TIMESTAMP)""")
                Project_management((event), (pub_database_path+r'/KHUBPub.GEO.'+event_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
                #CopyFeatures_management((RH_Database+r'/KHUB.RH.'+ event), (pub_database_path+r'/KHUBPub.GEO.'+event_name)) 
                ChangePrivileges_management((pub_database_path+r'/KHUBPub.GEO.'+event_name), "readonly", View="GRANT", Edit="")
                AddMessage('{0} {1}: {2} {3} {4}'.format(event_name, "copied to publication database", i, "of", len(EventList)))
                update_status_table(status_table, event_name, status_fields, "Copied to Publication Database", None)
                
            else:
                MakeFeatureLayer_management(RH_Database+r'/KHUB.RH.'+ event, event, where_clause="""(LRSFromDate is null or LRSFromDate<=CURRENT_TIMESTAMP) and (LRSToDate is null or LRSToDate>CURRENT_TIMESTAMP)""")
                Project_management((event), (pub_database_path+r'/KHUBPub.GEO.'+event_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
                #Project_management((RH_Database+r'/KHUB.RH.'+ event), (pub_database_path+r'/KHUBPub.GEO.'+event_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
                #TruncateTable_management((pub_database_path+r'/KHUBPub.GEO.'+event_name))
                #Append_management((RH_Database+r'/KHUB.RH.'+ event), (pub_database_path+r'/KHUBPub.GEO.'+event_name), "TEST")
                ChangePrivileges_management((pub_database_path+r'/KHUBPub.GEO.'+event_name), "readonly", View="GRANT", Edit="")
                AddMessage('{0} {1}: {2} {3} {4}'.format(event_name, "copied over publication database", i, "of", len(EventList)))
                update_status_table(status_table, event_name, status_fields, "Overwrite in Publication Database", None)
                
            i += 1    
        except ExecuteError:
            AddWarning('{0} {1}: {2} {3} {4}'.format(event_name, "produced an error", i, "of", len(EventList)))
            message = GetMessages(2)
            update_status_table(status_table, event_name, status_fields, "Error Occurred", message)
            i += 1
            del event
            continue
    
    for network in NetworksList:
        try:
            network_name = network.split(".")[-1]
            if network_name not in pub_network_list:
                MakeFeatureLayer_management(RH_Database+r'/KHUB.RH.'+ network, network, where_clause="""(LRSFromDate is null or LRSFromDate<=CURRENT_TIMESTAMP) and (LRSToDate is null or LRSToDate>CURRENT_TIMESTAMP)""")
                Project_management((network), (pub_database_path+r'/KHUBPub.GEO.'+network_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
                #CopyFeatures_management((RH_Database+r'/KHUB.RH.'+network), (pub_database_path+r'/KHUBPub.GEO.'+network_name))
                ChangePrivileges_management((pub_database_path+r'/KHUBPub.GEO.'+network_name), "readonly", View="GRANT", Edit="")
                AddMessage('{0} {1}'.format(network_name, "copied to publication database"))
                update_status_table(status_table, network_name, status_fields, "Copied to Publication Database", None)
            else:
                MakeFeatureLayer_management(RH_Database+r'/KHUB.RH.'+ network, network, where_clause="""(LRSFromDate is null or LRSFromDate<=CURRENT_TIMESTAMP) and (LRSToDate is null or LRSToDate>CURRENT_TIMESTAMP)""")
                Project_management((network), (pub_database_path+r'/KHUBPub.GEO.'+network_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
                #TruncateTable_management((pub_database_path+r'/KHUBPub.GEO.'+network_name))
                #Append_management((RH_Database+r'/KHUB.RH.'+network), (pub_database_path+r'/KHUBPub.GEO.'+network_name), "TEST")
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
            if intersec_name not in pub_network_list:
                Project_management(RH_Database+r'/KHUB.RH.'+ intersec, (pub_database_path+r'/KHUBPub.GEO.'+intersec_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
                AddMessage('{0} {1}'.format(intersec_name, "copied to publication database"))
                update_status_table(status_table, intersec_name, status_fields, "Copied to Publication Database", None)
            else:
                Project_management(RH_Database+r'/KHUB.RH.'+ intersec, (pub_database_path+r'/KHUBPub.GEO.'+intersec_name), webmerc, transform_method, in_coor_system, "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
                AddMessage('{0} {1}'.format(intersec_name, "overwrote in publication database"))
                update_status_table(status_table, intersec_name, status_fields, "Overwrite in Publication Database", None)
                
        except ExecuteError:
            AddWarning('{0} {1}'.format(intersec_name, "produced an error"))
            message = GetMessages(2)
            update_status_table(status_table, intersec_name, status_fields, "Error Occurred", message)
            del network
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

    # utilizes workspace C:\\\\temp\\CONCURRENT.gdb
    # ---------------------------------------------------------------------------
    from datetime import datetime

    if target == 'Prod':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\Geo@KHPub.sde'
        pubinstance = r"khdbpubprod\khubpub_prod"
        RH_Database = r'C:\Users\planadm\GISDATA\DbConnections\Prod\RH@KHTransKhub.sde'
    elif target == 'Test':
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\Geo@KHPubTest.sde'
        pubinstance = r"khdbpubtest\khubpub_test"
        RH_Database = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\rh@KHTestKHUB.sde'
    else:
        pub_database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\Geo@KHPubDev.sde'   
        pubinstance = r"khdbpubdev\khubpub_dev"
        RH_Database = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\rh@KHDevKHUB.sde'
    
    from arcpy import env, da, AddMessage, AddWarning, Exists, MakeRouteEventLayer_lr, CheckExtension, CheckOutExtension, CreateRoutes_lr, ChangePrivileges_management, CopyFeatures_management, Delete_management, MultipartToSinglepart_management, Copy_management, Merge_management, MakeTableView_management, Erase_analysis, ExecuteError, GetMessages, LocateFeaturesAlongRoutes_lr, CheckInExtension, MakeFeatureLayer_management, FeatureClassToFeatureClass_conversion, CreateTable_management, Append_management, AddField_management, CalculateField_management
    from locref import CalculateRouteConcurrencies
    ws= env.workspace=r"C:\\temp\\CONCURRENT.gdb"
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


    whereClauseAll= "Prefix IN ('1','2','3','4','5')"
    MakeFeatureLayer_management (LRSCounty,KHUBRoutesLyr,whereClauseAll)
    CalculateRouteConcurrencies(KHUBRoutesLyr, "temp_table", "", "FIND_DOMINANCE")
    if Exists(ws + "\\concurr_tbl_all"):
        # Delete it if it does exist
        Delete_management(ws + "\\concurr_tbl_all")
    CreateTable_management(ws, "concurr_tbl_all", "temp_table")
    Append_management("temp_table","concurr_tbl_all")
    AddField_management("concurr_tbl_all", "Prefix", "TEXT", "", "", "1", "", "NULLABLE", "NON_REQUIRED", "")

    CalculateField_management("concurr_tbl_all", "Prefix", "Mid( [RouteId],4,1 )", "VB", "")
    print ("concurrent table created")

    FeatureClassToFeatureClass_conversion(KHUBRoutesLyr, ws, KHUBRoutes, "LRSToDate IS NULL AND Prefix IN ( '1', '2', '3','4','5') ")

    CheckInExtension("Highways")
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
    TargetRoutes_Erase_LocateFea_Events = "TargetRoutes_Erase_LocateFea Events"
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
    LocateFeaturesAlongRoutes_lr(TargetRoutes_Erase, TargetRoutesPrefix1235, "RouteId", "0.01 Feet", TargetRoutes_Erase_LocateFea, Output_Event_Table_Properties, "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
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


    # Create singlepart features
    MultipartToSinglepart_management(DominantRoutesAll,DominantRtesSinglePart)
    AddField_management(DominantRtesSinglePart, "MinMeas", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management(DominantRtesSinglePart, "MaxMeas", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management(DominantRtesSinglePart, "MaxMeas", "round(!Shape.extent.MMax!,7)  ", "PYTHON_9.3", "")
    CalculateField_management(DominantRtesSinglePart, "MinMeas", "round(!Shape.extent.MMin!,7)  ", "PYTHON_9.3", "")

    print ("single parts fc with measures created ")
    #output these results to the publication database
    FeatureClassToFeatureClass_conversion(DominantRoutesAll, pub_database, "LRS_County_Primary", "")
    FeatureClassToFeatureClass_conversion(DominantRtesSinglePart, pub_database, "LRS_County_PrimarySP", "")
    ChangePrivileges_management((pub_database+r'/KHUBPub.GEO.LRS_County_Primary'), "readonly", View="GRANT", Edit="")
    ChangePrivileges_management((pub_database+r'/KHUBPub.GEO.LRS_County_PrimarySP'), "readonly", View="GRANT", Edit="")
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

    
    
    
    

def main():
    Analyze()
    PostAndReconcile()  ##enable for nightly run
    Compress()          ##enable for nightly run
    Analyze()
    #RebuildIndexes() #in testing
    #RecreatePubGDB('Dev')
    #RecreatePubGDB('Prod')
    PublicateNetworkProd2Target('Prod') ## update prod transactional data to publication in 'dev', 'test', or 'prod'
    #PublicateNetworkProd2Target('Test')  #In testing
    #PublicateNetworkProd2Target('Dev') 
    CreatePrimaryNetwork('Test')
    print("run completed" )
    
    
main()

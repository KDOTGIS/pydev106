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
from prod_config import sde, rh
from arcpy import DisconnectUser, DeleteVersion_management, AcceptConnections, RebuildIndexes_management

def Analyze():
    from arcpy import AnalyzeDatasets_management
    print("this function analyzes datasets for "+rh + " and " + sde)
    print("analyzing RH and SDE in source")
    AnalyzeDatasets_management(rh, "NO_SYSTEM", "KHUB.RH.Calibration_Point;KHUB.RH.Centerline;KHUB.RH.Centerline_Sequence;KHUB.RH.Lrs_Edit_Log;KHUB.RH.Lrs_Event_Behavior;KHUB.RH.Lrs_Locks;KHUB.RH.Lrs_Metadata;KHUB.RH.Redline;KHUB.RH.LRS_County", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
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
    
    #Transactional Database connection to default to copy to publication
    RH_Database = r'C:\Users\kyleg\gisdata\DbConnections\Prod\ad@KHProd.sde'
    
    if target == 'Prod':
        pub_database = r'C:\Users\kyleg\gisdata\DbConnections\Prod\geo@KHPub.sde'
    elif target == 'Test':
        pub_database = r'C:\Users\kyleg\gisdata\DbConnections\KHTest\geo@KHPubTest.sde'
    else:
        pub_database = r'C:\Users\kyleg\gisdata\DbConnections\KHDev\geo@KHPubDev.sde'    
    print (pub_database)
    pub_database_path = pub_database
    env.workspace = pub_database
    from KhubFCList import NetworksList, EventList
    from arcpy import da, CopyFeatures_management, AddMessage, AddWarning, TruncateTable_management, Append_management, ExecuteError, CreateTable_management, AddField_management, Exists, GetMessages
    pub_event_list = EventList
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
            print(event +" " +event_name)
            if event_name not in pub_event_list:
                CopyFeatures_management((RH_Database+r'/KHUB.RH.'+ event), (pub_database_path+r'/KHUBPub.GEO.'+event_name))  # Modified to test Copy Features instead of Fc to Fc conversion
                AddMessage('{0} {1}: {2} {3} {4}'.format(event_name, "copied to publication database", i, "of", len(EventList)))
                update_status_table(status_table, event_name, status_fields, "Copied to Publication Database", None)
            else:
                TruncateTable_management((pub_database_path+r'/KHUBPub.GEO.'+event_name))
                Append_management((RH_Database+r'/KHUB.RH.'+ event), (pub_database_path+r'/KHUBPub.GEO.'+event_name), "TEST")
                AddMessage('{0} {1}: {2} {3} {4}'.format(event_name, "updated in publication database", i, "of", len(EventList)))
                update_status_table(status_table, event_name, status_fields, "Updated in Publication Database", None)
            i += 1    
        except ExecuteError:
            AddWarning('{0} {1}: {2} {3} {4}'.format(event_name, "produced an error", i, "of", len(EventList)))
            message = GetMessages(2)
            update_status_table(status_table, event_name, status_fields, "Error Occurred", message)
            i += 1
            continue
    
    for network in NetworksList:
        try:
            network_name = network.split(".")[-1]
            if network_name not in pub_network_list:
                CopyFeatures_management((RH_Database+r'/KHUB.RH.'+network), (pub_database_path+r'/KHUBPub.GEO.'+network_name))
                AddMessage('{0} {1}'.format(network_name, "copied to publication database"))
                update_status_table(status_table, network_name, status_fields, "Copied to Publication Database", None)
            else:
                TruncateTable_management((pub_database_path+r'/KHUBPub.GEO.'+network_name))
                Append_management((RH_Database+r'/KHUB.RH.'+network), (pub_database_path+r'/KHUBPub.GEO.'+network_name), "TEST")
                AddMessage('{0} {1}'.format(network_name, "updated in publication database"))
                update_status_table(status_table, network_name, status_fields, "Updated in Publication Database", None)
        except ExecuteError:
            AddWarning('{0} {1}'.format(network_name, "produced an error"))
            message = GetMessages(2)
            update_status_table(status_table, network_name, status_fields, "Error Occurred", message)
            continue

def PublicateNetworkProd2Prod():
    from arcpy import env
    from datetime import datetime
    env.overwriteOutput = True
    
    #Transactional Database connection to default to copy to publication
    RH_Database = r'C:\Users\kyleg\gisdata\DbConnections\Prod\ad@KHProd.sde'
    
    pub_database = r'C:\Users\kyleg\gisdata\DbConnections\Prod\geo@KHPub.sde'
    
    pub_database_path = pub_database
    env.workspace = pub_database
    from KhubFCList import NetworksList, EventList
    from arcpy import da, CopyFeatures_management, AddMessage, AddWarning, TruncateTable_management, Append_management, ExecuteError, CreateTable_management, AddField_management, Exists, GetMessages
    pub_event_list = EventList
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
            print(event +" " +event_name)
            if event_name not in pub_event_list:
                CopyFeatures_management((RH_Database+r'/KHUB.RH.'+ event), (pub_database_path+r'/KHUBPub.GEO.'+event_name))  # Modified to test Copy Features instead of Fc to Fc conversion
                AddMessage('{0} {1}: {2} {3} {4}'.format(event_name, "copied to publication database", i, "of", len(EventList)))
                update_status_table(status_table, event_name, status_fields, "Copied to Publication Database", None)
            else:
                TruncateTable_management((pub_database_path+r'/KHUBPub.GEO.'+event_name))
                Append_management((RH_Database+r'/KHUB.RH.'+ event), (pub_database_path+r'/KHUBPub.GEO.'+event_name), "TEST")
                AddMessage('{0} {1}: {2} {3} {4}'.format(event_name, "updated in publication database", i, "of", len(EventList)))
                update_status_table(status_table, event_name, status_fields, "Updated in Publication Database", None)
            i += 1    
        except ExecuteError:
            AddWarning('{0} {1}: {2} {3} {4}'.format(event_name, "produced an error", i, "of", len(EventList)))
            message = GetMessages(2)
            update_status_table(status_table, event_name, status_fields, "Error Occurred", message)
            i += 1
            continue
    
    for network in NetworksList:
        try:
            network_name = network.split(".")[-1]
            if network_name not in pub_network_list:
                CopyFeatures_management((RH_Database+r'/KHUB.RH.'+network), (pub_database_path+r'/KHUBPub.GEO.'+network_name))
                AddMessage('{0} {1}'.format(network_name, "copied to publication database"))
                update_status_table(status_table, network_name, status_fields, "Copied to Publication Database", None)
            else:
                TruncateTable_management((pub_database_path+r'/KHUBPub.GEO.'+network_name))
                Append_management((RH_Database+r'/KHUB.RH.'+network), (pub_database_path+r'/KHUBPub.GEO.'+network_name), "TEST")
                AddMessage('{0} {1}'.format(network_name, "updated in publication database"))
                update_status_table(status_table, network_name, status_fields, "Updated in Publication Database", None)
        except ExecuteError:
            AddWarning('{0} {1}'.format(network_name, "produced an error"))
            message = GetMessages(2)
            update_status_table(status_table, network_name, status_fields, "Error Occurred", message)
            continue


def main():
    Analyze()
    PostAndReconcile()  ##enable for nightly run
    Compress()          ##enable for nightly run
    Analyze()
    #RebuildIndexes() #in testing
    PublicateNetworkProd2Target('Dev') ## update prod transactional data to publication in 'dev', 'test', or 'prod'
    PublicateNetworkProd2Target('Test')  #In testing
    PublicateNetworkProd2Target('Prod') 
    #PublicateNetworkProd2Prod()  #tested once
    print("run completed" )
    
    
main()


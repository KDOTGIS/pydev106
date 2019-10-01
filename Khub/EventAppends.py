'''
Created on Jun 18, 2019

Discussion with Andrea and Logan 8/1/2019






@author: kyleg
'''



if __name__ == '__main__':
    pass

def FieldMappingTest():
    print ('Field Mapping Test running')
    from arcpy import CheckOutExtension, CheckInExtension, FieldMappings, ListFeatureClasses, ValueTable, env
    from locref import AppendEvents
    from config_dev import stagefile, ad
    print ('function and config imports completed')
    
    CheckOutExtension("Highways")
    print ('Extension checked out')
    env.workspace = ad
    in_dataset = stagefile+r'\trans_ev_TravelWayOp_final'
    in_target_event = ad+r'\KHUB.RH.ev_TravelWayOperation'
    print (in_dataset)
    print (in_target_event)
    field_mapping = FieldMappings()
    field_mapping.addTable(in_dataset)
    field_mapping.addTable(in_target_event)
    fcs = ListFeatureClasses("*ev_Travel*", "Polyline")
    vTab = ValueTable()
    for fc in fcs:
        print (fc)
        fieldmappings = FieldMappings()
        # Adding a table is the fast way to load all the fields from the
        #   input into fieldmaps held by the fieldmappings object.
        #
        fieldmappings.addTable(fc)
    
        # In this example also create two fieldmaps by 'chopping up'
        #   an input field. Feed the chopped field into the new fieldmaps.
        #
        #fldmap_TRACTID.addInputField(fc, "STFID")
        #fldmap_BLOCKID.addInputField(fc, "STFID")
            
        # Populate the input value table with feature classes
        #
        vTab.addRow(fc)
    #Manually Cross reference different named fields
    

    load_type = 'RETIRE_OVERLAPS'  #ADD RETIRE_OVERLAPS  RETIRE_BY_EVENT_ID, REPLACE_BY_EVENT_ID 
    generate_event_ids = 'NO_GENERATE_EVENT_IDS'
    generate_shapes = 'GENERATE_SHAPES'
    print('appending events to admo from staging')
    #AppendEvents(in_dataset, in_target_event, field_mapping, load_type, generate_event_ids, generate_shapes)
    print('appended events to admo from staging')
    
    CheckInExtension("Highways")
 
    print ('Extension checked in')

def AppendAdmo():
    print ('Appennd Admo running')
    from arcpy import CheckOutExtension, CheckInExtension
    from locref import AppendEvents
    from config_dev import stage, ad
    print ('function and config imports completed')
    
    CheckOutExtension("Highways")
    print ('Extension checked out')
    
    in_dataset = stage+r'\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL'
    in_target_event = ad+r'\KHUB.RH.ev_AdministrativeOwner'
    print (in_dataset)
    print (in_target_event)
    field_mapping = """'EventID "EventID" true false false 38 Text 0 0 ,First,#,C:\gisdata\DBConnections\Khub\KHDev\ad@KHubdevKHUBStage.sde\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL,EventID,-1,-1;
    RouteID "RouteID" true false false 38 Text 0 0 ,First,#,C:\gisdata\DBConnections\Khub\KHDev\ad@KHubdevKHUBStage.sde\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL,RouteID,-1,-1;
    FromMeasure "FromMeasure" true true false 8 Double 7 38 ,First,#,C:\gisdata\DBConnections\Khub\KHDev\ad@KHubdevKHUBStage.sde\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL,FromMeasure,-1,-1;
    ToMeasure "ToMeasure" true true false 8 Double 7 38 ,First,#,C:\gisdata\DBConnections\Khub\KHDev\ad@KHubdevKHUBStage.sde\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL,ToMeasure,-1,-1;
    AdministrativeOwner "AdministrativeOwner" true false false 3 Text 0 0 ,First,#,C:\gisdata\DBConnections\Khub\KHDev\ad@KHubdevKHUBStage.sde\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL,AdministrativeOwner,-1,-1;
    InventoryStartDate "InventoryStartDate" true true false 8 Date 0 0 ,First,#,C:\gisdata\DBConnections\Khub\KHDev\ad@KHubdevKHUBStage.sde\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL,InventoryStartDate,-1,-1;
    LRSFromDate "LRSFromDate" true false false 8 Date 0 0 ,First,#,C:\gisdata\DBConnections\Khub\KHDev\ad@KHubdevKHUBStage.sde\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL,LRSFromDate,-1,-1;
    LRSToDate "LRSToDate" true true false 8 Date 0 0 ,First,#,C:\gisdata\DBConnections\Khub\KHDev\ad@KHubdevKHUBStage.sde\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL,LRSToDate,-1,-1;
    SourceCIT "SourceCIT" true true false 20 Text 0 0 ,First,#,C:\gisdata\DBConnections\Khub\KHDev\ad@KHubdevKHUBStage.sde\KHUB_STG.RH.TRANS_EV_ADMINISTRATIVEOWNER_ALL,SourceCIT,-1,-1'"""
    load_type = 'ADD'
    generate_event_ids = 'NO_GENERATE_EVENT_IDS'
    generate_shapes = 'GENERATE_SHAPES'
    print('appending events to admo from staging')
    AppendEvents(in_dataset, in_target_event, field_mapping, load_type, generate_event_ids, generate_shapes)
    print('appended events to admo from staging')
    
    CheckInExtension("Highways")
    
    print ('Extension checked in')
    
def VersionToLockroot():
    from arcpy import ReconcileVersions_management
    from config_dev import sde
    out_log = r"//gisdata/KHUB/documentation/reconcile_versions_log/lockroot_to_default/log2019061802.txt"
    ReconcileVersions_management(sde, "ALL_VERSIONS", "QCADMIN.QC_Lockroot", '"DTNT\KYLEG".KyleAppendEvents', "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", out_log)
  
    
def LockrootToDefault():
    from arcpy import ReconcileVersions_management, Compress_management
    from config_dev import sde, rh
    print ('posting lockroot to default')
    out_log = r"//gisdata/KHUB/documentation/reconcile_versions_log/lockroot_to_default/log2019061803.txt"
    ReconcileVersions_management(sde, "ALL_VERSIONS", "sde.DEFAULT", "QCADMIN.QC_Lockroot", "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", out_log)
    Compress_management(rh)
    
    
    
    
def main():
    #AppendAdmo()
    
    #LockrootToDefault()
    FieldMappingTest()
    
main()
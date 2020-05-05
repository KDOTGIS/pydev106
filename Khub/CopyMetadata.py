'''
Created on Aug 13, 2019
Metadata Export from Dev and import to TEST, check. then then run on Prod
takes about 20 minutes to run on all listed feature classes in dev test and prod

@author: kyleg
'''

if __name__ == '__main__':
    pass

print ("started")
from arcpy import  ListFeatureClasses, env, ListTables, MetadataImporter_conversion, ExportMetadata_conversion, XSLTransform_conversion, ClearWorkspaceCache_management
from KhubFCList import EventList, TestEvents
print ("arcpy tools imported")
MetaDataSorceDB = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\rh@KHDevKHUB.sde'

DevPub = r'C:\Users\planadm\GISDATA\DbConnections\KHDev\Geo@KHPubDev.sde'
ProdPub =r'C:\Users\planadm\GISDATA\DbConnections\Prod\Geo@KHPub.sde'
TestPub = r'C:\Users\planadm\GISDATA\DbConnections\KHTest\Geo@KHPubTest.sde'
TransTest = r"C:\Users\planadm\GISDATA\DbConnections\KHTest\rh@KHTestKHUB.sde"
TransProd = r"C:\Users\planadm\GISDATA\DbConnections\Prod\rh@KHTransKHUB.sde"
TransDBDO = 'KHUB.RH.'
PubDBNO = 'KHUBPub.Geo.'
Translator = r"D:/Program Files (x86)/ArcGIS/Desktop10.6/Metadata/Translator/ARCGIS2ISO19139.xml"
env.overwriteOutput = 1

def exportFromTransDev():
    #Transactional DEV is where we are maintaining our comprehensive metadata process, where Chris is actively editing
    env.workspace = MetaDataSorceDB
    print env.workspace
    print("workspace set")
    #just listing these feature classes and tables takes a pretty long time, like about 20 minutes.
    #features exported for 22 min, then tables took another hour plus
    #FCList = ListFeatureClasses("*KHUB.RH.ev_*")
    for FC in EventList:
        FCPath = TransDBDO + FC
        print(FCPath)
        ExportMetadata_conversion(FCPath, Translator, r"C:\temp\Khub_Metadata\\"+FC+".xml")
        MetadataImporter_conversion(FCPath, r"C:\temp\Khub_Metadata\\"+FC+".xml")
                
def MetadataScrubber():
    print ("Scrubbing Metadata GP history for:")
    remove_gp_history_xslt = r"D:\Program Files (x86)\ArcGIS\Desktop10.6\Metadata\Stylesheets\gpTools\remove geoprocessing history.xslt"
    #merge_Description2Fields = r"D:/Program Files (x86)/ArcGIS/Desktop10.6/Metadata/Stylesheets/gpTools/merge imported metadata with existing.xslt"
    for FC in EventList:
        print(FC)
        XSLTransform_conversion(r"C:/temp/Khub_Metadata/"+FC+".xml", remove_gp_history_xslt, r"C:/temp/Khub_Metadata/"+FC+"Clean.xml", "")
        #XSLTransform_conversion(r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+"Clean.xml", merge_Description2Fields, r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+"Valid.xml", r"C:\temp\Khub_Metadata\styletemplate\KhubTemplate.xml")
        #XSLTransform_conversion(r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+".xml", merge_Description2Fields, r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+"ValidHistory.xml", r"C:\temp\Khub_Metadata\styletemplate\KhubTemplate.xml")

def importTarget(target):
    env.workspace = target
    print env.workspace
    print("importing metadata")
    for FC in EventList:
        print(FC)
        MetadataImporter_conversion(r"C:/temp/Khub_Metadata/"+FC+"Clean.xml", FC)
    ClearWorkspaceCache_management()
    
def main():
    exportFromTransDev()  #do this on a routine, deployed with publication upddates
    MetadataScrubber()  # and do this
    #importTarget(DevPub)
    importTarget(TestPub)
    importTarget(ProdPub)
    importTarget(TransTest)
    importTarget(TransProd)
    ClearWorkspaceCache_management()
    
main()
    

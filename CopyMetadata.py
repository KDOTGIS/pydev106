'''
Created on Aug 13, 2019
Metadata Export from Dev and import to TEST, check. then then run on Prod
takes about two hours to run on all feature classes, tables, and views

@author: kyleg
'''

if __name__ == '__main__':
    pass

print ("started")
from arcpy import  ListFeatureClasses, env, ListTables, MetadataImporter_conversion, ExportMetadata_conversion, XSLTransform_conversion, ClearWorkspaceCache_management
from KhubFCList import EventList, TestEvents
print ("arcpy tools imported")
DEV = r'C:\gisdata\DBConnections\Khub\KHDev\rh@KHubdevKHUB.sde'
DEVNO = 'KHUB.RH.'
#TARGET = r"C:\gisdata\DBConnections\Khub\KHTest\rh@KHTestKHUB.sde"
#TARGET = r"C:\gisdata\DBConnections\Khub\Khub\rh@KHTransKHUB.sde"
TARGET = DEV
TargetDBNO = 'KHUB.RH.'
Translator = r"C:/Program Files (x86)/ArcGIS/Desktop10.6/Metadata/Translator/ARCGIS2ISO19139.xml"
env.overwriteOutput = 1

def exportFromDev():
    env.workspace = DEV
    print env.workspace
    print("workspace set")
    #just listing these feature classes and tables takes a pretty long time, like about 20 minutes.
    #features exported for 22 min, then tables took another hour plus
    #FCList = ListFeatureClasses("*KHUB.RH.ev_*")
    for FC in EventList:
        FCPath = DEVNO + FC
        print(FC)
        ExportMetadata_conversion(FC, Translator, r"C:\temp\Khub_Metadata\\"+FC+".xml")
        MetadataImporter_conversion(FC, r"C:\temp\Khub_Metadata\\"+FC+".xml")
    
    #Tables = ListTables()
    #for table in Tables:
    #    print(table)
    #    MetadataImporter_conversion(FC, translator, "C:/temp/Khub_Metadata/"+table+".XML")
        
def MetadataScrubber():
    print ("Scrubbing Metadata GP history for:")
    remove_gp_history_xslt = r"C:\Program Files (x86)\ArcGIS\Desktop10.6\Metadata\Stylesheets\gpTools\remove geoprocessing history.xslt"
    merge_Description2Fields = r"C:/Program Files (x86)/ArcGIS/Desktop10.6/Metadata/Stylesheets/gpTools/merge imported metadata with existing.xslt"
    for FC in EventList:
        print(FC)
        XSLTransform_conversion(r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+".xml", remove_gp_history_xslt, r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+"Clean.xml", "")
        #XSLTransform_conversion(r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+"Clean.xml", merge_Description2Fields, r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+"Valid.xml", r"C:\temp\Khub_Metadata\styletemplate\KhubTemplate.xml")
        #XSLTransform_conversion(r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+".xml", merge_Description2Fields, r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+"ValidHistory.xml", r"C:\temp\Khub_Metadata\styletemplate\KhubTemplate.xml")

def importTarget():
    env.workspace = TARGET
    print env.workspace
    print("importing metadata")
    for FC in EventList:
        print(FC)
        MetadataImporter_conversion(r"C:/temp/Khub_Metadata/"+TargetDBNO+FC+"ValidHistory.xml", FC)
    
def main():
    #exportFromDev()
    MetadataScrubber()
    importTarget()
    ClearWorkspaceCache_management()
    
main()
    
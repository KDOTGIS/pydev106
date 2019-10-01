'''
Created on Aug 8, 2019

@author: kyleg
'''

var = 'Khub_20190805.RH.KHUB_RH_KhubDD'
print(var)
var1 = var[25:]
print(var1)

import arcpy
import os, string

''' Update the following five variables before running the script.'''
version = "10.5"
myWorkspace = r"C:\XML_out\dbinstance_testgdb.sde"
gp_history_xslt = r"C:\Program Files (x86)\ArcGIS\Desktop{}\Metadata\Stylesheets\gpTools\remove geoprocessing history.xslt".format(version)
output_dir = r"C:\XML_out"
db_type = "SQL" #Set this to either "SQL" or "Oracle" if your db has spatial views. If not you may set it to "".

def RemoveHistory(myWorkspace, gp_history_xslt, output_dir):
##Removes GP History for feature dataset stored feature classes, and feature classes in the File Geodatabase.

    arcpy.env.workspace = myWorkspace
    for fds in arcpy.ListDatasets('','feature') + ['']:
        for fc in arcpy.ListFeatureClasses('','',fds):
            data_path = os.path.join(myWorkspace, fds, fc)
            if isNotSpatialView(myWorkspace, fc):
                removeAll(data_path, fc, gp_history_xslt, output_dir)


def isNotSpatialView(myWorkspace, fc):
##Determines if the item is a spatial view and if so returns True to listFcsInGDB()    
    if db_type <> "":
        desc = arcpy.Describe(fc)
        fcName = desc.name
        #Connect to the GDB
        egdb_conn = arcpy.ArcSDESQLExecute(myWorkspace)
        #Execute SQL against the view table for the specified RDBMS
        if db_type == "SQL":
            db, schema, tableName = fcName.split(".")
            sql = r"IF EXISTS(select * FROM sys.views where name = '{0}') SELECT 1 ELSE SELECT 0".format(tableName)
        elif db_type == "Oracle":
            schema, tableName = fcName.split(".")
            sql = r"SELECT count(*) from dual where exists (select * from user_views where view_name = '{0}')".format(tableName)
            egdb_return = egdb_conn.execute(sql)
            if egdb_return == 0:
                return True
            else:
                return False
        else: return True
    else: return True

def removeAll(data_path, feature, gp_history_xslt, output_dir):
##Remove all GP History metadata from a feature class.

    arcpy.ClearWorkspaceCache_management()
    name_xml = os.path.join(output_dir, str(feature)) + ".xml"

    arcpy.XSLTransform_conversion(data_path, gp_history_xslt, name_xml)
    print "Completed xml coversion on {0}".format(feature)

    arcpy.MetadataImporter_conversion(name_xml, data_path)
    print "Imported XML on {0}".format(feature)

def makeDirectory(output_dir):
##Creates directory to store the xml tables of converted metadata. If the
##directory already exists, the files will be created there.

    if not arcpy.Exists(output_dir):
        os.mkdir(output_dir)

if __name__ == "__main__":
    makeDirectory(output_dir)
    RemoveHistory(myWorkspace, gp_history_xslt, output_dir)
print "Done Done"

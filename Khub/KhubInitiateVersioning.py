'''
Created on Jun 18, 2019

@author: kyleg
'''

if __name__ == '__main__':
    pass

print ('script initiated')

def CreateLockroot():
    from config_test import QC
    from arcpy import CreateVersion_management
    CreateVersion_management(QC, "sde.DEFAULT", "QC_Lockroot", "PUBLIC")

def ProtectDefault():
    from config_test import sde
    from arcpy import AlterVersion_management
    AlterVersion_management(sde, "sde.DEFAULT", "#", '#', "PROTECTED")
    
def CreateTDSUserVersions():
    from config_prod import tds
    from arcpy import CreateVersion_management
    CreateVersion_management(tds, "QCADMIN.QC_Lockroot", "PavementSandwich", "PUBLIC")
    CreateVersion_management(tds, "QCADMIN.QC_Lockroot", "PavementSandwich_Ed2", "PUBLIC")
    CreateVersion_management(tds, "QCADMIN.QC_Lockroot", "PavementSandwich_Ed3", "PUBLIC")
    CreateVersion_management(tds, "QCADMIN.QC_Lockroot", "PavementSandwich_Ed4", "PUBLIC")
    CreateVersion_management(tds, "QCADMIN.QC_Lockroot", "PavementSandwich_Ed5", "PUBLIC")

def main():
    print ('running main')
    #CreateLockroot()
    #ProtectDefault()
    CreateTDSUserVersions()
    print ('completed')
    
main()
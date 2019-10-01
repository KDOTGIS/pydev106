'''
Created on May 28, 2019

@author: kyleg
'''

if __name__ == '__main__':
    pass

ServiceDirectoryFolder = r'\\gisdata\KHUB\services\MXD\Khubi3_1061'

RootPLV_service = r'TDSUser@KHUB_KHDBTRANSDEV_v_pavementsandwich.sde'
RootBaseVersion = r'TDSUSER.PavementSandwich'

from arcpy import ChangeVersion_management, CreateVersion_management, mapping

mapping.MXD = r'\\gisdata\KHUB\services\MXD\Khubi3_1061\PLV_EditsKMG.mxd'

def CreatePLV_MXD():
    

def main():
'''
Created on Aug 14, 2019

@author: kyleg
'''
TestEvents = ['ev_AccessControl', 'ev_WorkZone']

NetworksList = ['LRS_County', 'LRS_State', 'Centerline', 'Calibration_Point', 'Redline', 'IM_INTERSECTION_POINT', 'IM_ROADWAY_SEGMENT', 'INTERCHANGE_INDEX']

ALRS_Tables = ['Centerline_Sequence', 'Lrs_Edit_Log', 'LRS_EVENT_BEHAVIOR', 'Lrs_Locks', 'LRS_METADATA']

EventList = [
            'ev_AADT',
            'ev_AADT2012',
            'ev_AADT2013',
            'ev_AADT2014',
            'ev_AADT2015',
            'ev_AADT2016',
            'ev_AADTDirFactor',
            'ev_AADTExpansionFactor',
            'ev_AADTKFactor',
            'ev_AccessControl',
            'ev_AccessPermit',
            'ev_AccidentAnalysisDate',
            'ev_Accidents',
            'ev_AdministrativeOwner',
            'ev_AdvisorySpeed',
            'ev_AuxiliaryLane',
            'ev_CapacityHCM',
            'ev_CityJurisdiction',
            'ev_CollectorSection',
            'ev_CongressionalDistrict',
            'ev_County',
            'ev_CountyOnState',
            'ev_CrestVertSightDistNP',
            'ev_CrestVertSightDistP',
            'ev_Culverts',
            'ev_CurbType',
            'ev_DesignAccessControl',
            'ev_DesignStandShoulderWt',
            'ev_EPFS',
            'ev_EPFS2012',
            'ev_EPFS2013',
            'ev_EPFS2014',
            'ev_EPFS2015',
            'ev_EPFS2016',
            'ev_FieldInventory',
            'ev_FreightNetwork',
            'ev_FunctionalClass',
            'ev_GradientPercent',
            'ev_HorizontalCurve',
            'ev_HorizontalCurveFT',
            'ev_HPMSPavementCondition',
            'ev_HPMSReporting',
            'ev_HPMSSample',
            'ev_IndianNation',
            'ev_KDOTMaintenance',
            'ev_KDOTProjects',
            'ev_KDOTRouteClass',
            'ev_MaintenanceResp',
            'ev_MajorGrading',
            'ev_ManagedLanes',
            'ev_Median',
            'ev_MedianBarrierType',
            'ev_MedianCrossoverType',
            'ev_MPOJurisdiction',
            'ev_MuniROW',
            'ev_NG911RouteStatus',
            'ev_NG911StreetName',
            'ev_NHSFederalAid',
            'ev_NonStateRouteStatus',
            'ev_NumberLanesAggregated',
            'ev_NumberThroughLanes',
            'ev_OnStreetParkingLeft',
            'ev_OnStreetParkingRight',
            'ev_OutdoorAdvertising',
            'ev_PassingLeft',
            'ev_PassingRight',
            'ev_PavementActivity',
            'ev_PavementConditionPSR',
            'ev_PavementCondSummary',
            'ev_PavementManagementSys',
            'ev_PriorityOptPvmtEquiv',
            'ev_ProjectTracking',
            'ev_RailroadCrossing',
            'ev_ReferencePost',
            'ev_RightOfWayLeft',
            'ev_RightOfWayMedian',
            'ev_RightOfWayRight',
            'ev_RockWedgeLeft',
            'ev_RockWedgeMedian',
            'ev_RockWedgeRight',
            'ev_RouteDesignation',
            'ev_RumbleStripCenterline',
            'ev_RumbleStripLeft',
            'ev_RumbleStripMedian',
            'ev_RumbleStripRight',
            'ev_SafetyAnalyst',
            'ev_ShoulderMaterialLeft',
            'ev_ShoulderMaterialMed',
            'ev_ShoulderMaterialRight',
            'ev_ShoulderWidthLeft',
            'ev_ShoulderWidthMedian',
            'ev_ShoulderWidthRight',
            'ev_SideSlopeLeft',
            'ev_SideSlopeMedian',
            'ev_SideSlopeRight',
            'ev_SNICE',
            'ev_SpeedLimit',
            'ev_STRAHNET',
            'ev_StripMapMajorGrading',
            'ev_Structure',
            'ev_StructureSegment',
            'ev_SupplementalGrading',
            'ev_SurfaceTypeNSRural',
            'ev_SurfaceWidthPaved',
            'ev_TerrainType',
            'ev_ThroughLaneWidth',
            'ev_TrafficSequence',
            'ev_TravelWayOperation',
            'ev_TruckRoute',
            'ev_TurnLeft',
            'ev_TurnRight',
            'ev_UrbanJurisdiction',
            'ev_WideningObstacle',
            'ev_WorkZone'
    ]


class KhubLinearEvents(object):
    '''
    ev_AADT
    ev_AADT2012
    ev_AADT2013
    ev_AADT2014
    ev_AADT2015
    ev_AADT2016
    ev_AADTDirFactor
    ev_AADTExpansionFactor
    ev_AADTKFactor
    ev_AccessControl
    ev_AccessPermit
    ev_AccidentAnalysisDate
    ev_Accidents
    ev_AdministrativeOwner
    ev_AdvisorySpeed
    ev_AuxiliaryLane
    ev_CapacityHCM
    ev_CityJurisdiction
    ev_CollectorSection
    ev_CongressionalDistrict
    ev_County
    ev_CountyOnState
    ev_CrestVertSightDistNP
    ev_CrestVertSightDistP
    ev_Culverts
    ev_CurbType
    ev_DesignAccessControl
    ev_DesignStandShoulderWt
    ev_EPFS
    ev_EPFS2012
    ev_EPFS2013
    ev_EPFS2014
    ev_EPFS2015
    ev_EPFS2016
    ev_FieldInventory
    ev_FreightNetwork
    ev_FunctionalClass
    ev_GradientPercent
    ev_HorizontalCurve
    ev_HorizontalCurveFT
    ev_HPMSPavementCondition
    ev_HPMSReporting
    ev_HPMSSample
    ev_IndianNation
    ev_KDOTMaintenance
    ev_KDOTProjects
    ev_KDOTRouteClass
    ev_MaintenanceResp
    ev_MajorGrading
    ev_ManagedLanes
    ev_Median
    ev_MedianBarrierType
    ev_MedianCrossoverType
    ev_MPOJurisdiction
    ev_MuniROW
    ev_NG911RouteStatus
    ev_NG911StreetName
    ev_NHSFederalAid
    ev_NonStateRouteStatus
    ev_NumberLanesAggregated
    ev_NumberThroughLanes
    ev_OnStreetParkingLeft
    ev_OnStreetParkingRight
    ev_OutdoorAdvertising
    ev_PassingLeft
    ev_PassingRight
    ev_PavementActivity
    ev_PavementConditionPSR
    ev_PavementCondSummary
    ev_PavementManagementSys
    ev_PriorityOptPvmtEquiv
    ev_ProjectTracking
    ev_RailroadCrossing
    ev_ReferencePost
    ev_RightOfWayLeft
    ev_RightOfWayMedian
    ev_RightOfWayRight
    ev_RockWedgeLeft
    ev_RockWedgeMedian
    ev_RockWedgeRight
    ev_RouteDesignation
    ev_RumbleStripCenterline
    ev_RumbleStripLeft
    ev_RumbleStripMedian
    ev_RumbleStripRight
    ev_SafetyAnalyst
    ev_ShoulderMaterialLeft
    ev_ShoulderMaterialMed
    ev_ShoulderMaterialRight
    ev_ShoulderWidthLeft
    ev_ShoulderWidthMedian
    ev_ShoulderWidthRight
    ev_SideSlopeLeft
    ev_SideSlopeMedian
    ev_SideSlopeRight
    ev_SNICE
    ev_SpeedLimit
    ev_STRAHNET
    ev_StripMapMajorGrading
    ev_Structure
    ev_StructureSegment
    ev_SupplementalGrading
    ev_SurfaceTypeNSRural
    ev_SurfaceWidthPaved
    ev_TerrainType
    ev_ThroughLaneWidth
    ev_TrafficSequence
    ev_TravelWayOperation
    ev_TruckRoute
    ev_TurnLeft
    ev_TurnRight
    ev_UrbanJurisdiction
    ev_WideningObstacle
    ev_WorkZone


    '''


    def __init__(self, u_EventID, u_RouteID, u_FromMeasure, u_ToMeasure,  u_LRSFromDate, u_LRSToDate, u_LocError, InventoryStartDate, SourceCIT):
        '''
        Constructor
        '''
        self.EventID = u_EventID
        self.RouteID=u_RouteID
        self.FromMeasure=u_FromMeasure
        self.ToMeasure=u_ToMeasure
        self.LRSFromDate=u_LRSFromDate
        self.LRSToDate=u_LRSToDate
        self.LocError=u_LocError
        self.InventoryStartDate=InventoryStartDate
        self.SourceCIT=SourceCIT
        
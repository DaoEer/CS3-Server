# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine

class BHZBPointData( object ):
	"""
	帮会争霸据点数据
	"""
	def __init__( self, index = 0, occupyPlayerDBID = 0,occupyPlayerName = "",occupyTongDBID = 0,occupyTongName = "",pointType = 0, declareWarState = 1,fightEndTime = "",restEndTime = "",readyEndTime="",joinAttackPlayerDBIDs = [],joinProtectPlayerDBIDs = [] ):
		self.index = index
		self.occupyPlayerDBID = occupyPlayerDBID
		self.occupyPlayerName = occupyPlayerName
		self.occupyTongDBID = occupyTongDBID
		self.occupyTongName = occupyTongName
		self.pointType = pointType
		self.declareWarState = declareWarState
		self.fightEndTime = fightEndTime
		self.restEndTime = restEndTime
		self.readyEndTime = readyEndTime
		self.joinAttackPlayerDBIDs = joinAttackPlayerDBIDs
		self.joinProtectPlayerDBIDs = joinProtectPlayerDBIDs
		self.declarePlayerDBID = 0
		self.declareTongDBID = 0
		self.declareTongName = ""
		self.declarePlayerName = ""
		self.declareWarTime = 0
		self.notifyID = 0
		self.isEnterDefense = False # 是否进入布防
		self.repeatAddIntegralID = 0 # 持续增加积分timerID
		self.joinProtectGroupTeamID = 0 # 参与防守的队伍编号
		self.attackGroupTeamID = 0	# 进攻队伍编号

	def initData( self, dict ):
		self.index = dict[ "index" ]
		self.occupyPlayerDBID = dict["occupyPlayerDBID"]
		self.occupyPlayerName = dict["occupyPlayerName"]
		self.occupyTongDBID = dict["occupyTongDBID"]
		self.occupyTongName = dict["occupyTongName"]
		self.pointType = dict["pointType"]
		self.declareWarState = dict["declareWarState"]
		self.fightEndTime = dict["fightEndTime"]
		self.restEndTime = dict["restEndTime"]
		self.readyEndTime = dict["readyEndTime"]
		self.joinAttackPlayerDBIDs = dict["joinAttackPlayerDBIDs"]
		self.joinProtectPlayerDBIDs = dict["joinProtectPlayerDBIDs"]
		self.joinProtectGroupTeamID = dict["joinProtectGroupTeamID"]
		self.attackGroupTeamID = dict["attackGroupTeamID"]
		self.declareTongDBID = dict["declareTongDBID"]

	def setPointDeclareData( self, declarePlayerDBID, declareTongDBID, declareTongName, declarePlayerName,declareWarTime,attackGroupTeamID):
		"""
		设置据点宣战数据
		"""
		self.declarePlayerDBID = declarePlayerDBID
		self.declareTongDBID = declareTongDBID
		self.declareTongName = declareTongName
		self.declarePlayerName = declarePlayerName
		self.declareWarTime = declareWarTime
		self.attackGroupTeamID = attackGroupTeamID

	def setPointOccupyData( self, occupyPlayerDBID, occupyPlayerName, occupyTongDBID, occupyTongName ):
		"""
		设置据点占领数据
		"""
		self.occupyPlayerDBID = occupyPlayerDBID
		self.occupyPlayerName = occupyPlayerName
		self.occupyTongDBID = occupyTongDBID
		self.occupyTongName = occupyTongName

	def setPointReadyEndTime( self, readyEndTime ):
		"""
		设置据点准备时间
		"""
		self.readyEndTime = readyEndTime

	def addPointJoinAttackMembers( self, playerDBID ):
		"""
		增加参与攻击据点的人员
		"""
		if playerDBID not in self.joinAttackPlayerDBIDs:
			self.joinAttackPlayerDBIDs.append( playerDBID )

	def addPointJoinProtectMembers( self, playerDBID ):
		"""
		增加参与防守据点的人员
		"""
		if playerDBID not in self.joinProtectPlayerDBIDs:
			self.joinProtectPlayerDBIDs.append( playerDBID )

	def setPointRestEndTime( self, restEndTime ):
		"""
		设置据点重置时间
		""" 
		self.restEndTime = restEndTime

	def setIsEnterDefense( self, isEnterDefense ):
		"""
		设置是否进入布防
		"""
		self.isEnterDefense = isEnterDefense

	def setJoinProtectGroupTeam( self, groupID ):
		self.joinProtectGroupTeamID = groupID

	def getJoinProtectGroupTeam( self ):
		return self.joinProtectGroupTeamID

	def getAttackGroupTeamID( self ):
		return self.attackGroupTeamID

	def getIsEnterDefense( self ):
		return self.isEnterDefense

	def getPointRestEndTime( self ):
		return self.restEndTime

	def clearPointJoinAttackMembers( self ):
		self.joinAttackPlayerDBIDs.clear()

	def clearPointJoinProtectMembers( self ):
		self.joinProtectPlayerDBIDs.clear()

	def setPointState( self, declareWarState ):
		"""
		设置据点状态
		"""
		self.declareWarState = declareWarState

	def setNotifyID( self, notifyID ):
		self.notifyID = notifyID

	def getNotifyID( self ):
		return self.notifyID

	def getPointReadyEndTime( self ):
		"""
		"""
		return self.readyEndTime

	def getPointOccupyTongDBID( self ):
		"""
		"""
		return self.occupyTongDBID

	def setRepeatAddIntegralID( self, repeatAddIntegralID ):
		self.repeatAddIntegralID = repeatAddIntegralID

	def getRepeatAddIntegralID( self ):
		return self.repeatAddIntegralID

	def getPointOccupyPlayerDBID( self ):
		return self.occupyPlayerDBID

	def getPointOccupyTongName( self ):
		return self.occupyTongName

	def getPointDeclareTongDBID( self ):
		return self.declareTongDBID

	def getPointDeclareTongName( self ):
		return self.declareTongName

	def getPointDeclarePlayerDBID( self ):
		return self.declarePlayerDBID

	def getPointtDeclarePlayerName( self ):
		return self.declarePlayerName 

	def getPointJoinAttackMembers( self ):
		"""
		"""
		return self.joinAttackPlayerDBIDs

	def getPointJoinProtectMembers( self ):
		return self.joinProtectPlayerDBIDs

	def getPointType( self ):
		return self.pointType

	def getPointDeclareWarState( self ):
		return self.declareWarState

	def getPointIndex( self ):
		return self.index

	def getDictFromObj( self, obj ):
		dict = {
			"index"	: obj.index,
			"occupyPlayerDBID":obj.occupyPlayerDBID,
			"occupyPlayerName":obj.occupyPlayerName,
			"occupyTongDBID":obj.occupyTongDBID,
			"occupyTongName":obj.occupyTongName,
			"pointType":obj.pointType,
			"declareWarState":obj.declareWarState,
			"fightEndTime":obj.fightEndTime,
			"restEndTime":obj.restEndTime,
			"readyEndTime":obj.readyEndTime,
			"joinAttackPlayerDBIDs":obj.joinAttackPlayerDBIDs,
			"joinProtectPlayerDBIDs":obj.joinProtectPlayerDBIDs,
			"joinProtectGroupTeamID":obj.joinProtectGroupTeamID,
			"attackGroupTeamID":obj.attackGroupTeamID,
			"declareTongDBID":obj.declareTongDBID,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBPointData )

class BHZBPointDataMgr( dict ):
	"""
	帮会争霸据点数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[m.index] = m

	def addNPCPointData( self, index,occupyPlayerDBID,occupyPlayerName,occupyTongDBID,occupyTongName,pointType,declareWarState,fightEndTime = "",restEndTime = "",readyEndTime = "",joinPlayerDBIDs = [],joinProtectPlayerDBIDs = [] ):
		"""
		增加据点数据
		"""
		if index in self:
			del self[index]

		self[index] = BHZBPointData( index,occupyPlayerDBID,occupyPlayerName,occupyTongDBID,occupyTongName,pointType,declareWarState,fightEndTime,restEndTime,readyEndTime,[] ,[] )

	def updateOccupyPointData( self, index, pointType,occupyPlayerDBID, occupyPlayerName, occupyTongDBID, occupyTongName ):
		"""
		更新据点被占领数据
		"""
		if index in self:
			self[index].occupyPlayerDBID = occupyPlayerDBID
			self[index].occupyPlayerName = occupyPlayerName
			self[index].occupyTongDBID = occupyTongDBID
			self[index].occupyTongName = occupyTongName
		else:
			self.addNPCPointData( index, occupyPlayerDBID, occupyPlayerName, occupyTongDBID, occupyTongName,pointType )

	def updataNPCPointRestEndTime( self, pointIndex, restEndTime ):
		"""
		更新据点重置时间
		"""
		if pointIndex in self:
			self[pointIndex].restEndTime = restEndTime

	def updataNPCPointReadyEndTime( self, pointIndex, readyEndTime ):
		"""
		更新据点准备时间
		"""
		if pointIndex in self:
			self[pointIndex].readyEndTime = readyEndTime

	def updataNPCPointDeclareWarState( self, pointIndex, declareWarState ):
		"""
		更新据点状态
		"""
		if pointIndex in self:
			self[pointIndex].declareWarState = declareWarState

	def updateNPCPointAttackGroupTeamID( self, pointIndex, attackGroupTeamID, declareTongDBID ):
		"""
		更新据点进攻队伍数据
		"""
		if pointIndex in self:
			self[pointIndex].attackGroupTeamID = attackGroupTeamID
			self[pointIndex].declareTongDBID = declareTongDBID

	def updataBHZBPointJoinProtectTeamID( self, pointIndex, joinProtectTeamID ):
		"""
		更新参与防守的队伍编号
		"""
		if pointIndex in self:
			self[pointIndex].joinProtectGroupTeamID = joinProtectTeamID

	def getLastPointDeclareWarState( self, pointIndex ):
		"""
		获得上一次据点状态
		"""
		if pointIndex in self:
			return self[pointIndex].declareWarState
		return -1

	def updataNPCPointOccupyData( self, pointIndex,playerDBID,playerName,tongDBID,tongName ):
		"""
		更新据点占领帮会
		"""
		if pointIndex in self:
			self[pointIndex].occupyTongDBID = playerDBID
			self[pointIndex].occupyPlayerName = playerName
			self[pointIndex].occupyTongDBID = tongDBID
			self[pointIndex].occupyTongName = tongName

	def updataBHZBPointJoinAttackMembers( self, pointIndex, joinAttackMembers ):
		"""
		更新据点攻占成员
		"""
		if pointIndex in self:
			self[pointIndex].joinAttackPlayerDBIDs = joinAttackMembers

	def updataBHZBPointJoinProtectMembers( self, pointIndex, joinProtectMembers ):
		"""
		更新据点防守成员
		"""
		if pointIndex in self:
			self[pointIndex].joinProtectPlayerDBIDs = joinProtectMembers

	def getAllBHZBPointJoinAttackMembers( self ):
		"""
		获得所有参加进攻据点成员
		"""
		tempList =[]
		for pointData in self.values():
			tempList.extend( pointData.getPointJoinAttackMembers() )
		return tempList

	def getAllBHZBPointJoinProtectMembers( self ):
		"""
		获得所有参加防守据点成员
		"""
		tempList = []
		for pointData in self.values():
			tempList.extend( pointData.getPointJoinProtectMembers() )
		return tempList 

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in list(obj.values()):
			tempDict[ "datas" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BHZBPointDataMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBPointDataMgr )

g_BHZBPointDataMgrMgr = BHZBPointDataMgr()
g_BHZBPointData = BHZBPointData()

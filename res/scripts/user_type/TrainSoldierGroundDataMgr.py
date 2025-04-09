# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine

class TrainSoldierGroundData( object ):
	"""
	练兵场数据
	"""
	def __init__( self, lineNumber = 0, index = 0, occupyPlayerDBID = 0, occupyPlayerName = "", occupyPlayerProfession = 0, declareWarState = 1, declareWarTime = 0, declarePlayerName = "",
					declarePlayerDBID = 0,declarePlayerProfession = 0):
		self.lineNumber = lineNumber
		self.index = index
		self.occupyPlayerDBID = occupyPlayerDBID
		self.occupyPlayerName = occupyPlayerName
		self.occupyPlayerProfession = occupyPlayerProfession
		self.declareWarState = declareWarState
		self.declareWarTime = declareWarTime
		self.declarePlayerName = declarePlayerName
		self.declarePlayerDBID = declarePlayerDBID
		self.declarePlayerProfession = declarePlayerProfession

	def initData( self, dict ):
		self.lineNumber = dict[ "lineNumber" ]
		self.index = dict[ "index" ]
		self.occupyPlayerDBID = dict["occupyPlayerDBID"]
		self.occupyPlayerName = dict["occupyPlayerName"]
		self.occupyPlayerProfession = dict["occupyPlayerProfession"]
		self.declareWarState = dict["declareWarState"]
		self.declareWarTime = dict["declareWarTime"]
		self.declarePlayerName = dict["declarePlayerName"]
		self.declarePlayerDBID = dict["declarePlayerDBID"]
		self.declarePlayerProfession = dict["declarePlayerProfession"]

	def getDictFromObj( self, obj ):
		dict = {
			"lineNumber" 	: obj.lineNumber,
			"index"	: obj.index,
			"occupyPlayerDBID"  : obj.occupyPlayerDBID,
			"occupyPlayerName" 	: obj.occupyPlayerName,
			"occupyPlayerProfession": obj.occupyPlayerProfession,
			"declareWarState" : obj.declareWarState,
			"declareWarTime" 		: obj.declareWarTime,
			"declarePlayerName" 		: obj.declarePlayerName,
			"declarePlayerDBID" 		: obj.declarePlayerDBID,
			"declarePlayerProfession" 		: obj.declarePlayerProfession,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, TrainSoldierGroundData )

class TrainSoldierGroundDataMgr( dict ):
	"""
	沙盘大地图练兵场数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			if m.lineNumber not in self:
				self[m.lineNumber] = {}
			self[ m.lineNumber ][m.index] = m

	def addTrainSoldierGroundData( self, lineNumber = 0, index = 0, occupyPlayerDBID = 0, occupyPlayerName = "", occupyPlayerProfession = 0, declareWarState = 0, declareWarTime = 0,
									declarePlayerName = "",declarePlayerDBID = 0,declarePlayerProfession = 0 ):
		"""
		增加练兵场数据
		"""
		if lineNumber not in self:
			self[lineNumber] = {}
		if index in self[lineNumber]:
			del self[lineNumber][index]
		self[lineNumber][index] = TrainSoldierGroundData( lineNumber, index, occupyPlayerDBID, occupyPlayerName, occupyPlayerProfession, declareWarState, declareWarTime,declarePlayerName,declarePlayerDBID,declarePlayerProfession )

	def updateOccupyTrainSoldierGroundData( self, lineNumber, index, occupyPlayerDBID, occupyPlayerName,occupyPlayerProfession ):
		"""
		更新练兵场被占领数据
		"""
		if lineNumber not in self:
			self[lineNumber] = {}
		if index in self[lineNumber]:
			self[lineNumber][index].occupyPlayerDBID = occupyPlayerDBID
			self[lineNumber][index].occupyPlayerName = occupyPlayerName
			self[lineNumber][index].occupyPlayerProfession = occupyPlayerProfession
			self[lineNumber][index].declareWarTime = 0
			self[lineNumber][index].declareWarState = csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE
		else:
			self.addTrainSoldierGroundData( lineNumber, index, occupyPlayerDBID, occupyPlayerName,occupyPlayerProfession )

	def clearOtherIsOccupyPlayerDBIDGroundData( self, lineNumber, index ):
		"""
		清除其他是OccupyPlayerDBID练兵场数据
		"""
		if lineNumber not in self:
			return
		if index in self[lineNumber]:
			self[lineNumber][index].occupyPlayerDBID = 0
			self[lineNumber][index].occupyPlayerName = ""
			self[lineNumber][index].occupyPlayerProfession = 0
			self[lineNumber][index].declareWarTime = 0
			self[lineNumber][index].declareWarState = csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE

	def getOtherGroundLineNumberIsOccupyPlayer( self, occupyPlayerDBID ):
		"""
		获得其他被玩家占领的练兵场
		"""
		for lineNumber in self.keys():
			for trainGroundObj in self[lineNumber].values():
				if trainGroundObj.occupyPlayerDBID == occupyPlayerDBID:
					return trainGroundObj.lineNumber,trainGroundObj.index
		return 0,0

	def updateDeclareTrainSoldierGroundData( self, index, lineNumber,playerDBID, playerName, playerProfession, declareWarTime, declareWarState ):
		"""
		更新练兵场的宣战信息
		"""
		if lineNumber not in self:
			self[lineNumber] = {}
		if index in self[lineNumber]:
			self[lineNumber][index].declarePlayerDBID = playerDBID
			self[lineNumber][index].declarePlayerName = playerName
			self[lineNumber][index].declarePlayerProfession = playerProfession
			self[lineNumber][index].declareWarTime = declareWarTime
			self[lineNumber][index].declareWarState = declareWarState
		else:
			self.addTrainSoldierGroundData( lineNumber, index, 0, "",0,declareWarState, declareWarTime,playerName,playerDBID,playerProfession)

	def getTrainSoldierGroundData( self, lineNumber ):
		"""
		获得练兵场数据
		"""
		if lineNumber not in self:
			return {}
		tempDict = {}
		for index, trainGroundObj in self[lineNumber].items():
			tempDict[index] = str(trainGroundObj.occupyPlayerDBID)
		return tempDict

	def getOccupyPlayerDBIDDataByIndex( self, lineNumber, index ):
		"""
		通过编号 获得练兵场占领的玩家DBID
		"""
		if lineNumber in self and index in self[lineNumber]:
			return self[lineNumber][index].occupyPlayerDBID
		return 0

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in list(obj.values()):
			for obj in list(mObj.values()):
				tempDict[ "datas" ].append( obj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = TrainSoldierGroundDataMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, TrainSoldierGroundDataMgr )

g_TrainSoldierGroundDataMgr = TrainSoldierGroundDataMgr()
g_TrainSoldierGroundData = TrainSoldierGroundData()

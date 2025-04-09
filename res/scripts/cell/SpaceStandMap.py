# -*- coding: utf-8 -*-

from CoreObject.SpaceObject import SpaceObject
import Const
import KBEDebug
import csdefine
import KBEngine

class SpaceStandMap( SpaceObject ):
	"""
	沙盘大地图
	"""
	def __init__( self ):
		SpaceObject.__init__( self )
		self.setCurrentSpaceData( Const.SPACE_DATA_LINE_NUMBER,self.spaceKey )
		
	def setMaxLineNumber( self, maxLineNumber ):
		"""
		设置最大线数
		"""
		self.setCurrentSpaceData( Const.SPACE_DATA_MAX_LINE_NUMBER, str(maxLineNumber) )

	def onRequestTrainSoldierGroundDatasCB( self, trainSoldierGroundDatas ):
		"""
		请求该分线练兵场的数据
		"""
		self.getScript().onRequestTrainSoldierGroundDatasCB( self ,trainSoldierGroundDatas)

	def addTrainSoldierGroundData( self, lineNumber, index, occupyPlayerDBID, occupyPlayerName, occupyPlayerProfession, isCanBeDeclareWar, declareWarTime, declarePlayerName,declarePlayerDBID,declarePlayerProfession ):
		"""
		增加练兵场数据
		"""
		self.trainSoldierGroundMgr.addTrainSoldierGroundData(lineNumber, index, occupyPlayerDBID, occupyPlayerName, occupyPlayerProfession, isCanBeDeclareWar, declareWarTime, declarePlayerName,declarePlayerDBID,declarePlayerProfession)

	def registerRole( self, roleMB ):
		"""
		记录空间玩家
		"""
		SpaceObject.registerRole( self, roleMB )
		if roleMB.playerDBID not in self.spaceRoleDict:
			self.spaceRoleDict[roleMB.playerDBID] = roleMB

	def deregisterRole( self, roleMB ):
		"""
		删除空间玩家
		"""
		SpaceObject.deregisterRole( self, roleMB )
		if roleMB.playerDBID in self.spaceRoleDict:
			del self.spaceRoleDict[roleMB.playerDBID]

	def getRoleMBByPlayerDBID( self, playerDBID ):
		"""
		通过玩家DBID 获得玩家的Mailbox
		"""
		if playerDBID in self.spaceRoleDict:
			return self.spaceRoleDict[playerDBID]

		return None

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_NPC_TRAINSOLDIERGROUND:
			self.spaceTrainSoldierGroundDict[ entityMailBox.getIndex() ] = entityMailBox

	def delEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		删除entityMailBox 记录
		"""
		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_NPC_TRAINSOLDIERGROUND and entityMailBox.getIndex() in self.spaceTrainSoldierGroundDict:
			del self.spaceTrainSoldierGroundDict[entityMailBox.getIndex()]

	def getTrainSoldierGroundEntityByIndex( self, index ):
		"""
		"""
		if index in self.spaceTrainSoldierGroundDict:
			return self.spaceTrainSoldierGroundDict[index]
		return None

	def notifyTrainSoldierGroundOccupyed( self, index, playerDBID, playerName, playerProfession  ):
		"""
		通知某个练兵场被占领了
		"""
		lineNumber = int(self.getCurrentSpaceData( Const.SPACE_DATA_LINE_NUMBER ))
		self.trainSoldierGroundMgr.updateOccupyTrainSoldierGroundData( lineNumber, index, playerDBID, playerName, playerProfession )

		npcEntity = self.getTrainSoldierGroundEntityByIndex( index )
		if not npcEntity:
			return
		npcEntity.setOccupyData( playerDBID, playerName, playerProfession )

	def clearOtherIsOccupyPlayerDBIDGroundData( self, lineNumber, index ):
		"""
		清除该玩家占领的其他练兵场数据
		"""
		self.trainSoldierGroundMgr.clearOtherIsOccupyPlayerDBIDGroundData( lineNumber,index )
		npcEntity = self.getTrainSoldierGroundEntityByIndex( index )
		if not npcEntity:
			return
		npcEntity.setOccupyData(0,"",0)

	def notifySpaceNPCTrainSoldierGroundState( self, index ):
		"""
		改变练兵场状态
		"""
		lineNumber = int(self.getCurrentSpaceData( Const.SPACE_DATA_LINE_NUMBER ))
		self.trainSoldierGroundMgr.updateDeclareTrainSoldierGroundData( index, lineNumber,0, "", 0, "", csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE )
		npcEntity = self.getTrainSoldierGroundEntityByIndex( index )
		if not npcEntity:
			return
		npcEntity.setDclareWarState( csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE )

	def updateDeclareTrainSoldierGroundData( self, index, lineNumber,playerDBID, playerName, playerProfession, declareWarTime, declareWarState ):
		"""
		更新练兵场的宣战信息
		"""
		self.trainSoldierGroundMgr.updateDeclareTrainSoldierGroundData( index, lineNumber,playerDBID, playerName, playerProfession, declareWarTime, declareWarState )
		KBEngine.globalData["TrainSoldierGroundManager"].addDeclareTrainSoldierGroundDatas( index, lineNumber,playerDBID, playerName, playerProfession, declareWarTime, declareWarState )

	def openAllGroundDetail( self, roleOccupylineNumber, roleOccupytrainSoldierGroundIndex, roleMB, queryLineNumber, maxLineNumber, npcID ):
		"""
		打开练兵场所有面板详情
		"""
		trainGroundDict = self.trainSoldierGroundMgr.getTrainSoldierGroundData( queryLineNumber )
		roleMB.openAllGroundDetail( roleOccupylineNumber, roleOccupytrainSoldierGroundIndex, list(trainGroundDict.keys()), list( trainGroundDict.values() ), maxLineNumber, npcID )


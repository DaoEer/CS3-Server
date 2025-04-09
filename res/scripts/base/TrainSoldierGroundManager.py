# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
from CoreObject import MgrPersistentObject
import KST
from Functions import Functor
import csstatus
import csdefine

HOME_BARRACKS_SPACE = "fu_ben_L_LBCDBY"
STAND_MAP_SPACE = "fu_ben_L_LBCDDT"

class TrainSoldierGroundManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	练兵场管理器
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.declareWarDBIDs = [] 	# 已宣战的练兵场玩家DBID
		self.onCompleteInit()
		self.preCreateStandMap()

	def addJoinTrainGroundMembers( self, playerDBID ):
		"""
		增加进入练兵场玩家的DBID  根据进入人数去开启大本营
		"""
		if playerDBID not in self.joinTrainGroundMembers:
			self.joinTrainGroundMembers.append( playerDBID )
			spaceObj = KST.g_objFactory.getSpaceObject( STAND_MAP_SPACE )
			amount = spaceObj.getTriggerLinePlayerAmount()
			if self.checkJoinTrainGroundMembers( amount ): # 如果参加练兵场人数大于了沙盘的触发人数 则创建分线
				KBEngine.globalData["SpaceManager"].remoteCallDomain(STAND_MAP_SPACE,"requestNewSpace",({"enterAmount":len(self.joinTrainGroundMembers)},))

	def checkJoinTrainGroundMembers( self, amount ):
		"""
		"""
		if len(self.joinTrainGroundMembers) > amount:
			return True
		return False

	def preCreateStandMap( self ):
		"""
		预创建沙盘大地图
		"""
		if not len(self.joinTrainGroundMembers):
			return
		spaceObj = KST.g_objFactory.getSpaceObject( STAND_MAP_SPACE )
		amount = spaceObj.getTriggerLinePlayerAmount()
		needCreateStandMapNum = len(self.joinTrainGroundMembers) // amount + 1
		KBEngine.globalData["SpaceManager"].remoteCallDomain(STAND_MAP_SPACE,"preCreateSpace",(needCreateStandMapNum,))

	def enterHomeBarracks( self, playerMB, playerDBID ):
		"""
		玩家进入大本营
		"""
		self.addJoinTrainGroundMembers( playerDBID )
		spaceObj = KST.g_objFactory.getSpaceObject( HOME_BARRACKS_SPACE )
		enterPos, enterDir = spaceObj.getEnterInfo()
		playerMB.cell.gotoSpace( HOME_BARRACKS_SPACE,enterPos, enterDir )

	def enterStandMap( self, playerMB, position, direction, pickArgs ):
		"""
		进入沙盘大地图
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( STAND_MAP_SPACE )
		amount = spaceObj.getTriggerLinePlayerAmount()
		needCreateStandMapNum = len(self.joinTrainGroundMembers) // amount + 1
		pickArgs.update( {"needCreateStandMapNum":needCreateStandMapNum} )
		playerMB.gotoSpace( STAND_MAP_SPACE,position,direction,pickArgs )

	def requestTrainSoldierGroundDatas( self, spaceLineNumber, spaceMB ):
		"""
		请求某一分线练兵场数据
		"""
		trainSoldierGroundDatas = []
		if spaceLineNumber in self.trainSoldierGroundDatas:
			trainSoldierGroundDatas = list(self.trainSoldierGroundDatas[spaceLineNumber].values())

		spaceMB.cell.onRequestTrainSoldierGroundDatasCB( trainSoldierGroundDatas )

	def saveSpaceNPCInfo( self, guardData ):
		"""
		<define method>
		保存练兵场布防数据
		"""
		for npcInfo in self.spaceNPCInfos:
			if npcInfo["belongDBID"] == guardData["belongDBID"] and npcInfo["spaceScriptID"] == guardData["spaceScriptID"]:
				self.spaceNPCInfos.remove( npcInfo )
				break
		self.spaceNPCInfos.append( guardData )
		
	def requestSpaceNPCInfo( self, spaceCell, DBID, spaceScriptID ):
		"""
		<define method>
		请求练兵场布防数据
		"""
		for npcInfo in self.spaceNPCInfos:
			if npcInfo["belongDBID"] == DBID and npcInfo["spaceScriptID"] == spaceScriptID:
				spaceCell.onRequestSpaceNPCInfo( npcInfo["spaceDatas"] )
				return
		spaceCell.onRequestSpaceNPCInfo( [] )

	def addDeclareWarPlayer( self, playerDBID ):
		"""
		增加已宣战玩家DBID
		"""
		if playerDBID not in self.declareWarDBIDs:
			self.declareWarDBIDs.append( playerDBID )
	
	def removeDeclareWarPlayer( self, playerDBID ):
		"""
		移除已宣战玩家DBID
		"""
		if playerDBID in self.declareWarDBIDs:
			self.declareWarDBIDs.remove( playerDBID )

	def notifyDeclareWarPlayer( self, spaceLineNumber, trainSoldierGroundIndex, spaceName, playerDBID, npcEntity, occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict ):
		"""
		提示宣战玩家参加练兵场战斗
		"""
		KBEngine.lookUpEntityByDBID( "Role",playerDBID,Functor( self.notifyDeclareWarPlayerCallBack, spaceLineNumber, trainSoldierGroundIndex, spaceName,playerDBID, npcEntity,occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict ) )

	def notifyDeclareWarPlayerCallBack( self, spaceLineNumber, trainSoldierGroundIndex, spaceName,playerDBID, npcEntity,occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict,target ):
		"""
		"""
		if target is False:
			self.removeDeclareWarPlayer( playerDBID )
			npcEntity.clearDeclareWarData()
			return
		if target is True:
			self.removeDeclareWarPlayer( playerDBID )
			npcEntity.clearDeclareWarData()
			return
		target.cell.sendIsJoinDeclareWarMsg( spaceLineNumber, trainSoldierGroundIndex, spaceName, npcEntity,occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict )

	def notifyOccupyWarPlayer( self, spaceLineNumber, trainSoldierGroundIndex, spaceName, playerDBID, npcEntity, occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict ):
		"""
		提示占领玩家参加练兵场战斗
		"""
		KBEngine.lookUpEntityByDBID( "Role",playerDBID,Functor( self.notifyOccupyWarPlayerCallBack, spaceLineNumber, trainSoldierGroundIndex, spaceName,playerDBID, npcEntity,occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict ) )

	def notifyOccupyWarPlayerCallBack( self, spaceLineNumber, trainSoldierGroundIndex, spaceName,playerDBID, npcEntity,occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict,target ):
		"""
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.sendIsJoinDeclareWarMsg( spaceLineNumber, trainSoldierGroundIndex, spaceName, npcEntity,occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict )

	def notifyOccupyPlayer( self, occupyPlayerDBID, declareStr, enterStr, declareName ):
		"""
		通知占领玩家 有人宣战你的练兵场
		"""
		KBEngine.lookUpEntityByDBID( "Role",occupyPlayerDBID,Functor( self.notifyOccupyPlayerCallBack, declareStr, enterStr, declareName) )

	def notifyOccupyPlayerCallBack( self, declareStr, enterStr, declareName,target ):
		"""
		"""
		if target is False:
			return
		if target is True:
			return
		msg = declareStr + "|" + declareName + "|" + enterStr
		target.client.statusMessage( csstatus.TRAIN_SOLDIER_GROUND_DECLARWAR_MSG,msg )

	def queryIsDeclareWar( self, roleMB, playerDBID ):
		"""
		查询玩家是否已宣战
		"""
		if playerDBID in self.declareWarDBIDs:
			roleMB.cell.setIsDeclareWar( True )
		else:
			roleMB.cell.setIsDeclareWar( False )

	def queryRoleOccupyTrainGroundData( self, roleMB, playerDBID ):
		"""
		define method
		查询玩家占领练兵场数据
		"""
		lineNumber, index = self.trainSoldierGroundDatas.getOtherGroundLineNumberIsOccupyPlayer( playerDBID )
		roleMB.cell.setRoleOccupyTrainData( lineNumber, index )

	def addOccupyTrainSoldierGroundDatas( self, lineNumber, trainSoldierGroundIndex, playerDBID, playerName, playerProfession,playerMB ):
		"""
		define method
		更新练兵场占领数据
		"""
		srcOccPlayerDBID = self.trainSoldierGroundDatas.getOccupyPlayerDBIDDataByIndex( lineNumber, trainSoldierGroundIndex )
		if srcOccPlayerDBID:
			KBEngine.lookUpEntityByDBID( "Role",srcOccPlayerDBID,Functor( self.notifyOccupyPlayerClearOccupyData) )
		self.clearOtherIsOccupyPlayerDBIDGroundData(playerDBID)
		self.trainSoldierGroundDatas.updateOccupyTrainSoldierGroundData( lineNumber, trainSoldierGroundIndex, playerDBID, playerName, playerProfession )
		if playerMB != None:
			playerMB.cell.setRoleOccupyTrainData( lineNumber,trainSoldierGroundIndex )
		KBEngine.globalData["SpaceManager"].remoteCallDomain(STAND_MAP_SPACE,"notifySpaceTrainSoldierGroundOccupy",(lineNumber, trainSoldierGroundIndex, playerDBID, playerName, playerProfession))

	def notifyOccupyPlayerClearOccupyData( self, target ):
		"""
		清楚原有玩家占领该练兵场数据
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.setRoleOccupyTrainData(0,0)

	def clearOtherIsOccupyPlayerDBIDGroundData( self, occupyPlayerDBID ):
		"""
		清除该玩家占领的其他练兵场数据
		"""
		lineNumber, index = self.trainSoldierGroundDatas.getOtherGroundLineNumberIsOccupyPlayer( occupyPlayerDBID )
		self.trainSoldierGroundDatas.clearOtherIsOccupyPlayerDBIDGroundData( lineNumber, index )
		KBEngine.globalData["SpaceManager"].remoteCallDomain(STAND_MAP_SPACE,"clearOtherIsOccupyPlayerDBIDGroundData",( lineNumber, index ))

	def addDeclareTrainSoldierGroundDatas( self,index, lineNumber,playerDBID, playerName, playerProfession, declareWarTime, declareWarState ):
		"""
		define method
		更新练兵场宣战数据
		"""
		self.trainSoldierGroundDatas.updateDeclareTrainSoldierGroundData( index, lineNumber,playerDBID, playerName, playerProfession, declareWarTime, declareWarState )

	def changeNPCTrainSoldierGroundData( self, lineNumber, trainSoldierGroundIndex ):
		"""
		define method
		更新练兵场数据
		"""
		self.trainSoldierGroundDatas.updateDeclareTrainSoldierGroundData( trainSoldierGroundIndex, lineNumber,0, "", 0, "", csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE )
		KBEngine.globalData["SpaceManager"].remoteCallDomain(STAND_MAP_SPACE,"notifySpaceNPCTrainSoldierGroundState",( lineNumber, trainSoldierGroundIndex ))

	def openAllGroundDetail( self, roleOccupylineNumber, roleOccupytrainSoldierGroundIndex, roleMB, lineNumber, npcID ):
		"""
		define method
		打开练兵场所有面板详情
		"""
		KBEngine.globalData["SpaceManager"].remoteCallDomain( STAND_MAP_SPACE,"openAllGroundDetail",( roleOccupylineNumber, roleOccupytrainSoldierGroundIndex, roleMB, lineNumber, npcID ) )


# -*- coding: utf-8 -*-

import csdefine
import KBEngine
from BHZBPointSpaceSaveInfoMgr import BHZBPointSpaceSaveInfo
from ObjectScript.Space.SpaceCopy import SpaceCopy
import ItemTypeEnum
import KBEDebug
import Const
import csstatus
import Functions
import csconst
import time
import KBEMath
import Math
import Define

class SpaceCopyBHZBPointWarPVP( SpaceCopy ):
	"""
	帮会争霸 据点争夺战 PVP
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.itemDatas = {}				# { itemID : num }
		self.gridNum = 0
		self.delyCloseTime = 0
		self.enterProtectInfo = ()	# 进入防守方的位置
		self.enterAttackInfo = ()	# 进入进攻方位置数据
		self.belongAttackScriptIDs = []
		self.belongProtectScriptIDs = []
		self.reviveRadius = 0.0
		self.rewardIntegral = 0 	# 增加的积分值
		self.rewardRepeatIntegral = 0 #持续增加的积分值
		self.rewardRepeatTime = 0.0 # 持续增加时间
		self.addRewardExp = 0 # 增加经验值
		self.killRoleAddExp = 0 # 击杀玩家增加经验值
		self.killRoleAddContribution = 0 # 击杀玩家增加帮贡值
		self.dieAddReviveTime = 0.0 # 每次死亡增加的复活的时间
		self.maxDieNum = 0 # 死亡的最大次数
		self.dieKickOutTim = 0.0 # 死亡踢出去的时间

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		itemDatas = configData["SpaceData"].get( "ItemDatas", "" )
		if itemDatas:
			itemStrList = itemDatas.split("|") 
			for itemStr in itemStrList:
				iStr = itemStr.split(":")
				if len(iStr) >= 2:
					self.itemDatas.update({ int(iStr[0]) : int(iStr[1])})
		self.gridNum = configData["SpaceData"].get( "gridNum",0 )
		self.delyCloseTime = configData["SpaceData"].get( "delyCloseTime",0 )

		if configData["SpaceData"].get("enterPos",""):
			enterPosInfos = configData["SpaceData"].get("enterPos","").split("|")
			enterDirInfos = configData["SpaceData"].get("enterDir","").split("|")
			enterPosList = []
			enterDirList = []
			for enterPosInfo in enterPosInfos:
				pos = Functions.vector3TypeConvert(enterPosInfo)
				pos = KBEMath.Unreal2KBEnginePosition( pos )
				enterPosList.append(pos)

			for enterDirInfo in enterDirInfos:
				dir = Functions.vector3TypeConvert(enterDirInfo)
				dir = KBEMath.Unreal2KBEngineDirection( dir )
				enterDirList.append(dir)
			self.enterAttackInfo = (enterPosList[0],enterDirList[0] )
			if len(enterPosList) > 1 and len( enterDirList ) > 1:
				self.enterProtectInfo = (enterPosList[1],enterDirList[1] )

		self.belongAttackScriptIDs = configData["SpaceData"].get( "belongAttackScriptIDs","" ).split("|")
		self.belongProtectScriptIDs = configData["SpaceData"].get( "belongProtectScriptIDs","" ).split("|")
		self.reviveRadius = configData["SpaceData"].get( "reviveRadius", 0.0 )

		self.rewardIntegral = configData["SpaceData"].get("rewardIntegral", 0)
		self.rewardRepeatIntegral = configData["SpaceData"].get("rewardRepeatIntegral",0)
		self.rewardRepeatTime = float(configData["SpaceData"].get("rewardRepeatTime",0.0))
		self.addRewardExp = configData["SpaceData"].get("addRewardExp",0)
		self.killRoleAddExp = configData["SpaceData"].get("killRoleAddExp",0)
		self.killRoleAddContribution = configData["SpaceData"].get("killRoleAddContribution",0)
		self.dieAddReviveTime = configData["SpaceData"].get("dieAddReviveTime",0.0)
		self.maxDieNum = configData["SpaceData"].get("maxDieNum",0)
		self.dieKickOutTim = configData["SpaceData"].get("dieKickOutTim",0.0)

	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass

	def addEntityMailBoxRecord( self, selfEntity,scriptID, entityMailBox ):
		"""
		"""
		pass

	def getProtectEnterInfo( self ):
		"""
		获得防守方的进入信息
		"""
		return self.enterProtectInfo

	def getAttackEnterInfo( self ):
		"""
		获得进攻方的进入信息
		"""
		return self.enterAttackInfo

	def getBelongAttackScriptIDs( self ):
		"""
		"""
		return self.belongAttackScriptIDs

	def getBelongProtectScriptIDs( self ):
		"""
		"""
		return self.belongProtectScriptIDs

	def getReviveRadius( self ):
		return self.reviveRadius

	def getRewardIntegral( self ):
		return self.rewardIntegral

	def getRewardRepeatIntegral( self ):
		return self.rewardRepeatIntegral

	def getRewardRepeatTime( self ):
		return self.rewardRepeatTime

	def getAddRewardExp( self ):
		return self.addRewardExp

	def getKillRoleAddExp( self ):
		return self.killRoleAddExp

	def getKillRoleAddContribution( self ):
		return self.killRoleAddContribution

	def getDieAddReviveTime( self ):
		return self.dieAddReviveTime

	def getMaxDieNum( self ):
		return self.maxDieNum

	def getDieKickOutTim( self ):
		return self.dieKickOutTim

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		if not selfEntity.createArgs.get("isEnterDefense",0):
			camp = selfEntity.createArgs.get("camp",0)
			pointIndex = int(selfEntity.spaceKey.split("|")[0])
			KBEngine.globalData["BHZBManager"].requestBHZBPointSpaceSaveInfo( camp, pointIndex,selfEntity )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		if selfEntity.createArgs.get("isEnterDefense",0):
			if playerRole.getClient():
				playerRole.client.ShowExitPointSaveSpaceBtn()
		else:
			playerRole.setTemp("isEnter",True)
		if not selfEntity.lifeTime:
			self.startSpaceLife( selfEntity )
		playerRole.setBelongSide( packArgs.get("belongSide",0) )
		if playerRole.getBelongSide() == csdefine.BELONG_SIDE_ATTACK:
			enemyTongName = packArgs.get("belongTongName","")
		else:
			enemyTongName = packArgs.get( "declareTongName","" )
		selfEntity.addWarMember( playerRole.tongName, playerRole.tongDBID, packArgs.get("belongSide",0) , playerRole.playerDBID, playerRole, playerRole.getName(),enemyTongName )
		selfEntity.delayTransferDataToClient( playerRole )

	def addPlayerExtraItemBar( self, playerRole ):
		"""
		增加玩家额外物品栏
		"""
		playerRole.setUnLockSpaceCopyGridNum( self.gridNum )
		spaceCopyItemList = playerRole.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY)
		uidList = []
		for itemInst in spaceCopyItemList:
			uidList.append(str(itemInst.uid))
		if playerRole.getClient():
			playerRole.client.CreateExtraItemBar( self.gridNum, uidList )

	def removePlayerExtraItemBar( self, playerRole ):
		"""
		移除玩家额外物品栏
		"""
		playerRole.setUnLockSpaceCopyGridNum(0)
		if playerRole.getClient():
			playerRole.client.RemoveExtralItemBar()

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		belongSide = selfEntity.warMemberDatas.getBelongSideByTongDBID( playerRole.tongDBID )
		playerRole.setBelongSide( belongSide )
		if playerRole.getBelongSide() == csdefine.BELONG_SIDE_ATTACK:
			enemyTongName = selfEntity.createArgs.get("belongTongName","")
		else:
			enemyTongName = selfEntity.createArgs.get( "declareTongName","" )
		selfEntity.addWarMember( playerRole.tongName, playerRole.tongDBID, belongSide, playerRole.playerDBID, playerRole, playerRole.getName(),enemyTongName )
		selfEntity.delayTransferDataToClient( playerRole )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		if selfEntity.createArgs.get("isEnterDefense",0):
			if playerRole.getClient():
				playerRole.client.HideExitPointSaveSpaceBtn()
			self.removePlayerExtraItemBar(playerRole)
		else:
			playerRole.setCallArmyIndex( -1 )
			if selfEntity.isAllAttackSideOut():
				selfEntity.setGCZIsWin( False )

	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		SpaceCopy.onLastPlayerLeave( self, selfEntity, playerRole, packArgs )
		if selfEntity.createArgs.get("isEnterDefense",0):
			camp = selfEntity.createArgs.get("camp",0)
			pointIndex = int(selfEntity.spaceKey.split("|")[0])
			occupyTongDBID = int( selfEntity.spaceKey.split("|")[1] )
			tempSaveInfos = []
			for scriptID, mBoxs in selfEntity.getAllEntityMailBoxRecord().items():
				for mBox in mBoxs:
					obj = BHZBPointSpaceSaveInfo( pointIndex, scriptID, mBox.position, mBox.direction )
					tempSaveInfos.append( obj )

			KBEngine.globalData["BHZBManager"].saveBHZBPointSpaceInfo( camp,pointIndex,tempSaveInfos,occupyTongDBID,selfEntity.createArgs.get("groupID",0) )


	def onTeleportCompleted( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onTeleportCompleted( self, selfEntity, playerRole )
		if selfEntity.createArgs.get("isEnterDefense",0):
			self.addPlayerExtraItemBar( playerRole )
			for itemID,num in self.itemDatas.items():
				playerRole.addItemByID( itemID, num )
		
		#召唤部队
		if len(playerRole.getRoleArmyDatas()) > 0:
			armyIndex = selfEntity.getRoleRecordCallArmy( playerRole.playerDBID )
			if armyIndex == -1:		#等于-1说明玩家之前没有进过副本或没有部队
				armyIndex = playerRole.getDefaultArmyIndex()
			if armyIndex != -1:
				playerRole.callIDArmyToWar( armyIndex )
		
		if playerRole.queryTemp("isEnter",False):
			playerRole.statusMessage( csstatus.BHZB_ATTACK_PVPPOINT, selfEntity.createArgs.get("declareTongName",""), selfEntity.createArgs.get("belongTongName",""), selfEntity.createArgs.get("pointName","") )
			playerRole.removeTemp("isEnter")

	def onPlayerCallArmy( self, selfEntity, playerID, playerDBID, armyIndex ):
		"""
		玩家点击了出战
		"""
		selfEntity.updateRoleRecordCallArmy( playerDBID, armyIndex )

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLife = self.spaceLife
		if selfEntity.createArgs.get("isEnterDefense",0):
			spaceLife = int(selfEntity.createArgs.get("spaceLife",0))
		spaceLifeSecond = spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		tempTime = spaceLifeSecond
		if not selfEntity.createArgs.get("isEnterDefense",0):
			tempTime = spaceLifeSecond + self.delyCloseTime
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( (tempTime), "closeSpace", () )
		if not selfEntity.createArgs.get("isEnterDefense",0):
			selfEntity.addTimerCallBack( spaceLifeSecond, "setGCZIsWin", (False,) )
		totalTime = spaceLifeSecond
		if not selfEntity.createArgs.get("isEnterDefense",0):
			totalTime = spaceLifeSecond + self.delyCloseTime
		if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalTime - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		else:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalTime - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))

	def changeSpaceLife( self, selfEntity, dynamicTime ):
		"""
		改变计时
		"""
		selfEntity.popTimer( selfEntity.lifeTimer )
		selfEntity.lifeTimer = 0
		selfEntity.popTimer( selfEntity.lifeNotifyTimer )
		selfEntity.lifeNotifyTimer = 0
		
		selfEntity.dynamicTime += dynamicTime
		remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) - selfEntity.lifeTotalStopTime + selfEntity.dynamicTime
		if remainTime >= 0:
			tempTime = remainTime
			if not selfEntity.createArgs.get("isEnterDefense",0):
				tempTime = remainTime + self.delyCloseTime
			selfEntity.lifeTimer = selfEntity.addTimerCallBack( (tempTime), "closeSpace", () )
			if not not selfEntity.createArgs.get("isEnterDefense",0):
				selfEntity.addTimerCallBack( remainTime, "setGCZIsWin", (False,) )
			totalRemainTime = remainTime
			if not selfEntity.createArgs.get("isEnterDefense",0):
				totalRemainTime = remainTime + self.delyCloseTime
			if totalRemainTime - Const.SPACE_LIFE_NOTIFY_TIME >= 0:
				if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
					selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalRemainTime - Const.SPACE_LIFE_NOTIFY_TIME, \
																				"showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
				else:
					selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalRemainTime - Const.SPACE_LIFE_NOTIFY_TIME, \
																				"showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
			for e in selfEntity._spaceRoles:
				e.client.ShowSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ) )
		else:
			selfEntity.closeSpace()

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packDict = SpaceCopy.getPackDomainData( self, playerEntity, args )
		if "belongTongDBID" not in packDict:
			spaceEntity = playerEntity.getCurrentSpace()
			if spaceEntity:
				packDict["belongTongDBID"] = spaceEntity.createArgs.get("belongTongDBID", 0)
				packDict["camp"] = playerEntity.getCamp()
				packDict["pointIndex"] = spaceEntity.createArgs.get("pointIndex",0)
		camp = packDict["camp"]
		pointIndex = packDict["pointIndex"]
		occupyTongDBID = packDict["belongTongDBID"]
		packDict["spaceKey"] = "{0}|{1}".format(pointIndex, occupyTongDBID )
		return packDict

	def getReviveToExitInfo( self, playerRole ):
		KBEngine.globalData["BHZBManager"].onRoleLoginBHZB( playerRole.getCamp(),playerRole.tongDBID, playerRole.playerDBID,playerRole.base, playerRole.captainID )	
		KBEDebug.INFO_MSG("player(%s playerDBID = %d) exit SpaceCopyBHZBPointWarPVP"%(playerRole.getName(),playerRole.playerDBID) )
		return (self._exitScriptID, self._exitPosition, self._exitDirection )

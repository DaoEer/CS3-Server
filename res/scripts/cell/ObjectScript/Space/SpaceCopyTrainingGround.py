# -*- coding: utf-8 -*-

import time
import KBEMath
import Math
import KBEDebug
import csdefine
import Const
import csconst
import Functions
import csstatus
import Define
from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr

class SpaceCopyTrainingGround( SpaceCopy ):
	"""
	练兵场
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.teleportCD = 60		# 防守方传送CD
		self.enterProtectInfo = ()	# 进入防守方的位置
		self.enterAttackInfo = ()	# 进入进攻方位置数据
		self.bossName = ""			# 守方BOSS的名字
		self.teleportPosList = []	# 守方可传送的坐标
		self.teleportDirList =[]	# 传送朝向
		self.rewardExploitID = "" 	# 胜利奖励军功ID
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
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
		self.transformScriptIDs = {}
		idStr = configData["SpaceData"].get( "transformScriptIDs","" ).split("|")
		for ids in idStr:
			scriptIDList = ids.split(":")
			if len(scriptIDList) >= 2:
				self.transformScriptIDs[scriptIDList[0]] = scriptIDList[1]
		self.bossName = configData["SpaceData"].get( "bossName","" )
		
		self.teleportCD = int( configData["SpaceData"].get( "teleportCD","60" ) )
		if configData["SpaceData"].get("teleportPos",""):
			for posStr in configData["SpaceData"].get("teleportPos","").split("|"):
				self.teleportPosList.append( Math.Vector3( Functions.vector3TypeConvert(posStr)) )
		if configData["SpaceData"].get("teleportDir",""):
			for dirStr in configData["SpaceData"].get("teleportDir","").split("|"):
				self.teleportDirList.append( Math.Vector3( Functions.vector3TypeConvert(dirStr)) )

		self.rewardExploitID = configData["SpaceData"].get( "rewardExploitID","" )

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		if self.bossName:
			selfEntity.memberDatas.add(None, 0, self.bossName, csdefine.BELONG_SIDE_PROTECT)
		if selfEntity.belongDBID:					# 如果是占领的，就去请求保存好的数据
			KBEngine.globalData["LbcMgr"].requestSpaceNPCInfo( selfEntity, selfEntity.belongDBID, selfEntity.scriptID ) 		
	

	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
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
		
	def getTeleportInfo( self, position ):
		"""
		获取传送信息
		"""
		for pos, dir in zip( self.teleportPosList, self.teleportDirList ):
			if position.distTo( pos ) <= 2:
				return KBEMath.Unreal2KBEnginePosition( pos ), KBEMath.KBEngine2UnrealDirection(dir)
		return None, None

	def getBelongAttackScriptIDs( self ):
		return self.belongAttackScriptIDs

	def getBelongProtectScriptIDs( self ):
		return self.belongProtectScriptIDs
		
	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		if selfEntity.belongDBID != playerRole.playerDBID:
			playerRole.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		else:
			playerRole.setBelongSide( csdefine.BELONG_SIDE_PROTECT )
			
		selfEntity.memberDatas.add(playerRole, playerRole.id, playerRole.getName(), playerRole.getBelongSide())
		selfEntity.delayTransferDataToClient( playerRole )

	def onTeleportCompleted( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onTeleportCompleted( self, selfEntity, playerRole )
		
		#召唤部队
		if len(playerRole.getRoleArmyDatas()) > 0:
			armyIndex = selfEntity.getRoleRecordCallArmy( playerRole.playerDBID )
			if armyIndex == -1:		#等于-1说明玩家之前没有进过副本或没有部队
				armyIndex = playerRole.getDefaultArmyIndex()
			if armyIndex != -1:
				playerRole.callIDArmyToWar( armyIndex )

	def onPlayerCallArmy( self, selfEntity, playerID, playerDBID, armyIndex ):
		"""
		玩家点击了出战
		"""
		selfEntity.updateRoleRecordCallArmy( playerDBID, armyIndex )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		if selfEntity.belongDBID != playerRole.playerDBID:
			playerRole.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		else:
			playerRole.setBelongSide( csdefine.BELONG_SIDE_PROTECT )
		selfEntity.memberDatas.add(playerRole, playerRole.id, playerRole.getName(), playerRole.getBelongSide())
		selfEntity.delayTransferDataToClient( playerRole )
			
	def showTimeCountDown( self, selfEntity, statusID, remainTime ):
		"""
		副本时间结束
		"""
		SpaceCopy.showTimeCountDown( self, selfEntity, statusID, remainTime )
		self.onSpaceFailure( selfEntity )
			
	def onlyShowTimeCountDown( self, selfEntity ):
		""""""
		for roleCell in selfEntity._spaceRoles:
			roleCell.statusMessage( csstatus.SPACE_PLANE_CLOSE_NOTIFY, 10 )
			
	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		进攻方 占领成功
		"""
		selfEntity.isCopyOver = True
		self.stopSpaceLife( selfEntity )
		self.spaceEvent_onSpaceSuccess( selfEntity )
		if isShowTimeCountDown:
			selfEntity.addTimerCallBack( 60, "closeSpace", () )
			selfEntity.addTimerCallBackForScript( 50, "onlyShowTimeCountDown", () )
			for roleCell in selfEntity._spaceRoles:
				roleCell.statusMessage( csstatus.SPACE_SUCCESS_TELEPORT,60 )
		
		liftTime = int( time.time() - selfEntity.lifeStartTime )
		selfEntity.addTimerCallBackForScript(3, "delayShowResult", (1, liftTime))
		
		lbcItem = selfEntity.createArgs.get("lbcItem",None)

		rewardDatas = RewardMgr.g_rewardMgr.getReward(self.rewardExploitID,{})
		for player in selfEntity._spaceRoles:
			if player.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
				KBEngine.globalData["LbcMgr"].attackerWin(lbcItem.line, lbcItem.index, player, player.playerDBID, player.getName(), player.getProfession())
				player.statusMessage( csstatus.GROUND_ATTACK_SUCCESS, player.getName(), lbcItem.lbcName)
				RewardMgr.g_rewardMgr.doRewards( rewardDatas, player.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_OCCUPY_LBC )
			else:
				player.statusMessage( csstatus.GROUND_DEFENSE_FAIL, lbcItem.lbcName)

		
	def delayShowResult( self, selfEntity, isWin, liftTime ):
		"""延迟显示 结算界面"""
		successReward = 0
		rewardDatas = RewardMgr.g_rewardMgr.getReward(self.rewardExploitID,{})
		for rewardData in rewardDatas:
			if rewardData.get("type","") == csdefine.REWARD_TYPE_EXPLOIT:
				successReward += rewardData.get("amount",0)
		for player in selfEntity._spaceRoles:
			if player.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
				if isWin:
					player.client.CLIENT_OnLBCSpaceResult( successReward , 1, liftTime)
				else:
					player.client.CLIENT_OnLBCSpaceResult( 0 , 0, liftTime)
			else:
				if not isWin:
					player.client.CLIENT_OnLBCSpaceResult( successReward , 1, liftTime)
				else:
					player.client.CLIENT_OnLBCSpaceResult( 0 , 0, liftTime)
		
	def onSpaceFailure( self, selfEntity, isShowTimeCountDown = True ):
		"""
		进攻方 占领失败
		"""
		selfEntity.isCopyOver = True
		selfEntity.addTimerCallBackForScript(3, "delayShowResult", (0, self.spaceLife))
		if isShowTimeCountDown:
			selfEntity.addTimerCallBack( 60, "closeSpace", () )
			if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
				selfEntity.addTimerCallBackForScript( 50, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, 10 ) )
			else:
				selfEntity.addTimerCallBackForScript( 50, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, 10 ) )
			for roleCell in selfEntity._spaceRoles:
				roleCell.statusMessage( csstatus.SPACE_FAILUER_TELEPORT,60 )
		
		lbcItem = selfEntity.createArgs.get("lbcItem",None)
		for player in selfEntity._spaceRoles:
			if player.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
				player.statusMessage( csstatus.GROUND_ATTACK_FAIL, lbcItem.lbcName)
				KBEngine.globalData['LbcMgr'].attackerLose(lbcItem.line, lbcItem.index, player)
			else:
				player.statusMessage( csstatus.GROUND_DEFENSE_SUCCESS, player.getName(), lbcItem.lbcName)
		

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		if not selfEntity.isCopyOver:					# 活动还没结束
			if playerRole.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
				self.onSpaceFailure( selfEntity )
			else:
				self.onSpaceSuccess( selfEntity )

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packDict = SpaceCopy.getPackDomainData( self, playerEntity, args )
		lbcItem = packDict.get("lbcItem",None)
		if lbcItem and lbcItem.occupierDBID > 0:
			packDict["spaceKey"] = str(lbcItem.occupierDBID)

		return packDict

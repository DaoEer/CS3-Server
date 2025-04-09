# -*- coding: utf-8 -*-

import KBEMath
import Math
import Functions
import random
import csstatus
import time
from KBEDebug import *
from MsgLogger import g_logger
from ObjectScript.Space.SpaceCopy import SpaceCopy
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
from ConfigObject.BuildDepleteLoader import g_BuildDepleteLoader
from ImpInterface.SpaceStageExtInterface import SpaceStageExtInterface

class SpaceCopyDongFu( SpaceStageExtInterface, SpaceCopy ):
	def __init__( self ):
		SpaceCopy.__init__( self )
		SpaceStageExtInterface.__init__( self )
		self._activeRevivePos = Math.Vector3(0.0, 0.0, 0.0)
		self._activeReviveDir = Math.Vector3(0.0, 0.0, 0.0)
		self._challengePStageFile = ""					# 争夺战 守方副本阶段
		self._challengeAStageFile = ""					# 争夺战 防方副本阶段
		self._plunderPStageFile = ""					# 掠夺战 守方副本阶段
		self._plunderAStageFile = ""					# 掠夺战 防方副本阶段
		
		self.attackEntityScriptIDs = []					# 攻方entity的scriptID
		self.guardPos = Math.Vector3(0.0, 0.0, 0.0)		# 守卫刷新位置
		self.batteryScriptID = ""						# 默认火炮的scriptID
		self.batteryScriptIDs = []					# 所有火炮的scriptID
		self.batteryPosList = []						# 火炮刷新的位置（2个）
		self.batteryDirList = []						# 火炮刷新朝向
		self.petCorralScriptIDs = {}					# 兽栏的scriptID	{quality:scriptID}
		self.petCorralPosList = []						# 兽栏的门刷新位置（6个）
		self.petCorralDir = Math.Vector3(0.0, 0.0, 0.0)	# 兽栏的门刷新朝向
		self.originPetEggItems = []						# 原兽蛋配置

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		posStr = configData["SpaceData"].get( "activeRevivePos", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._activeRevivePos = KBEMath.Unreal2KBEnginePosition( pos )
		dirStr = configData["SpaceData"].get( "activeReviveDir", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._activeReviveDir = KBEMath.Unreal2KBEngineDirection( dir )
			
		self._challengeAStageFile = configData["SpaceData"].get( "challengeAStageFile", "" )
		self._challengePStageFile = configData["SpaceData"].get( "challengePStageFile", "" )
		self.initAckAndPctCSpaceStages( self._challengePStageFile, self._challengeAStageFile )
		
		self._plunderPStageFile = configData["SpaceData"].get( "plunderPStageFile", "" )
		self._plunderAStageFile = configData["SpaceData"].get( "plunderAStageFile", "" )
		self.initAckAndPctSpaceStages( self._plunderPStageFile, self._plunderAStageFile )
		
		self.attackEntityScriptIDs = [ i for i in configData["SpaceData"].get( "attackEntityScriptIDs", "" ).split("|") ]
		posStr = configData["SpaceData"].get( "guardPos", "" )
		if posStr:
			self.guardPos = KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( posStr ) )
		self.batteryScriptID = configData["SpaceData"].get( "batteryScriptID", "" )
		self.batteryScriptIDs = configData["SpaceData"].get( "batteryScriptIDList", "" ).split("|")
		posStr = configData["SpaceData"].get( "batteryPosList", "" )
		if posStr:
			for posS in posStr.split("|"):
				self.batteryPosList.append( KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( posS ) ) )
		dirStr = configData["SpaceData"].get( "batteryDirList", "" )
		if dirStr:
			for dirS in dirStr.split("|"):
				self.batteryDirList.append( KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( dirS ) ))
				
		petCorralScriptID = configData["SpaceData"].get( "petCorralScriptID", "" )
		if petCorralScriptID:
			for cScriptID in petCorralScriptID.split("|"):
				datas = cScriptID.split(":")
				if len( datas ) >= 2:
					self.petCorralScriptIDs[int(datas[0])] = datas[1]
		
		posStr = configData["SpaceData"].get( "petCorralPosList", "" )
		if posStr:
			for posS in posStr.split("|"):
				self.petCorralPosList.append( KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( posS ) ) )
		dirStr = configData["SpaceData"].get( "petCorralDir", "" )
		if dirStr:
			self.petCorralDir = KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( dirStr ) )
		
		petStr = configData["SpaceData"].get( "originPetEggItems", "" )
		if petStr:
			self.originPetEggItems = [int(i) for i in petStr.split("|")]
			
	def onSpaceSpawnPointLoadOver( self, selfEntity ):
		"""
		virtual method
		刷新点 加载完，才去请求！
		"""
		SpaceCopy.onSpaceSpawnPointLoadOver( self, selfEntity )
		belongDBID = selfEntity.createArgs.get("belongDBID", -1)
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestSpaceNPCInfo( selfEntity, belongDBID, selfEntity.scriptID )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		self.initPlayerEnterSpace( selfEntity, playerRole )
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		
	def initPlayerEnterSpace( self, selfEntity, playerRole ):
		"""玩家进入副本"""
		if selfEntity.belongDBID == playerRole.playerDBID:				# 进去自己的洞府
			playerRole.setBelongSide( csdefine.BELONG_SIDE_PROTECT )
			playerRole.delayRequestOriginPet()
			if selfEntity.isActivetyStart:
				guardList = selfEntity.getGuardIDList()
				if guardList:
					playerRole.client.initDFMonsterInfo( guardList )
		else:
			playerRole.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
			self.noticeAPlayerEnter( selfEntity, playerRole )
			if selfEntity.ghostList:
				playerRole.client.initDFMonsterInfo( selfEntity.ghostList )
		
		petData = selfEntity.getPetCorralData()
		if petData:
			playerRole.client.CLIENT_showOriginPetModel( petData )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		self.initPlayerEnterSpace( selfEntity, playerRole )
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		
	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		DEBUG_MSG( "Player(%s) leave space(%s)! reason:%s." % ( playerRole.id, selfEntity.id, packArgs[ "leaveReason" ] ) )
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )

	def getGuardPos( self ):
		"""获取 守卫刷新坐标"""
		return self.guardPos + Math.Vector3(random.randint(-2,2), 0, random.randint(-2,2))

	def getActiveReviveInfo( self ):
		"""获取活动时的复活坐标朝向"""
		return self._activeRevivePos, self._activeReviveDir
		
	def onFirstStageResult( self, selfEntity, isChallengeActive, result = 1):
		"""第一阶段结果"""
		if not result:					# 失败
			self._doReward( selfEntity, isChallengeActive, 1, result )
#			self.delayTeleportAttackPlayer( selfEntity, result )
			selfEntity.onChallengeActiveEnd( isChallengeActive )
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].onFinishDFActive( selfEntity.belongDBID )
		
	def _doReward( self, selfEntity, isChallengeActive, stage = 1, result = 1 ):
		"""执行奖励"""
		level = selfEntity.buildLevel[csdefine.LHMJ_BUIILD_LING_QUAN]
		isRewardAttack = False
		isRewardProtect = False
		# 0：攻方失败，1：攻方胜利，2：守方失败，3：守方胜利,4：第一阶段守方胜利，5：第一阶段攻方失败
		if stage == 1 and not result :
			cResultAttack = 5
			cResultProtect = 4
		else:
			cResultAttack = 1 if result else 0
			cResultProtect = 2 if result else 3
		startTime = int(selfEntity.activetyBeginTime)
		activeTime = int( time.time()) - selfEntity.activetyBeginTime
		for role in selfEntity._spaceRoles:
			if role.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
				isRewardAttack = True
				rewardIDs = g_BuildDepleteLoader.getActivityRewardID( level, role.getBelongSide(), stage, result )
				role.doActiveReward( isChallengeActive, cResultAttack, rewardIDs, selfEntity.isDestroyBuild, startTime, activeTime, selfEntity.attackDeadNum)
			else:
				isRewardProtect = True
				rewardIDs = g_BuildDepleteLoader.getActivityRewardID( level, role.getBelongSide(), stage, not result )
				role.doActiveReward( isChallengeActive, cResultProtect, rewardIDs, selfEntity.isDestroyBuild, startTime, activeTime, selfEntity.protectDeadNum)
		# 攻守方，有一方不在 洞府
		if not isRewardAttack:
			rewardIDs = g_BuildDepleteLoader.getActivityRewardID( level, csdefine.BELONG_SIDE_ATTACK, stage, result )
			gifts = g_BuildDepleteLoader.getActivityGiftID( level, csdefine.BELONG_SIDE_ATTACK, stage, result )
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].doActiveReward( selfEntity.belongDBID, csdefine.BELONG_SIDE_ATTACK, \
				cResultAttack, rewardIDs, gifts, selfEntity.isDestroyBuild, startTime, activeTime, selfEntity.attackDeadNum)
		if not isRewardProtect:
			rewardIDs = g_BuildDepleteLoader.getActivityRewardID( level, csdefine.BELONG_SIDE_PROTECT, stage, result )
			gifts = g_BuildDepleteLoader.getActivityGiftID( level, csdefine.BELONG_SIDE_PROTECT, stage, result )
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].doActiveReward( selfEntity.belongDBID, csdefine.BELONG_SIDE_PROTECT, \
				cResultProtect, rewardIDs, gifts, selfEntity.isDestroyBuild, startTime, activeTime, selfEntity.protectDeadNum)
		
	def delayTeleportAttackPlayer( self, selfEntity, result ):
		""""""
		for roleCell in selfEntity._spaceRoles:
			if roleCell.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
				if result:
					roleCell.statusMessage( csstatus.SPACE_SUCCESS_TELEPORT,60 )
				else:
					roleCell.statusMessage( csstatus.SPACE_FAILUER_TELEPORT,60 )
#		selfEntity.addTimerCallBackForScript( 60, "teleportAttackPlayer", () )			# 客户端 主动掉
		
	def noticeAPlayerEnter( self, selfEntity, playerRole ):
		"""攻方玩家进入洞府"""
		for player in selfEntity._spaceRoles:
			if player.isBelongSide( csdefine.BELONG_SIDE_PROTECT ):
				player.statusMessage( csstatus.DONG_FU_ENTER_BY_ATTACK, playerRole.getName() )
				return
		# 找不到守方玩家，就去mgr找
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].noticeAPlayerEnter( selfEntity.belongDBID, playerRole.getName())
		
	def teleportAttackPlayer( self, selfEntity ):
		"""将进攻方传送出副本"""
		for role in selfEntity._spaceRoles:
			if role.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
				role.gotoExitSpacePos()
		
	def onActiveResult( self, selfEntity, isChallengeActive, result ):
		"""掠夺战\争夺战 结果"""
		self._doReward( selfEntity, isChallengeActive, 2, result )
		selfEntity.onChallengeActiveEnd( isChallengeActive )
#		self.delayTeleportAttackPlayer( selfEntity, result )
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].onFinishDFActive( selfEntity.belongDBID )
		
	def onChallengeActiveStart( self, selfEntity ):
		"""
		活动开启
		"""
		if KBEngine.globalData.get( "LHMJ_ChallengeActive"):
			msg = "LHMJ_ChallengeActive"
		else:
			msg = "LHMJ_PlunderActive"
		self.onConditionChange( selfEntity, "", selfEntity.id, msg, "")
		
	def getPackDomainData( self, playerEntity, args ):
		""""""
		if "belongDBID" in args:
			args["spaceKey"] = str(args["belongDBID"])
		else:
			ERROR_MSG("player(%d) goto space(%s) err!!can not find spaceKey"%(playerEntity.id, self.scriptID))
		args["belongType"] = csdefine.SPACE_BELONG_PERSON
		args["playerDBID"] = playerEntity.playerDBID
		return args
		
	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass
		
	def onPlayerDie( self, selfEntity, playerID, playerMB ):
		"""
		"""
		playerRole = KBEngine.entities.get( playerID )
		if playerRole is None:
			return
		if playerRole.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
			selfEntity.attackDeadNum += 1
		else:
			selfEntity.protectDeadNum += 1
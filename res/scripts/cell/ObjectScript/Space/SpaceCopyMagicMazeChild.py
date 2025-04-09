# -*- coding: utf-8 -*-
import Const
import Math
import csstatus
import KBEMath
import KBEngine
import Functions
import csdefine
from ObjectScript import Space
from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
from MsgLogger import g_logger
import LogDefine
import time

class SpaceCopyMagicMazeChild( SpaceCopy ):
	"""
	幻阵迷宫 子副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
	
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.parentScriptID = configData["SpaceData"].get("parentScriptID", "")
		self.needLevel = configData["SpaceData"].get("needLevel", 0)
		self.teleportSkillID = int(configData["SpaceData"].get("teleportSkillID", 0))
		
	def onAllPlayerTeleportCompleted( self, selfEntity ):
		"""客户端所有玩家加载地图完成"""
		pass

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		KBEngine.globalData["MagicMazeSpaceManager"].setNextLevelLoading(belongType, spaceKey, playerRole.base, 0, 0,selfEntity.createArgs["mainScriptID"])
				
	def onStartTeleportToParent(self, selfEntity ):
		"""
		请求传送玩家到父副本
		"""
		if selfEntity.hasAllRoleTeleport:
			return
		
		if len(selfEntity._spaceRoles):
			teammates={}
			belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
			for playerCell in selfEntity._spaceRoles:											#全部传送
				player = KBEngine.entities.get( playerCell.id, None )
				if player:
					player.reviveOnOrigin()		#传送出副本前进行复活
					teammates[ player.playerDBID ] = player.base 
			pickArg = { "packBelongType": belongType, "spaceKey":spaceKey, "players": teammates, "mainScriptID":selfEntity.createArgs["mainScriptID"] }
			KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeParentSpace(belongType, spaceKey, pickArg)
			selfEntity.hasAllRoleTeleport = True
		
	def getPlayerBelongTypeAndSpaceKey(self, selfEntity):
		belongType = selfEntity.belongType
		spaceKey = selfEntity.spaceKey
		return selfEntity.belongType, selfEntity.spaceKey
	
	def onTeleportCompleted( self, selfEntity, playerRole ):
		"""
		"""
		KBEngine.globalData["MagicMazeSpaceManager"].setSpaceInParent(selfEntity.belongType, selfEntity.spaceKey, False,selfEntity.createArgs["mainScriptID"])

	def onPlaySpaceIntroduceVoice( self, selfEntity, playerRole ):
		"""
		播放场景语音
		"""
		if self.spaceIntroduce:
			playerRole.showMessagePlaySound( self.spaceIntroduce["voiceID"] )
	
	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本通关
		isShowTimeCountDown 是否显示倒计时提示 见JIRA-3404
		"""
		SpaceCopy.onSpaceSuccess( self, selfEntity, isShowTimeCountDown)
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		KBEngine.globalData["MagicMazeSpaceManager"].onChildSpaceSuccess(belongType, spaceKey, selfEntity.scriptID,selfEntity.createArgs["mainScriptID"])
		for roleCell in selfEntity._spaceRoles:
			roleCell.statusMessage( csstatus.HUAN_ZHEN_MI_GONG_SUCCESS_MSG, "" )
			selfEntity.addTimerCallBackForScript( 1.2, "onAddExtraReward", ( roleCell, ) )
	
	def onSpaceFailure( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本失败
		isShowTimeCountDown 是否显示倒计时提示 见JIRA-3404
		"""
		SpaceCopy.onSpaceFailure( self, selfEntity, isShowTimeCountDown)
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		KBEngine.globalData["MagicMazeSpaceManager"].onChildSpaceFailure(belongType, spaceKey, selfEntity.scriptID,selfEntity.createArgs["mainScriptID"])
		for roleCell in selfEntity._spaceRoles:
			roleCell.statusMessage( csstatus.HUAN_ZHEN_MI_GONG_FAILURE_MSG, "" )
		
	def onPlayerDie( self, selfEntity, playerID, playerMB ):
		"""
		玩家死亡
		"""
		SpaceCopy.onPlayerDie(self, selfEntity, playerID, playerMB )
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		KBEngine.globalData["MagicMazeSpaceManager"].onChildSpacePlayerDie(belongType, spaceKey, selfEntity.scriptID, playerID, playerMB,selfEntity.createArgs["mainScriptID"])
	
	def onAddPotential( self, selfEntity, playerRole, potential, reason):
		"""
		增加潜能
		"""
		SpaceCopy.onAddPotential( self, selfEntity, playerRole, potential, reason)
	
	def onAddExtraReward( self, selfEntity, playerRole ):
		"""
		获取额外奖励
		"""
		if playerRole.playerDBID in selfEntity.recordAddPotential:
			extraPotential = int(selfEntity.recordAddPotential[playerRole.playerDBID] * selfEntity.extraRewardRate)
			if extraPotential:
				playerRole.addPotential( extraPotential, csdefine.POTENTIAL_ADD_REASON_SPACE_SENTLEMENT )
				useTime = int(time.time() - spaceEntity.lifeStartTime)
				g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, playerRole.accountDBID, playerRole.playerDBID, playerRole.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_POTENTIAL, str(extraPotential), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
			playerRole.client.CLIENT_ShowLuckExtraReward( extraPotential )
			
		
	def onSetSpaceExtraReward( self, selfEntity, extraRewardCount, extraRewardRate, extraBuffBonus):
		selfEntity.extraRewardCount = extraRewardCount
		selfEntity.extraRewardRate = extraRewardRate
		selfEntity.extraBuffBonus = extraBuffBonus
		if extraBuffBonus != 0:
			for player in selfEntity._spaceRoles:
				player.addBuff( player, extraBuffBonus )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		for player in selfEntity._spaceRoles:
			if selfEntity.extraBuffBonus != 0:
				player.removeBuffByID(selfEntity.extraBuffBonus)
	
	def onCloseSpace( self, selfEntity, isEnter):
		self.onStartTeleportToParent(selfEntity)

	def onClickedBtnGotoExitSpace( self, selfEntity, playerRole ):
		"""
		玩家点击退出副本按钮
		"""
		if selfEntity.belongType == csdefine.SPACE_BELONG_PERSON:
			KBEngine.globalData["MagicMazeSpaceManager"].deregister( selfEntity.belongType, selfEntity.spaceKey,selfEntity.createArgs["mainScriptID"] )
			
	def showTimeCountDown( self, selfEntity, statusID, remainTime ):
		"""
		所有玩家显示读秒倒计时
		"""
		SpaceCopy.showTimeCountDown( self, selfEntity, statusID, remainTime )
		if self.teleportSkillID and len(selfEntity._spaceRoles):
			for role in selfEntity._spaceRoles:
				role.useSkillToEntity(self.teleportSkillID, role.id)
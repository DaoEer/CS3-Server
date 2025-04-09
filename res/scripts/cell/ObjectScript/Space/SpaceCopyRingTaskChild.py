# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import json
import Functions
import KBEMath
import Math
import KBEDebug
import csdefine
import Define
import KBEngine

class SpaceCopyRingTaskChild( SpaceCopy ):
	"""
	环任务秘境 子副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		self.logoutCloseTime = configData["SpaceData"].get( "logoutCloseTime", 1.0 )

	def onStartTeleportParentScene( self, selfEntity, player ):
		"""
		开始传送进主场景
		"""
		spaceKey = str( player.playerDBID )
		belongType = csdefine.SPACE_BELONG_PERSON
		KBEngine.globalData["RingTaskSpaceMgr"].setIsInMainScene( spaceKey, True )
		questID = player.loopQuest["loopQuestList"][0]
		pickArgs = { "packBelongType": belongType, "spaceKey":spaceKey }
		player.gotoRingTaskSpace( selfEntity.scriptID, str(questID), pickArgs, True )

	def onPlaySpaceIntroduceVoice( self, selfEntity, playerRole ):
		"""
		播放场景语音
		"""
		pass

	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		spaceKey = str( playerRole.playerDBID )
		KBEngine.globalData["RingTaskSpaceMgr"].setIsInMainScene( spaceKey, True )
		if selfEntity.belongType == csdefine.SPACE_BELONG_PERSON and packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_LOGOUT:		# 单人下线
			selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( self.logoutCloseTime, "closeSpace", () )
		elif selfEntity.belongType == csdefine.SPACE_BELONG_PERSON and packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_TELEPORT:	# 单人传送
			selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 5.0, "closeSpace", () )

	def onCloseSpace( self, selfEntity ):
		"""
		关闭副本之前做的事
		"""
		for player in selfEntity._spaceRoles:
			spaceKey = str( player.playerDBID )
			belongType = csdefine.SPACE_BELONG_PERSON
			KBEngine.globalData["RingTaskSpaceMgr"].setIsInMainScene( spaceKey, True )
			if len(player.loopQuest["loopQuestList"]) > 0:
				questID = player.loopQuest["loopQuestList"][0]
				KBEngine.globalData["RingTaskSpaceMgr"].setPreloadSpace( player.base, spaceKey, str(questID), 1 )
				pickArgs = { "packBelongType": belongType, "spaceKey":spaceKey }
				player.gotoRingTaskSpace( selfEntity.scriptID, str(questID), pickArgs, True )
			player.gotoExitSpacePos()
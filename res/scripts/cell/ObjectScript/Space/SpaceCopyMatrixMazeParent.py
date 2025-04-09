# -*- coding: utf-8 -*-
import Const
import Math
import KBEMath
import KBEngine
import Functions
import csdefine
from KBEDebug import *
from ObjectScript import Space
from ObjectScript.Space.SpaceCopy import SpaceCopy


class SpaceCopyMatrixMazeParent( SpaceCopy ):
	"""
	幻阵迷宫 父副本 第三版
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.children = {}
		self.needLevel = 0
		self.flyDelayTime = 0.0
		self.flyVoiceID = []
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		for key, value in configData["SpaceData"].get("children", {}).items():
			self.children[int(key)] = value
		self.needLevel = configData["SpaceData"].get("needLevel", 0)
		self.flyVoiceID = configData["SpaceData"].get( "flyVoiceID", "").split("|")
		self.flyDelayTime = float(configData["SpaceData"].get( "flyDelayTime", 0.0 ))

	def getFlyInfo( self, index ):
		"""
		获得飞行数据
		"""
		datas = self.children[index]
		patrolID = datas["flyPatrolID"]
		enterPos = Math.Vector3(0.0, 0.0, 0.0)
		enterPosStr = datas.get("enterPos", "")
		enterPosConvert = Functions.vector3TypeConvert( enterPosStr )
		if enterPosConvert:
			enterPos = enterPosConvert
		return patrolID, datas["patrolPoint"], enterPos
	
	def getSceneDelayTime( self, index ):
		"""
		获取播放镜头后延迟传送的时间
		"""
		datas = self.children[index]
		return datas["sceneDelayTime"]
	
	def getChildNeedLevel(self):
		"""
		"""
		return self.needLevel

	def getFlyVoiceID( self, index ):
		"""
		获取起飞语音ID
		"""
		return self.flyVoiceID[ index ]

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		KBEngine.globalData["MagicMazeSpaceManager"].setNextLevelLoading(belongType, spaceKey, playerRole.base, 0, 0,selfEntity.createArgs["mainScriptID"])
		
	def onTeleportCompleted( self, selfEntity, playerRole ):
		"""
		"""
		KBEngine.globalData["MagicMazeSpaceManager"].setSpaceInParent( selfEntity.belongType, selfEntity.spaceKey, True,selfEntity.createArgs["mainScriptID"])
		if selfEntity.progress == 0:
			if selfEntity.copyIsComplet:
				selfEntity.addTimerCallBack( 3.0, "onStopStory", ())
			elif self.spaceIntroduce:
				playerRole.showMessagePlaySound( self.spaceIntroduce["voiceID"] )
		else:
			if selfEntity.progress <3 and selfEntity.firstEndFlyPlayer:
				selfEntity.firstEndFlyPlayer = False
				selfEntity.onClientStartMove( playerRole, selfEntity.flySpeed )
				selfEntity.onPlaySoundAndNotifyResult()
			else:
				selfEntity.addTimerCallBack( 3.0, "onStopStory", ())
		
	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		if Const.MAZE_SPACE_MAIN_SCENE not in packArgs:
			belongType = csdefine.SPACE_BELONG_PERSON
			spaceKey = str( playerRole.playerDBID )
			if playerRole.isInTeam():
				belongType = csdefine.SPACE_BELONG_TEAM
				spaceKey = str( playerRole.teamMailbox.id )
			KBEngine.globalData["MagicMazeSpaceManager"].deregister( belongType,spaceKey,selfEntity.createArgs["mainScriptID"] )
			KBEngine.globalData["MagicMazeSpaceManager"].setSpaceExtraReward( belongType, spaceKey, -1, 0.0,selfEntity.createArgs["mainScriptID"] )
			selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 1.0, "closeSpace", () )
	
	def onStartTeleportToChild(self, selfEntity, player, belongType ):
		"""
		请求传送玩家到子副本
		"""
		teammates = {}
		spaceLevel = min( self.getChildNeedLevel() + 19, player.getLevel() )	#怪物等级上限为副本开放等级+19级（CST-2880）
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		if belongType == csdefine.SPACE_BELONG_PERSON:								#个人模式
			teammates[player.playerDBID] = player.base
		elif belongType == csdefine.SPACE_BELONG_TEAM:								#组队模式
			for playerCell in selfEntity._spaceRoles:										#队员
				teamMember = KBEngine.entities.get( playerCell.id, None )
				if not teamMember:
					continue
				if player.isTeammate( teamMember.id ):
					teammates[ teamMember.playerDBID ] = teamMember.base 
					
		pickArg = { "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "players": teammates,"mainScriptID":selfEntity.createArgs["mainScriptID"]}
		KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeChildSpace(belongType, spaceKey, pickArg)

	def onChildSpaceFailure(self, selfEntity):
		self.spaceSettlement_onChildSpaceFailure(selfEntity)
		
	def getPlayerBelongTypeAndSpaceKey(self, selfEntity):
		return selfEntity.belongType,selfEntity.spaceKey
		
	def onTeamCaptainChange(self, selfEntity):
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		if belongType != csdefine.SPACE_BELONG_PERSON:
			for playerCell in selfEntity._spaceRoles:
				player = KBEngine.entities.get( playerCell.id, None )
				if player:
					player.client.ShowMazeDice( player.isTeamCaptain() )
					
	def onCloseSpace( self, selfEntity, isEnter):
		if isEnter:
			for roleCell in selfEntity._spaceRoles:
				roleCell.gotoExitSpacePos()
		else:
			for roleBase in selfEntity._readyEnterRoles:
				roleBase.cell.gotoExitSpacePos()

	def onStopOtherPlayerFly( self, selfEntity ):
		"""
		点击传送门,其他玩家还在飞行则通知客户端停止飞行
		"""
		for playerCell in selfEntity._spaceRoles:
			if playerCell.id not in selfEntity.playerNotEndFlyList:
				selfEntity.onMagicMazeEndFly( playerCell )
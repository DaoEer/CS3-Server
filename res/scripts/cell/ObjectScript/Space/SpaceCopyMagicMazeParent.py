# -*- coding: utf-8 -*-
import Const
import Math
import KBEMath
import KBEngine
import Functions
import csdefine
import KBEDebug
from ObjectScript import Space
from ObjectScript.Space.SpaceCopy import SpaceCopy


class SpaceCopyMagicMazeParent( SpaceCopy ):
	"""
	幻阵迷宫 父副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.children = {}
		self.needLevel = 0
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		for key, value in configData["SpaceData"].get("children", {}).items():
			self.children[int(key)] = value
		self.needLevel = configData["SpaceData"].get("needLevel", 0)
		
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
	
	def gotoChildSpaceCopy( self, selfEntity ):
		"""
		传送到子副本
		"""
		index = selfEntity.progress
		datas = self.children[index]
		scriptID = datas["scriptID"]
		pos, dire = self.getChildPosAndDire( index )
		for playerRole in selfEntity._spaceRoles:
			playerRole.gotoSpaceUseArg( scriptID, pos, dire, {} )
		
	def onTeleportCompleted( self, selfEntity, playerRole ):
		"""
		"""
		KBEngine.globalData["MagicMazeSpaceManager"].setSpaceInParent(selfEntity.belongType, selfEntity.spaceKey, True,selfEntity.createArgs["mainScriptID"])
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		if selfEntity.progress == 0:
			if self.spaceIntroduce:
				playerRole.showMessagePlaySound( self.spaceIntroduce["voiceID"] )
			playerRole.client.ShowMazeDice(False)
		else:
			if belongType == csdefine.SPACE_BELONG_PERSON:
				playerRole.client.ShowMazeDice(True)
			else:
				playerRole.client.ShowMazeDice( playerRole.isTeamCaptain() )
		
	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		pass
	
	def onStartTeleportToChild(self, selfEntity):
		teammates = []
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if not player.isTeamCaptain():
				teammates.append( playerCell.base )
		isPlayerInTeam = False
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player and player.isInTeam() and player.isTeamCaptain():
				belongType = csdefine.SPACE_BELONG_TEAM
				spaceKey = str( player.teamMailbox.id )
				spaceLevel = min( self.getChildNeedLevel() + 19, player.getLevel() )	#怪物等级上限为副本开放等级+19级（CST-2880）
				KBEngine.globalData["MagicMazeSpaceManager"].setSpaceInParent(belongType, spaceKey, False,selfEntity.createArgs["mainScriptID"])
				pickArg = { "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "teammates": teammates, "mainSpace":""}
				pickArg.update({"mainScriptID":selfEntity.createArgs["mainScriptID"]})
				isPlayerInTeam = True
				player.gotoMagicMazeSpace(belongType, selfEntity.scriptID, pickArg)
		
		if not isPlayerInTeam:
			for playerCell in selfEntity._spaceRoles:
				player = KBEngine.entities.get( playerCell.id, None )
				if player:
					belongType = csdefine.SPACE_BELONG_PERSON
					spaceKey = str( player.playerDBID )
					spaceLevel = min( self.getChildNeedLevel() + 19, player.getLevel() )	#怪物等级上限为副本开放等级+19级（CST-2880）
					KBEngine.globalData["MagicMazeSpaceManager"].setSpaceInParent(belongType, spaceKey, False,selfEntity.createArgs["mainScriptID"])
					pickArg = { "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "mainSpace":""}
					pickArg.update({"mainScriptID":selfEntity.createArgs["mainScriptID"]})
					player.gotoMagicMazeSpace(belongType, selfEntity.scriptID, pickArg)
					
	
	def onChildSpaceFailure(self, selfEntity):
		self.spaceSettlement_onChildSpaceFailure(selfEntity)
		
	def getPlayerBelongTypeAndSpaceKey(self, selfEntity):
		belongType = csdefine.SPACE_BELONG_PERSON
		spaceKey = ""
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			spaceKey = str( player.playerDBID )
			if player and player.isInTeam() and player.isTeamCaptain():
				belongType = csdefine.SPACE_BELONG_TEAM
				spaceKey = str( player.teamMailbox.id )
				break
		return belongType,spaceKey
		
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

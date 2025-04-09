# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine
import KBEMath
import Functions
import csdefine
import Math
import time
import KBEDebug

class SpaceCopyShiFangCheng( SpaceCopy ):
	"""
	十方城
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.activityBunch = ""
		self.currentActivityName = ""
		self.nextActDoorData = {}
		self.completeStage1 = 0.0
		self.readyTime = 60.0
		self.destroyTime = 300.0
		self.stageListStr = []		

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )

		self.activityBunch = configData["SpaceData"].get("activityBunch","")
		self.currentActivityName = configData["SpaceData"].get( "currentActivityName","" )

		self.nextActDoorData["activityBunch"] = self.activityBunch
		self.nextActDoorData["activityName"] = configData["SpaceData"].get("nextActivityName","")
		self.nextActDoorData["position"] = Math.Vector3(0,0,0)
		self.nextActDoorData["direction"] = Math.Vector3(0,0,0)
		posStr = configData["SpaceData"].get( "doorPos", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			pos = KBEMath.Unreal2KBEnginePosition( pos )
			self.nextActDoorData["position"] = Math.Vector3(pos)
		
		dirStr = configData["SpaceData"].get( "doorDir", "" )
		direction = Functions.vector3TypeConvert( dirStr )
		if direction:
			direction = KBEMath.Unreal2KBEnginePosition( direction )
			self.nextActDoorData["direction"] = Math.Vector3(direction)
		self.doorScriptID = configData["SpaceData"].get( "doorScriptID","" )
		self.stageListStr = configData["SpaceData"].get("stageListStr","").split("|") #["1 2 3","4 5 6"]
		self.wallID = configData["SpaceData"].get("wallID","")

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		self.startLifeOnInit = 0
		SpaceCopy.initEntity( self, selfEntity )

	def getWallID( self ):
		return self.wallID

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		self.playerEnter( selfEntity, playerRole )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		self.playerEnter( selfEntity, playerRole )

	def onTeleportCompleted( self, selfEntity, playerRole ):
		SpaceCopy.onTeleportCompleted( self, selfEntity, playerRole )
		KBEngine.globalData["PersonStarcraftMgr"].showPassShiFangChengByLogin( self.scriptID, playerRole.base)

	def playerEnter( self, selfEntity, playerRole ):
		"""
		"""
		if selfEntity.readyDestroyTimer:
			selfEntity.popTimer(selfEntity.readyDestroyTimer)
			selfEntity.readyDestroyTimer = 0
		needTime = time.time() - selfEntity.startTime
		if needTime <= self.readyTime:
			remainTime = self.readyTime - needTime
			if remainTime > 10.0:
				playerRole.addTimerCallBack( remainTime - 10.0,"ShowCountDown",(10,) )
			else:
				playerRole.ShowCountDown( int(remainTime) )
			selfEntity.addTimerCallBack(remainTime,"destroyWall",())
		else:
			selfEntity.destroyWall()
		
	def activityStart( self, selfEntity,useStageIndex ):
		"""
		活动开始
		"""
		#self.startSpaceLife( selfEntity )
		selfEntity.startTime = time.time()
		selfEntity.useStageIndex = useStageIndex
		selfEntity.addTimerCallBackForScript( self.readyTime, "startSpaceLife",())
		selfEntity.readyDestroyTimer = selfEntity.addTimerCallBack(self.destroyTime,"onReady" ,())

	def activityEnd( self, selfEntity ):
		"""
		活动结束
		"""
		self.passFailure( selfEntity )

	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本通关
		"""
		SpaceCopy.onSpaceSuccess( self, selfEntity, isShowTimeCountDown)
		for player in selfEntity._spaceRoles:
			passTime = int(time.time() - selfEntity.startTime)
			#player.actBunch_joinNext( self.activityBunch, self.currentActivityName, {"passTime" : passTime } )
			KBEngine.globalData["PersonStarcraftMgr"].addYeZhanFengQiMember( self.scriptID,player.base,player.getName(), player.playerDBID ,passTime )

	def passFailure( self, selfEntity ):
		"""
		通关失败
		"""
		pass

	def passSuccess( self, selfEntity ):
		"""
		通关成功 已成功报名下一场
		"""
		selfEntity.createEntityByScriptID( self.doorScriptID, self.nextActDoorData["position"], self.nextActDoorData["direction"],{} )

	def onStageComplete( self, selfEntity ):
		"""
		完成某阶段
		"""
		useTime = time.time() - selfEntity.stageStartTime
		for player in selfEntity._spaceRoles:
			stageListStr = self.stageListStr[selfEntity.useStageIndex]
			stageList = [int(i) for i in stageListStr.split(" ")]
			currentStageIndex = stageList.index(selfEntity.spaceStage.stageIndex)
			if currentStageIndex < len(stageList):
				KBEngine.globalData["PersonStarcraftMgr"].completeShiFangChengStage( self.scriptID,player.base, player.playerDBID, player.getName(), currentStageIndex + 1, useTime )

		selfEntity.completeSpaceStages.append( selfEntity.spaceStage.stageIndex )
		for roleCell in selfEntity._spaceRoles:
			roleCell.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_SPACE_STAGE_COMPLETE )
			roleCell.client.CLIENT_updateCompleteSpaceStage( self.getCompleteSpaceStageName( selfEntity ) )
			roleCell.client.CLIENT_ClearSpaceStageTaskArea()

		self.setNextStage( selfEntity )

	def setNextStage( self, selfEntity ):
		"""
		"""
		oldStageIndex = selfEntity.spaceStage.stageIndex
		selfEntity.spaceStage = None
		selfEntity.stageStartTime = 0.0
		self.spaceEvent_onStageComplete( selfEntity, oldStageIndex )
		stageListStr = self.stageListStr[selfEntity.useStageIndex]
		stageList = [int(i) for i in stageListStr.split(" ")]
		index = stageList.index(oldStageIndex)
		if len(stageList) and index < len(stageList) - 1:
			if self.beginOnInit:
				self.setSpaceStage( selfEntity, stageList[index + 1] )

	def spaceStage_onSpaceInit( self, selfEntity ):
		"""
		"""
		selfEntity.spaceStage = None # 初始值需要为None，而因为是define属性，此值会是一个SpaceStageDataType对象，不为None，因此手动赋一下值。
		if len( self.spaceStages ) and self.beginOnInit:
			stageListStr = self.stageListStr[selfEntity.useStageIndex]
			stageList = [int(i) for i in stageListStr.split(" ")]
			self.setSpaceStage( selfEntity, stageList[0] )

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
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader

class SpaceCopyRingTask( SpaceCopy ):
	"""
	环任务秘境
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.questIDs = [] #休闲类任务ID

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		if configData["SpaceData"].get("xiuXianQuestID",""):
			self.questIDs = [ int(i) for i in configData["SpaceData"].get("xiuXianQuestID","").split("|") ]

	def onStartTeleportChildScene( self, selfEntity, player ):
		"""
		开始传送进子场景
		"""
		spaceKey = str( player.playerDBID )
		belongType = csdefine.SPACE_BELONG_PERSON
		KBEngine.globalData["RingTaskSpaceMgr"].setIsInMainScene( spaceKey, False )
		questID = player.loopQuest["loopQuestList"][0]
		KBEngine.globalData["RingTaskSpaceMgr"].setPreloadSpace( player.base, spaceKey, str(questID), 0 )
		pickArgs = { "packBelongType": belongType, "spaceKey":spaceKey }
		player.gotoRingTaskSpace( selfEntity.scriptID, str(questID), pickArgs, True )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		stageIndex = packArgs["stageIndex"]
		taskIndex = packArgs["taskIndex"]
		self.setCurrentStage( selfEntity, playerRole, stageIndex, taskIndex )
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		if playerRole.getClient():
			playerRole.client.ShowLoopQuestWin()

	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 2.0, "closeSpace", () )

	def onCloseSpace( self, selfEntity ):
		"""
		关闭副本之前做的事
		"""
		for roleCell in selfEntity._spaceRoles:
			roleCell.gotoExitSpacePos()

	def onPlaySpaceIntroduceVoice( self, selfEntity, playerRole ):
		"""
		播放场景语音
		"""
		pass

	def onTeleportCompleted( self, selfEntity, playerRole ):
		# 播放场景语音
		SpaceCopy.onTeleportCompleted( self, selfEntity, playerRole )
		# if self.hasSpaceStage( selfEntity ):
		# 	if self.isStageIndexLowerThanRoleLoopQuestProgress( selfEntity, playerRole ):
		# 		self.spaceStage_forceCompleteStage( selfEntity )
		questID = playerRole.loopQuest["loopQuestList"][0]
		if questID in self.questIDs:
			if playerRole.queryTaskStatus( questID, 2 ) in [csdefine.QUEST_NOT_ACCEPT,csdefine.QUEST_NOT_DONE]:
				KBEngine.globalData["RingTaskSpaceMgr"].setPreloadSpace( playerRole.base, str(playerRole.playerDBID) , str(questID), 0 )
				return
		if len(playerRole.loopQuest["loopQuestList"]) > 1:
			questID = playerRole.loopQuest["loopQuestList"][1]
			KBEngine.globalData["RingTaskSpaceMgr"].setPreloadSpace( playerRole.base, str(playerRole.playerDBID) , str(questID), 0 )

	def getCompleteStageIndexByRoleLoopQuestProgress( self, selfEntity, roleCell ):
		"""
		获得玩家已完成的阶段目标
		"""
		loopQuestProgress = 0
		if roleCell.loopQuestProgress < 6:
			loopQuestProgress = roleCell.loopQuestProgress
		if roleCell.loopQuestProgress > 6 and roleCell.loopQuestProgress < 12:
			loopQuestProgress = roleCell.loopQuestProgress - 6
		if roleCell.loopQuestProgress > 12:
			loopQuestProgress = roleCell.loopQuestProgress - 12
		return list(range(0,loopQuestProgress))

	def spaceStage_onSpaceInit( self, selfEntity ):
		"""
		"""
		pass

	def spaceStage_onPlayerEnter( self, selfEntity, roleCell ):
		"""
		玩家进副本
		"""
		pass

	def setCurrentStage( self, selfEntity, playerRole, stageIndex, taskIndex ):
		"""
		设置当前阶段
		"""
		stageIndex = selfEntity.createArgs.get("stageIndex",1)
		completeStageIndexs = list(range(1, stageIndex))
		for completeStageIndex in completeStageIndexs:
			selfEntity.completeSpaceStages.append(completeStageIndex)
		self.setSpaceStage( selfEntity, stageIndex )
		if selfEntity.spaceStage:
			completeTaskIndexs = list(range(1,taskIndex))
			for completeTaskIndex in completeTaskIndexs:
				self.spaceStage_forceCompleteStageTask( selfEntity,completeTaskIndex )

	def onEnterSpaceStageArea( self, selfEntity, stageIndex, taskIndex ):
		"""
		玩家进入阶段目标区域
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		if selfEntity.spaceStage.stageIndex != stageIndex:
			return
		stage = selfEntity.spaceStage.getTaskByTaskIndex( taskIndex )
		if not stage:
			return
		if stage.isCompleted():
			return
		SpaceCopy.onEnterSpaceStageArea( self, selfEntity, stageIndex, taskIndex )

	def onSpaceSpawnPointLoadOver( self, selfEntity ):
		"""刷新点加载完成回调"""
		SpaceCopy.onSpaceSpawnPointLoadOver(self, selfEntity)
		stageIndex = selfEntity.createArgs.get("stageIndex",1)
		completeStageIndexs = list(range(1, stageIndex))
		for completeStageIndex in completeStageIndexs:
			self.spaceEvent_onStageComplete( selfEntity, completeStageIndex )

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packArgs = SpaceCopy.getPackDomainData( self, playerEntity, args )
		tempDict = {}
		progress = playerEntity.loopQuestProgress
		if playerEntity.loopQuestProgress >= 6 and playerEntity.loopQuestProgress < 12:
			progress = playerEntity.loopQuestProgress - 6
		if playerEntity.loopQuestProgress >= 12:
			progress = playerEntity.loopQuestProgress - 12
		tempDict["stageIndex"] = progress + 1
		questID = playerEntity.loopQuest["loopQuestList"][0]
		quest = playerEntity.questTable.get( questID,None )
		tempDict["taskIndex"] = 1
		if not quest: # 如果玩家身上没有这个任务 阶段目标为1
			packArgs.update( tempDict )
			return packArgs
		taskIndex = 2 # 如果玩家身上有这个任务 阶段目标默认为2
		task1 = quest.getTask(1) # 取任务的第一任务目标 如果完成 阶段就为 3
		task2 = quest.getTask(2) # 取任务的第二任务目标 如果完成 阶段就为 3
		if task1 and task1.isDone():
			taskIndex = 3
		if task2 and task2.isDone():
			taskIndex = 3
			
		tempDict["taskIndex"] = taskIndex
		packArgs.update( tempDict )
		return packArgs

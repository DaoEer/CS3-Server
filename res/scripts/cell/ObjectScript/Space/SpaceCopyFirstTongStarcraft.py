# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Define
import Functions
import csdefine
import time
import KBEngine

class SpaceCopyFirstTongStarcraft( SpaceCopy ):
	"""
	帮会争霸 第一场
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.stageListStr = []
		self.bossID = ""
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.stageListStr = configData["SpaceData"].get("stageListStr","").split("|") #["1 2 3","4 5 6"]
		self.bossID = configData["SpaceData"].get("bossID","")
		
	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )

	def activeStart( self, selfEntity ):
		"""
		活动开始
		"""
		selfEntity.startTime = time.time()
		self.startSpaceLife( selfEntity )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		selfEntity.warInfos.addMember( packArgs["tongDBID"], packArgs["tongName"],packArgs["playerDBID"],playerRole, 0,packArgs["groupID"], packArgs["stageIndex"]  )
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		
	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )

	def onMonsterDie( self, selfEntity, monsterID, monsterScriptID ):
		"""
		怪物死亡
		"""
		SpaceCopy.onMonsterDie( self, selfEntity, monsterID, monsterScriptID )
		if monsterScriptID == self.bossID:
			passTime = int(time.time() - selfEntity.startTime)
			KBEngine.globalData["TongStarcraftManager"].starcraft_onPassFirstStarcraft( selfEntity.camp,selfEntity.tongDBID, passTime)

	def hasSpaceStage( self, selfEntity ):
		pass

	def getIndexByStageIndex( self, stageIndex ):
		"""
		"""
		for stageListStr in self.stageListStr:
			if stageIndex in [int(i) for i in stageListStr.split(" ")]:
				return self.stageListStr.index(stageListStr)
		return -1

	def setSpaceStage( self, selfEntity, stageIndex ):
		"""
		设置副本当前阶段
		"""
		stage = self.getStageByIndex( stageIndex )
		if not stage:
			return
		if stageIndex in selfEntity.completeSpaceStages:#如果在已完成列表中就不用重新设置，否则会导致界面出现2个相同的阶段
			return
		for spaceStage in selfEntity.spaceStageList:
			if spaceStage.stageIndex == stage.stageIndex:
				return

		selfEntity.spaceStageList.append(stage)
		self.onCurrentStageStart( selfEntity, stage )

	def onCurrentStageStart( self, selfEntity, stage ):
		"""
		当前阶段开始
		"""
		index = self.getIndexByStageIndex( stage.stageIndex )
		memberList = selfEntity.warInfos.getMembersByStageIndex(selfEntity.tongDBID,index)
		for member in memberList:
			member.mailbox.client.CLIENT_showSpaceStageWin( self.stageFileName,self.getCompleteSpaceStageNameByIndex( selfEntity, index ), stage.packToString() )
			self.sendCurrentSpaceStageTaskArea( selfEntity, member.mailbox, stage )
		#必须放在后面执行，因为updateSpaceStage可能导致阶段完成
		changedTasks = stage.updateGetItemTask( selfEntity )	#获取物品类目标在开始的时候要刷一下已完成数量
		self.updateCurrentSpaceStage( selfEntity, stage, changedTasks )

	def onStageStart( self, selfEntity ):
		"""
		阶段开始
		"""
		pass

	def updateCurrentSpaceStage( self, selfEntity, stage, changedTasks ):
		"""
		阶段目标计数更新
		"""
		if len( changedTasks ) == 0:
			return
		
		tempList = []
		for taskIndex, val in changedTasks:
			tempList.append( { "taskIndex":taskIndex, "val":val } )
		tempString = Functions.toJsonString( tempList )

		index = self.getIndexByStageIndex( stage.stageIndex )
		memberList = selfEntity.warInfos.getMembersByStageIndex(selfEntity.tongDBID,index)
		for member in memberList:
			member.mailbox.client.CLIENT_updateSpaceStageWin( stage.stageIndex, tempString )

		if stage.isCompleted():
			self.onCurrentStageComplete( selfEntity, stage )

	def updateSpaceStage( self, selfEntity, changedTasks ):
		"""
		阶段目标计数更新
		"""
		pass

	def onCurrentStageComplete( self, selfEntity, stage ):
		"""
		阶段完成
		"""
		selfEntity.completeSpaceStages.append( stage.stageIndex )
		index = self.getIndexByStageIndex( stage.stageIndex )
		memberList = selfEntity.warInfos.getMembersByStageIndex(selfEntity.tongDBID,index)
		for member in memberList:
			member.mailbox.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_SPACE_STAGE_COMPLETE )
			member.mailbox.client.CLIENT_updateCompleteSpaceStage( self.getCompleteSpaceStageNameByIndex( selfEntity,index ) )
			member.mailbox.client.CLENT_ClearSpaceStageTaskArea()

		self.spaceEvent_onStageComplete( selfEntity, stage.stageIndex )
		self.removeCurrentSpaceStage( selfEntity, stage.stageIndex )
		nextStageIndex = self.getNextStageIndexByIndex( selfEntity, stage.stageIndex, index )
		if nextStageIndex:
			if self.beginOnInit:
				self.setSpaceStage( selfEntity, nextStageIndex )

	def getNextStageIndexByIndex( self, selfEntity, stageIndex, index ):
		"""
		"""
		stageIndexList = [int(i) for i in self.stageListStr[index].split(" ")]
		index = stageIndexList.index(stageIndex)
		if index + 1 < len(stageIndexList):
			return stageIndexList[index + 1]
		return None

	def removeCurrentSpaceStage( self, selfEntity, stageIndex ):
		"""
		"""
		for spaceStage in selfEntity.spaceStageList:
			if spaceStage.stageIndex == stageIndex:
				selfEntity.spaceStageList.remove(spaceStage)
				break

	def onStageComplete( self, selfEntity ):
		"""
		阶段完成
		"""
		pass

	def getCompleteSpaceStageNameByIndex( self, selfEntity,index ):
		"""
		获取某一index已完成的阶段的标题 
		"""
		tempList = []
		for stageIndex in selfEntity.completeSpaceStages:
			for stage in self.spaceStages:
				srcindex = self.getIndexByStageIndex( stage.stageIndex )
				if stage.stageIndex == stageIndex and srcindex == index:
					tempList.append( stage.title )
					break
		return tempList

	def getCompleteSpaceStageName( self, selfEntity ):
		"""
		获取已完成的阶段的标题
		"""
		pass

	def spaceStage_onSpaceInit( self, selfEntity ):
		"""
		"""
		selfEntity.spaceStageList = []
		if self.beginOnInit:
			for stageListStr in self.stageListStr:
				stageList =[int(i) for i in stageListStr.split(" ")]
				self.setSpaceStage( selfEntity,stageList[0] )

	def spaceStage_onPlayerEnter( self, selfEntity, roleCell ):
		"""
		玩家进副本
		"""
		useStageIndex = selfEntity.warInfos.getRoleUseSpaceStage(selfEntity.tongDBID, roleCell.playerDBID )
		currentStage = None
		for stage in selfEntity.spaceStageList:
			if self.getIndexByStageIndex( stage.stageIndex ) == useStageIndex:
				currentStage = stage
				break
		if currentStage:
			roleCell.client.CLIENT_showSpaceStageWin( self.stageFileName, self.getCompleteSpaceStageNameByIndex( selfEntity,useStageIndex), currentStage.packToString() )
			self.sendCurrentSpaceStageTaskArea( selfEntity, roleCell,currentStage )

			changedTasks = currentStage.updateGetItemTask( selfEntity )	#获取物品类目标在玩家进入副本的时候要刷一下已完成数量
			self.updateCurrentSpaceStage( selfEntity, currentStage, changedTasks )
		else:
			if len(selfEntity.completeSpaceStages) != 0:
				roleCell.client.CLIENT_showSpaceStageWin( self.stageFileName, self.getCompleteSpaceStageNameByIndex( selfEntity,index ), "" )

	def spaceStage_onPlayerLeave( self, selfEntity, roleCell ):
		"""
		玩家出副本
		"""
		roleCell.client.CLIENT_hideSpaceStageWin()		#没有stage也要隐藏一下，因为stage完成后界面还在
		useStageIndex = selfEntity.warInfos.getRoleUseSpaceStage(selfEntity.tongDBID, roleCell.playerDBID )
		currentStage = None
		for stage in selfEntity.spaceStageList:
			if self.getIndexByStageIndex( stage.stageIndex ) == useStageIndex:
				currentStage = stage
				break
		if currentStage:
			roleCell.client.CLIENT_ClearSpaceStageTaskArea()
			changedTasks = currentStage.updateGetItemTask( selfEntity )	#获取物品类目标在玩家离开副本的时候要刷一下已完成数量
			self.updateCurrentSpaceStage( selfEntity, currentStage, changedTasks )

	#-------------------------------
	# 阶段目标区域相关
	#-------------------------------
	def sendCurrentSpaceStageTaskArea( self, selfEntity, roleCell, currentStage ):
		"""
		阶段目标区域发送到客户端，用于触发“进入某范围”阶段目标
		"""
		tempList = []
		for task in currentStage.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_ENTER_AREA:
				tempDict = { "taskIndex": task.taskIndex, "shapeType": task.param1, "areaZRange": task.param2, "areaParam": task.param3 }
				tempList.append( tempDict )
		
		if len(tempList) == 0:
			return
		roleCell.client.CLIENT_AddSpaceStageTaskArea( self.scriptID, currentStage.stageIndex, Functions.toJsonString( tempList ) )


	def sendSpaceStageTaskArea( self, selfEntity, roleCell ):
		"""
		阶段目标区域发送到客户端，用于触发“进入某范围”阶段目标
		"""
		pass

	def onEnterSpaceStageArea( self, selfEntity, stageIndex, taskIndex ):
		"""
		玩家进入阶段目标区域
		"""
		for spaceStage in selfEntity.spaceStageList:
			if spaceStage.stageIndex == stageIndex:
				changedTasks = spaceStage.onEnterTaskArea( taskIndex )
				self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	#------------------------------------
	# 各种阶段目标触发接口
	#------------------------------------
	def spaceStage_onMonsterDie( self, selfEntity, monsterScriptID ):
		"""
		怪物死亡
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.onMonsterDie( monsterScriptID )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onTriggerBox( self, selfEntity, scriptID ):
		"""
		箱子被触发
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.onTriggerBox( scriptID )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onNPCObjectDestroy( self, selfEntity, enityID, entityScriptID ):
		"""
		NPCObject销毁
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.onNPCObjectDestroy( entityScriptID )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		副本某条件发生改变
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.onConditionChange( senderType, senderID, conditionKey, extraValue )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onPlayerGetItem( self, selfEntity, itemID, amount ):
		"""
		玩家获得物品
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.onPlayerGetItem( itemID, amount )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onPlayerRemoveItem( self, selfEntity, itemID, amount ):
		"""
		玩家移除物品
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.onPlayerRemoveItem( selfEntity, itemID, amount )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_forceCompleteStageTask( self, selfEntity, taskIndex ):
		"""
		强制完成当前阶段目标
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.forceCompleteStageTask( taskIndex )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_forceSetCurrentStageTaskClear( self, selfEntity, taskIndex  ):
		"""
		强制设置当前阶段目标清0 具体在CST-2936有使用
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.forceSetCurrentStageTaskClear( taskIndex )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onPlayerUseItem( self, selfEntity, itemID, amount ):
		"""
		玩家使用物品
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.onPlayerUseItem( selfEntity, itemID, amount )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_gmCompleteStageTask( self, selfEntity, taskIndex, progress ):
		"""
		gm强制完成当前阶段目标
		"""
		for spaceStage in selfEntity.spaceStageList:
			changedTasks = spaceStage.gmCurrentStageTask( taskIndex, progress )
			if not changedTasks:
				return False
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )
			return True




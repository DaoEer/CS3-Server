# -*- coding: utf-8 -*-

# 副本阶段显示功能接口

import copy
import time
import Functions
from LoadModule import *
import KBEDebug
import Define
import csdefine
import csstatus
from ConfigObject.SpaceStage.SpaceStage import *
from ConfigObject.SpaceStage.SpaceStageTask import *

class SpaceStageInterface:
	"""
	"""
	def __init__( self ):
		self.stageFileName = ""
		self.beginOnInit = True	# 副本创建时开始阶段一，并且阶段完成时自动开启后续阶段
		self.spaceStages = []
	
	def initSpaceStages( self, fileName ):
		"""
		初始化阶段数据
		"""
		section = openJsonCfg( "GameObject/SpaceObject/SpaceStageFile/%s.json"%fileName )
		self.stageFileName = section.get( "name", "" )
		self.beginOnInit = section["beginOnSpaceInit"]
		for stageIndexStr, stageSec in section["stages"].items():
			instance = SpaceStage()
			instance.init( int(stageIndexStr), stageSec )
			self.spaceStages.append( instance )
		self.spaceStages.sort(key = lambda x:x.stageIndex)
	
	def hasSpaceStage( self, selfEntity ):
		return selfEntity.spaceStage and isinstance( selfEntity.spaceStage, SpaceStage )
	
	def getStageByIndex( self, index ):
		"""
		"""
		for stage in self.spaceStages:
			if stage.stageIndex == index:
				return stage
		return None

	def setSpaceStage( self, selfEntity, stageIndex ):
		"""
		设置副本当前阶段
		"""
		stage = self.getStageByIndex( stageIndex )
		if not stage:
			return
		if stageIndex in selfEntity.completeSpaceStages:#如果在已完成列表中就不用重新设置，否则会导致界面出现2个相同的阶段
			return
		if selfEntity.spaceStage and selfEntity.spaceStage.stageIndex == stage.stageIndex:
			return
		selfEntity.spaceStage = copy.deepcopy( stage )
		self.onStageStart( selfEntity )

	def updateSpaceStage( self, selfEntity, changedTasks ):
		"""
		阶段目标计数更新
		"""
		if len( changedTasks ) == 0:
			return
		
		tempList = []
		for taskIndex, val in changedTasks:
			tempList.append( { "taskIndex":taskIndex, "val":val } )
		tempString = Functions.toJsonString( tempList )
		for roleCell in selfEntity._spaceRoles:
			roleCell.client.CLIENT_updateSpaceStageWin( selfEntity.spaceStage.stageIndex, tempString )
		
		if selfEntity.spaceStage.isCompleted():
			self.onStageComplete( selfEntity )
		else:
			for taskIndex, val in changedTasks:
				task = selfEntity.spaceStage.getTaskByTaskIndex( taskIndex )
				if not task:
					continue
				if task.isCompleted():
					self.onSpaceStageTaskCompleted( selfEntity, task )

	def onStageStart( self, selfEntity ):
		"""
		阶段开始
		"""
		selfEntity.stageStartTime = time.time()
		for roleCell in selfEntity._spaceRoles:
			roleCell.client.CLIENT_showSpaceStageWin( self.stageFileName, self.getCompleteSpaceStageName( selfEntity ), selfEntity.spaceStage.packToString() )
			self.sendSpaceStageTaskArea( selfEntity, roleCell )
		self.spaceEvent_onStageStart( selfEntity, selfEntity.spaceStage.stageIndex )
		
		#必须放在后面执行，因为updateSpaceStage可能导致阶段完成
		changedTasks = selfEntity.spaceStage.updateGetItemTask( selfEntity )	#获取物品类目标在开始的时候要刷一下已完成数量
		self.updateSpaceStage( selfEntity, changedTasks )

	def onStageComplete( self, selfEntity ):
		"""
		阶段完成
		"""
		selfEntity.completeSpaceStages.append( selfEntity.spaceStage.stageIndex )
		for roleCell in selfEntity._spaceRoles:
			roleCell.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_SPACE_STAGE_COMPLETE )
			roleCell.client.CLIENT_updateCompleteSpaceStage( self.getCompleteSpaceStageName( selfEntity ) )
			roleCell.client.CLIENT_ClearSpaceStageTaskArea()
		
		oldStageIndex = selfEntity.spaceStage.stageIndex
		selfEntity.spaceStage = None
		selfEntity.stageStartTime = 0.0
		self.spaceEvent_onStageComplete( selfEntity, oldStageIndex )
		
		if oldStageIndex < len(self.spaceStages):	#还有后续阶段
			if self.beginOnInit:
				self.setSpaceStage( selfEntity, oldStageIndex+1 )

	def getCompleteSpaceStageName( self, selfEntity ):
		"""
		获取已完成的阶段的标题
		"""
		tempList = []
		for stageIndex in selfEntity.completeSpaceStages:
			for stage in self.spaceStages:
				if stage.stageIndex == stageIndex:
					tempList.append( stage.title )
					break
		return tempList

	def onSpaceStageTaskCompleted( self, selfEntity, task ):
		"""
		当前阶段的某个目标完成
		"""
		self.spaceEvent_onStageTaskComplete( selfEntity, selfEntity.spaceStage.stageIndex, task.taskIndex )
		self.sendNextSpaceStageTaskToClient( selfEntity, task )

	def sendNextSpaceStageTaskToClient( self, selfEntity, task ):
		"""
		发送下个阶段目标到客户端
		"""
		if selfEntity.spaceStage == None:
			return
		currentPriority = selfEntity.spaceStage.getCurrentPriority()
		if currentPriority > task.priority:
			nextPriority = task.priority + 1
			tempList = selfEntity.spaceStage.packNextTasksToString( nextPriority )
			for role in selfEntity._spaceRoles:
				role.client.CLIENT_showSpaceStageNextTask( selfEntity.spaceStage.stageIndex,Functions.toJsonString(tempList) )
				self.sendSpaceStageTaskArea(selfEntity,role)
			for task in selfEntity.spaceStage.tasks:
				if task.priority == nextPriority and task.isCompleted():
					self.onSpaceStageTaskCompleted( selfEntity, task )

	def spaceStage_onSpaceInit( self, selfEntity ):
		"""
		"""
		selfEntity.spaceStage = None	# 初始值需要为None，而因为是define属性，此值会是一个SpaceStageDataType对象，不为None，因此手动赋一下值。
		if len( self.spaceStages ) and self.beginOnInit:
			self.setSpaceStage( selfEntity, self.spaceStages[0].stageIndex )

	def spaceStage_onPlayerEnter( self, selfEntity, roleCell ):
		"""
		玩家进副本
		"""
		if self.hasSpaceStage( selfEntity ):
			roleCell.client.CLIENT_showSpaceStageWin( self.stageFileName, self.getCompleteSpaceStageName( selfEntity ), selfEntity.spaceStage.packToString() )
			self.sendSpaceStageTaskArea( selfEntity, roleCell )
			
			changedTasks = selfEntity.spaceStage.updateGetItemTask( selfEntity )	#获取物品类目标在玩家进入副本的时候要刷一下已完成数量
			self.updateSpaceStage( selfEntity, changedTasks )
		else:
			if len(selfEntity.completeSpaceStages) != 0:
				roleCell.client.CLIENT_showSpaceStageWin( self.stageFileName, self.getCompleteSpaceStageName( selfEntity ), "" )
	
	def spaceStage_onPlayerLeave( self, selfEntity, roleCell ):
		"""
		玩家出副本
		"""
		if roleCell.getClient():
			roleCell.client.CLIENT_hideSpaceStageWin()		#没有stage也要隐藏一下，因为stage完成后界面还在
		if not self.hasSpaceStage( selfEntity ):
			return
		if roleCell.getClient():
			roleCell.client.CLIENT_ClearSpaceStageTaskArea()
		changedTasks = selfEntity.spaceStage.updateGetItemTask( selfEntity )	#获取物品类目标在玩家离开副本的时候要刷一下已完成数量
		self.updateSpaceStage( selfEntity, changedTasks )
	
	#-------------------------------
	# 阶段目标区域相关
	#-------------------------------
	def sendSpaceStageTaskArea( self, selfEntity, roleCell ):
		"""
		阶段目标区域发送到客户端，用于触发“进入某范围”阶段目标
		"""

		priority = selfEntity.spaceStage.getCurrentPriority()
		tempList = []
		for task in selfEntity.spaceStage.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_ENTER_AREA and task.priority == priority:
				tempDict = { "taskIndex": task.taskIndex, "shapeType": task.param1, "areaZRange": task.param2, "areaParam": task.param3 }
				tempList.append( tempDict )
		if len(tempList) == 0:
			return
		roleCell.client.CLIENT_AddSpaceStageTaskArea( self.scriptID, selfEntity.spaceStage.stageIndex, Functions.toJsonString( tempList ) )
	
	def onEnterSpaceStageArea( self, selfEntity, stageIndex, taskIndex ):
		"""
		玩家进入阶段目标区域
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		if selfEntity.spaceStage.stageIndex != stageIndex:
			return
		
		changedTasks = selfEntity.spaceStage.onEnterTaskArea( taskIndex )
		self.updateSpaceStage( selfEntity, changedTasks )
	
	#------------------------------------
	# 各种阶段目标触发接口
	#------------------------------------
	def spaceStage_onMonsterDie( self, selfEntity, monsterScriptID ):
		"""
		怪物死亡
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onMonsterDie( monsterScriptID )
		self.updateSpaceStage( selfEntity, changedTasks )
	
	def spaceStage_onTriggerBox( self, selfEntity, scriptID ):
		"""
		箱子被触发
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onTriggerBox( scriptID )
		self.updateSpaceStage( selfEntity, changedTasks )
	
	def spaceStage_onNPCObjectDestroy( self, selfEntity, enityID, entityScriptID ):
		"""
		NPCObject销毁
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onNPCObjectDestroy( entityScriptID )
		self.updateSpaceStage( selfEntity, changedTasks )
	
	def spaceStage_onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		副本某条件发生改变
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onConditionChange( senderType, senderID, conditionKey, extraValue )
		self.updateSpaceStage( selfEntity, changedTasks )
	
	def spaceStage_onPlayerGetItem( self, selfEntity, itemID, amount ):
		"""
		玩家获得物品
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onPlayerGetItem( itemID, amount )
		self.updateSpaceStage( selfEntity, changedTasks )
	
	def spaceStage_onPlayerRemoveItem( self, selfEntity, itemID, amount ):
		"""
		玩家移除物品
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onPlayerRemoveItem( selfEntity, itemID, amount )
		self.updateSpaceStage( selfEntity, changedTasks )

	def spaceStage_onPlayerUseTitle( self, selfEntity, titleID ):
		"""
		玩家装备称号
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onPlayerUseTitle( selfEntity, titleID )
		self.updateSpaceStage( selfEntity, changedTasks )

	def spaceStage_forceCompleteStageTask( self, selfEntity, taskIndex ):
		"""
		强制完成当前阶段目标
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.forceCompleteStageTask( taskIndex )
		self.updateSpaceStage( selfEntity, changedTasks )

	def spaceStage_forceSetCurrentStageTaskClear( self, selfEntity, taskIndex  ):
		"""
		强制设置当前阶段目标清0 具体在CST-2936有使用
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.forceSetCurrentStageTaskClear( taskIndex )
		self.updateSpaceStage( selfEntity, changedTasks )

	def spaceStage_onPlayerUseItem( self, selfEntity, itemID, amount ):
		"""
		玩家使用物品
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onPlayerUseItem( selfEntity, itemID, amount )
		self.updateSpaceStage( selfEntity, changedTasks )

	def spaceStage_gmCompleteStageTask( self, selfEntity, taskIndex, progress ):
		"""
		gm强制完成当前阶段目标
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.gmCurrentStageTask( taskIndex, progress )
		if not changedTasks:
			return False
		self.updateSpaceStage( selfEntity, changedTasks )
		return True
		
	def spaceStage_forceCompleteStage( self, selfEntity ):
		"""
		强制完成某个阶段
		"""
		for task in selfEntity.spaceStage.tasks:
			self.spaceStage_forceCompleteStageTask( selfEntity, task.taskIndex )
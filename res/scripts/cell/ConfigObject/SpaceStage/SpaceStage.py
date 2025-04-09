# -*- coding: utf-8 -*-

# 副本阶段数据类


import Functions
import Define
import SmartImport
from KBEDebug import *
from SpaceStageDataType import SpaceStageDataType
import SpaceStageTaskDataType

class SpaceStage( SpaceStageDataType ):
	def __init__( self ):
		self.stageIndex = ""
		self.title = ""
		self.comment = ""
		self.tasks = []

	def init( self, stageIndex, dict ):
		self.stageIndex = stageIndex
		self.title = dict["title"]
		self.comment = dict["comment"]
		for taskIndexStr, taskSection in dict["tasks"].items():
			taskClass = SmartImport.smartImport( "ConfigObject.SpaceStage.SpaceStageTask:" + taskSection["type"] )
			instance = taskClass()
			instance.init( int(taskIndexStr), taskSection )
			self.tasks.append( instance )
		self.tasks.sort(key = lambda x:x.priority)

	def getCurrentPriority( self ):
		"""
		获得当前优先级
		"""
		for task in self.tasks:
			if task.isCompleted():
				continue
			return task.priority
		return 0

	def packToString( self ):
		"""
		"""
		_dict = {}
		_dict["stageIndex"] = self.stageIndex
		_dict["title"] = self.title
		_dict["comment"] = self.comment
		tempList = []
		priority = self.getCurrentPriority()
		for task in self.tasks:
			if priority >= task.priority:
				tempDict = SpaceStageTaskDataType.instance.getDictFromObj( task )
				tempList.append(tempDict)
		_dict["tasks"] = tempList
		return Functions.toJsonString( [ _dict ] )

	def packNextTasksToString( self, priority ):
		"""
		打包当前阶段目标数据
		"""
		tempList = []
		for task in self.tasks:
			if task.priority == priority:
				tempDict = SpaceStageTaskDataType.instance.getDictFromObj( task )
				tempList.append(tempDict)
		return tempList

	def isCompleted( self ):
		"""
		阶段是否已完成
		"""
		for task in self.tasks:
			if not task.isCompleted():
				return False
		return True

	def getTaskByTaskIndex( self, taskIndex ):
		"""
		"""
		for task in self.tasks:
			if task.taskIndex == taskIndex:
				return task
		return None

	def onMonsterDie( self, scriptID ):
		"""
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_KILL_MONSTER:
				if task.checkMonsterScriptID( scriptID ):
					if task.increaseVal( 1 ) and task.priority == priority:
						resultList.append( (task.taskIndex, task.val) )
		return resultList

	def onTriggerBox( self, scriptID ):
		"""
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_TRIGGER_BOX:
				if task.checkBoxScriptID( scriptID ):
					if task.increaseVal( 1 ) and task.priority == priority:
						resultList.append( (task.taskIndex, task.val) )
		return resultList

	def onNPCObjectDestroy( self, scriptID ):
		"""
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_ENTITY_DESTROY:
				if task.checkEntityScriptID( scriptID ):
					if task.increaseVal( 1 ) and task.priority == priority:
						resultList.append( (task.taskIndex, task.val) )
		return resultList

	def onConditionChange( self, senderType, senderID, conditionKey, extraValue ):
		"""
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_CONDITION_CHANGE:
				if task.checkCondition( senderType, senderID, conditionKey, extraValue ):
					if task.increaseVal( 1 ) and task.priority == priority:
						resultList.append( (task.taskIndex, task.val) )
		return resultList

	def onPlayerGetItem( self, itemID, amount ):
		"""
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_GET_ITEM:
				if task.checkItemID( itemID ):
					if task.increaseVal( amount ) and task.priority == priority:
						resultList.append( (task.taskIndex, task.val) )
		return resultList

	def onPlayerRemoveItem( self, spaceEntity, itemID, amount ):
		"""
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_GET_ITEM:
				if task.checkItemID( itemID ):
					hasAmount = self.getSpacePlayerItemAmount( spaceEntity, itemID )
					if task.setVal( hasAmount ) and task.priority == priority:
						resultList.append( (task.taskIndex, task.val) )
		return resultList

	def onPlayerUseItem( self, spaceEntity, itemID, amount ):
		"""
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_USE_ITEM:
				if task.checkItemID( itemID ):
					if task.increaseVal( amount ) and task.priority == priority:
						resultList.append( (task.taskIndex, task.val) )
		return resultList

	def onEnterTaskArea( self, taskIndex ):
		"""
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.taskIndex == taskIndex and task.getType() == Define.SPACE_STAGE_TASK_ENTER_AREA:
				if task.increaseVal( 1 ) and task.priority == priority:
					resultList.append( (task.taskIndex, task.val) )
				break
		return resultList

	def onPlayerUseTitle( self, spaceEntity, titleID ):
		"""
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_USE_TITLE:
				if task.checkTitleID( titleID ):
					if task.increaseVal( 1 ) and task.priority == priority:
						resultList.append( (task.taskIndex, task.val) )
		return resultList

	def forceCompleteStageTask( self, taskIndex ):
		"""
		强制完成阶段目标
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.taskIndex == taskIndex:
				if task.setVal(task.reqVal) and task.priority == priority:
					resultList.append( (task.taskIndex,task.val) )
		return resultList

	def forceSetCurrentStageTaskClear( self, taskIndex ):
		"""
		强制设置阶段目标清0
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.taskIndex == taskIndex:
				if task.setVal(0) and task.priority == priority:
					resultList.append( (task.taskIndex,task.val) )
		return resultList

	def gmCurrentStageTask( self, taskIndex, progress ):
		"""
		GM强制设置阶段目标完成次数
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.taskIndex == taskIndex:
				if task.gmSetVal( progress ) and task.priority == priority:
					resultList.append( (task.taskIndex,task.val) )
		return resultList

	#------------------------------获取物品类目标特殊处理---------------------------------
	def getSpacePlayerItemAmount( self, spaceEntity, itemID ):
		"""
		获取所有玩家某物品总数
		"""
		hasAmount = 0
		itemList = []
		
		for e in spaceEntity._spaceRoles:
			itemList.extend( e.getItemInstsByID( itemID ))
			
		for itemInst in itemList:
			hasAmount += itemInst.amount
		
		return hasAmount
	
	def updateGetItemTask( self, spaceEntity ):
		"""
		刷新一下获取物品类目标的已完成数量
		注：重新计算所有玩家的物品数
		"""
		priority = self.getCurrentPriority()
		resultList = []
		for task in self.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_GET_ITEM:
				itemID = task.getReqItemID()
				hasAmount = self.getSpacePlayerItemAmount( spaceEntity, itemID )
				if task.setVal( hasAmount ) and task.priority == priority:
					resultList.append( (task.taskIndex, task.val) )
		return resultList

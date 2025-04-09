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

class SpaceStageExtInterface:
	"""
	副本阶段扩展（实现 PVP副本中攻防、守方的副本阶段不同，但每个阶段都是对应的）
	主要重写SpaceStageInterface方法，不继承SpaceStateInterface 是避免多重继承
	"""
	def __init__( self ):
		# 掠夺战阶段目标
		self.stageFileName = ""			# 守方副本阶段
		self.attackFileName = ""		# 攻防副本阶段
		self.beginOnInit = True			# 副本创建时开始阶段一，并且阶段完成时自动开启后续阶段
		self.spaceStages = []
		self.attackSpaceStages = []
		# 争夺战阶段目标
		self.cstageFileName = ""			# 守方副本阶段
		self.cattackFileName = ""		# 攻防副本阶段
		self.cbeginOnInit = True			# 副本创建时开始阶段一，并且阶段完成时自动开启后续阶段
		self.cspaceStages = []
		self.cattackSpaceStages = []
	
	def initAckAndPctSpaceStages( self, fileName, attackFileName ):
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
		
		section = openJsonCfg( "GameObject/SpaceObject/SpaceStageFile/%s.json"%attackFileName )
		self.attackFileName = section.get( "name", "" )
		for stageIndexStr, stageSec in section["stages"].items():
			instance = SpaceStage()
			instance.init( int(stageIndexStr), stageSec )
			self.attackSpaceStages.append( instance )
		self.attackSpaceStages.sort(key = lambda x:x.stageIndex)
		
	def initAckAndPctCSpaceStages( self, fileName, attackFileName ):
		"""
		初始化阶段数据
		"""
		section = openJsonCfg( "GameObject/SpaceObject/SpaceStageFile/%s.json"%fileName )
		self.cstageFileName = section.get( "name", "" )
		self.cbeginOnInit = section["beginOnSpaceInit"]
		for stageIndexStr, stageSec in section["stages"].items():
			instance = SpaceStage()
			instance.init( int(stageIndexStr), stageSec )
			self.cspaceStages.append( instance )
		self.cspaceStages.sort(key = lambda x:x.stageIndex)
		
		section = openJsonCfg( "GameObject/SpaceObject/SpaceStageFile/%s.json"%attackFileName )
		self.cattackFileName = section.get( "name", "" )
		for stageIndexStr, stageSec in section["stages"].items():
			instance = SpaceStage()
			instance.init( int(stageIndexStr), stageSec )
			self.cattackSpaceStages.append( instance )
		self.cattackSpaceStages.sort(key = lambda x:x.stageIndex)
	
	def hasSpaceStage( self, selfEntity ):
		return selfEntity.spaceStage and isinstance( selfEntity.spaceStage, SpaceStage )
	
	def getStageByIndex( self, index ):
		"""
		"""
		for stage in self.spaceStages:
			if stage.stageIndex == index:
				return stage
		return None
		
	def getAttackStageByIndex( self, index ):
		"""
		"""
		for stage in self.attackSpaceStages:
			if stage.stageIndex == index:
				return stage
		return None

	def setSpaceStage( self, selfEntity, stageIndex ):
		"""
		设置副本当前阶段
		"""
		stage = self.getStageByIndex( stageIndex )
		attackStage = self.getAttackStageByIndex( stageIndex )
		if not stage or not attackStage:
			return
		if stageIndex in selfEntity.completeSpaceStages:#如果在已完成列表中就不用重新设置，否则会导致界面出现2个相同的阶段
			return
		if selfEntity.spaceStage and selfEntity.spaceStage.stageIndex == stage.stageIndex:
			return
		if selfEntity.attackSpaceStages and selfEntity.attackSpaceStages.stageIndex == attackStage.stageIndex:
			return
		selfEntity.spaceStage = copy.deepcopy( stage )
		selfEntity.attackSpaceStages = copy.deepcopy(attackStage)
		self.onStageStart( selfEntity )

	def updateSpaceStage( self, selfEntity, changedTasks, belongSide = csdefine.BELONG_SIDE_PROTECT ):
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
			if roleCell.isBelongSide( belongSide ):
				roleCell.client.CLIENT_updateSpaceStageWin( selfEntity.spaceStage.stageIndex, tempString )
		if belongSide == csdefine.BELONG_SIDE_PROTECT:
			stage = selfEntity.spaceStage
		else:
			stage = selfEntity.attackSpaceStages
		if stage.isCompleted() and belongSide == csdefine.BELONG_SIDE_ATTACK:
			self.onStageComplete( selfEntity )
		else:
			for taskIndex, val in changedTasks:
				task = stage.getTaskByTaskIndex( taskIndex )
				if not task:
					continue
				if task.isCompleted():
					self.onSpaceStageTaskCompleted( selfEntity, belongSide, task )

	def onStageStart( self, selfEntity ):
		"""
		阶段开始
		"""
		selfEntity.stageStartTime = time.time()
		for roleCell in selfEntity._spaceRoles:
			if roleCell.isBelongSide( csdefine.BELONG_SIDE_PROTECT ):
				stageFileName = self.stageFileName
				packStr = selfEntity.spaceStage.packToString()
			else:
				stageFileName = self.attackFileName
				packStr = selfEntity.attackSpaceStages.packToString()
			roleCell.client.CLIENT_showSpaceStageWin( stageFileName, self.getCompleteSpaceStageName( selfEntity, roleCell.belongSide ), packStr )
				
			self.sendSpaceStageTaskArea( selfEntity, roleCell )
		self.spaceEvent_onStageStart( selfEntity, selfEntity.spaceStage.stageIndex )
		
		#必须放在后面执行，因为updateSpaceStage可能导致阶段完成
		changedTasks = selfEntity.spaceStage.updateGetItemTask( selfEntity )	#获取物品类目标在开始的时候要刷一下已完成数量
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		
		changedTasks = selfEntity.attackSpaceStages.updateGetItemTask( selfEntity )	#获取物品类目标在开始的时候要刷一下已完成数量
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )

	def onStageComplete( self, selfEntity ):
		"""
		阶段完成
		"""
		selfEntity.completeSpaceStages.append( selfEntity.spaceStage.stageIndex )
		for roleCell in selfEntity._spaceRoles:
			roleCell.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_SPACE_STAGE_COMPLETE )
			roleCell.client.CLIENT_updateCompleteSpaceStage( self.getCompleteSpaceStageName( selfEntity, roleCell.belongSide ) )
			roleCell.client.CLIENT_ClearSpaceStageTaskArea()
		
		oldStageIndex = selfEntity.spaceStage.stageIndex
		selfEntity.spaceStage = None
		selfEntity.attackSpaceStages = None
		selfEntity.stageStartTime = 0.0
		self.spaceEvent_onStageComplete( selfEntity, oldStageIndex )
		
		if oldStageIndex < len(self.spaceStages):	#还有后续阶段
			if self.beginOnInit:
				self.setSpaceStage( selfEntity, oldStageIndex+1 )

	def getCompleteSpaceStageName( self, selfEntity, belongSide = csdefine.BELONG_SIDE_PROTECT ):
		"""
		获取已完成的阶段的标题
		"""
		tempList = []
		if belongSide == csdefine.BELONG_SIDE_PROTECT:
			stages = self.spaceStages
		else:
			stages = self.attackSpaceStages
		for stageIndex in selfEntity.completeSpaceStages:
			for stage in stages:
				if stage.stageIndex == stageIndex:
					tempList.append( stage.title )
					break
		return tempList

	def onSpaceStageTaskCompleted( self, selfEntity, belongSide, task ):
		"""
		当前阶段的某个目标完成
		"""
		self.spaceEvent_onStageTaskComplete( selfEntity, selfEntity.spaceStage.stageIndex, task.taskIndex )
		self.sendNextSpaceStageTaskToClient( selfEntity, belongSide, task )

	def sendNextSpaceStageTaskToClient( self, selfEntity, belongSide, task ):
		"""
		发送下个阶段目标到客户端
		"""
		if belongSide == csdefine.BELONG_SIDE_PROTECT:
			stage = selfEntity.spaceStage
		else:
			stage = selfEntity.attackSpaceStages
		currentPriority = stage.getCurrentPriority()
		if currentPriority > task.priority:
			nextPriority = task.priority + 1
			tempList = stage.packNextTasksToString( nextPriority )
			for role in selfEntity._spaceRoles:
				if role.isBelongSide( belongSide ):
					role.client.CLIENT_showSpaceStageNextTask( stage.stageIndex,Functions.toJsonString(tempList) )
					self.sendSpaceStageTaskArea(selfEntity,role)
			for task in stage.tasks:
				if task.priority == nextPriority and task.isCompleted():
					self.onSpaceStageTaskCompleted( selfEntity, belongSide, task )

	def spaceStage_onSpaceInit( self, selfEntity ):
		"""
		"""
		pass
		
	def spaceStage_onPlayerEnter( self, selfEntity, roleCell ):
		"""
		玩家进副本
		"""
		if self.hasSpaceStage( selfEntity ):
			if roleCell.isBelongSide( csdefine.BELONG_SIDE_PROTECT ):
				stageFileName = self.stageFileName
				packStr = selfEntity.spaceStage.packToString()
			else:
				stageFileName = self.attackFileName
				packStr = selfEntity.attackSpaceStages.packToString()
			roleCell.client.CLIENT_showSpaceStageWin( stageFileName, self.getCompleteSpaceStageName( selfEntity, roleCell.belongSide ), packStr )
			self.sendSpaceStageTaskArea( selfEntity, roleCell )
			
			changedTasks = selfEntity.spaceStage.updateGetItemTask( selfEntity )	#获取物品类目标在玩家进入副本的时候要刷一下已完成数量
			self.updateSpaceStage( selfEntity, changedTasks, roleCell.belongSide )
		else:
			if len(selfEntity.completeSpaceStages) != 0:
				if roleCell.isBelongSide( csdefine.BELONG_SIDE_PROTECT ):
					stageFileName = self.stageFileName
				else:
					stageFileName = self.attackFileName
				roleCell.client.CLIENT_showSpaceStageWin( stageFileName, self.getCompleteSpaceStageName( selfEntity, roleCell.belongSide ), "" )
	
	def spaceStage_onPlayerLeave( self, selfEntity, roleCell ):
		"""
		玩家出副本
		"""
		pass
	
	#-------------------------------
	# 阶段目标区域相关
	#-------------------------------
	def sendSpaceStageTaskArea( self, selfEntity, roleCell ):
		"""
		阶段目标区域发送到客户端，用于触发“进入某范围”阶段目标
		"""
		priority = selfEntity.spaceStage.getCurrentPriority()
		tempList = []
		tasks = []
		if roleCell.isBelongSide( csdefine.BELONG_SIDE_PROTECT ):
			tasks = selfEntity.spaceStage.tasks
		elif roleCell.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
			tasks = selfEntity.attackSpaceStages.tasks
		for task in tasks:
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
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		
		changedTasks = selfEntity.attackSpaceStages.onEnterTaskArea( taskIndex )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )
	
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
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		changedTasks = selfEntity.attackSpaceStages.onMonsterDie( monsterScriptID )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )
	
	def spaceStage_onTriggerBox( self, selfEntity, scriptID ):
		"""
		箱子被触发
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onTriggerBox( scriptID )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		changedTasks = selfEntity.attackSpaceStages.onTriggerBox( scriptID )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )
	
	def spaceStage_onNPCObjectDestroy( self, selfEntity, enityID, entityScriptID ):
		"""
		NPCObject销毁
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onNPCObjectDestroy( entityScriptID )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		changedTasks = selfEntity.attackSpaceStages.onNPCObjectDestroy( entityScriptID )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )
	
	def spaceStage_onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		副本某条件发生改变
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onConditionChange( senderType, senderID, conditionKey, extraValue )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		changedTasks = selfEntity.attackSpaceStages.onConditionChange( senderType, senderID, conditionKey, extraValue )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )
	
	def spaceStage_onPlayerGetItem( self, selfEntity, itemID, amount ):
		"""
		玩家获得物品
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onPlayerGetItem( itemID, amount )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		changedTasks = selfEntity.attackSpaceStages.onPlayerGetItem( itemID, amount )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )
	
	def spaceStage_onPlayerRemoveItem( self, selfEntity, itemID, amount ):
		"""
		玩家移除物品
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onPlayerRemoveItem( selfEntity, itemID, amount )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		changedTasks = selfEntity.attackSpaceStages.onPlayerRemoveItem( selfEntity, itemID, amount )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )

	def spaceStage_onPlayerUseTitle( self, selfEntity, titleID ):
		"""
		玩家装备称号
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onPlayerUseTitle( selfEntity, titleID )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		changedTasks = selfEntity.attackSpaceStages.onPlayerUseTitle( selfEntity, titleID )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )

	def spaceStage_forceCompleteStageTask( self, selfEntity, taskIndex ):
		"""
		强制完成当前阶段目标
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.forceCompleteStageTask( taskIndex )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_PROTECT )
		changedTasks = selfEntity.attackSpaceStages.forceCompleteStageTask( taskIndex )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )

	def spaceStage_forceSetCurrentStageTaskClear( self, selfEntity, taskIndex  ):
		"""
		强制设置当前阶段目标清0 具体在CST-2936有使用
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.forceSetCurrentStageTaskClear( taskIndex )
		self.updateSpaceStage( selfEntity, changedTasks )
		changedTasks = selfEntity.attackSpaceStages.forceSetCurrentStageTaskClear( taskIndex )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )

	def spaceStage_onPlayerUseItem( self, selfEntity, itemID, amount ):
		"""
		玩家使用物品
		"""
		if not self.hasSpaceStage( selfEntity ):
			return
		changedTasks = selfEntity.spaceStage.onPlayerUseItem( selfEntity, itemID, amount )
		self.updateSpaceStage( selfEntity, changedTasks )
		changedTasks = selfEntity.attackSpaceStages.onPlayerUseItem( selfEntity, itemID, amount )
		self.updateSpaceStage( selfEntity, changedTasks, csdefine.BELONG_SIDE_ATTACK )

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
	
	def showPlayerDFActiveStage( self, player, stageIndex, isChallengeActive, belongSide, endTime ):
		"""显示玩家洞府活动阶段"""
		if stageIndex > 1:
			# 第二阶段已完成
			player.client.CLIENT_updateCompleteSpaceStage( ["0","1"] )
			return
		if isChallengeActive:
			if belongSide == csdefine.BELONG_SIDE_PROTECT:
				fileName = self.cstageFileName
				stage = self.cspaceStages[stageIndex]
			else:
				fileName = self.cattackFileName
				stage = self.cattackSpaceStages[stageIndex]
		else:
			if belongSide == csdefine.BELONG_SIDE_PROTECT:
				fileName = self.stageFileName
				stage = self.spaceStages[stageIndex]
			else:
				fileName = self.attackFileName
				stage = self.attackSpaceStages[stageIndex]
		if stageIndex == 1:
			player.client.CLIENT_updateCompleteSpaceStage( [] )
		player.client.ShowSpaceLife( str(endTime), 0,str( Functions.getTime() ) )
		player.client.CLIENT_showSpaceStageWin( fileName, [], stage.packToString() )
	
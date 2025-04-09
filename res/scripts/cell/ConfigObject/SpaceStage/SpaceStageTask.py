# -*- coding: utf-8 -*-

# 副本阶段任务数据类

import Define
from KBEDebug import *
import SpaceStageTaskDataType

class SpaceStageTaskBase( SpaceStageTaskDataType.SpaceStageTaskDataType ):
	"""
	基类
	"""
	def __init__( self ):
		SpaceStageTaskDataType.SpaceStageTaskDataType.__init__( self )

	def init( self, taskIndex, dict ):
		self.taskIndex = taskIndex
		self.title = dict["title"]
		self.reqVal = dict["reqVal"]
		self.val = dict.get( "val", 0 )
		self.param1 = dict["param1"]
		self.param2 = dict["param2"]
		self.param3 = dict["param3"]
		self.isShowByProgressbar = dict.get("isShowByProgressbar",0) #是否使用进度条显示
		self.priority = dict.get("priority",0) #阶段目标的显示优先级
		self.navigateData = dict["navigateData"]

	def getType( self ):
		return Define.SPACE_STAGE_TASK_NONE

	def increaseVal( self, value ):
		if value == 0:
			return False
		
		if self.val >= self.reqVal:
			return False
		
		self.val = min( self.reqVal, self.val + value )
		return True

	def decreaseVal( self, value ):
		if value == 0:
			return False
		
		if self.val == 0:
			return False
		
		self.val = max( 0, self.val - value )
		return True
	
	def setVal( self, value ):
		validValue = max( 0, min( self.reqVal, value ) )
		if self.val == validValue:
			return False
		
		self.val = validValue
		return True

	def isCompleted( self ):
		return self.val >= self.reqVal

	def gmSetVal( self, value ):
		self.val += value
		if self.val >= self.reqVal:
			self.val = self.reqVal
		
		return True

	def getPriority( self ):
		return self.priority

class SStageTask_killMonster( SpaceStageTaskBase ):
	"""
	杀怪
	"""
	def getType( self ):
		return Define.SPACE_STAGE_TASK_KILL_MONSTER

	def checkMonsterScriptID( self, scriptID ):
		scriptIDList = self.param1.split("|")
		return scriptID in scriptIDList

class SStageTask_triggerBox( SpaceStageTaskBase ):
	"""
	触发箱子
	"""
	def getType( self ):
		return Define.SPACE_STAGE_TASK_TRIGGER_BOX

	def checkBoxScriptID( self, scriptID ):
		return self.param1 == scriptID

class SStageTask_conditionChange( SpaceStageTaskBase ):
	"""
	副本某条件改变
	"""
	def getType( self ):
		return Define.SPACE_STAGE_TASK_CONDITION_CHANGE

	def checkCondition( self, senderType, senderID, conditionKey, extraValue ):
		if self.param1 and self.param1 != senderType:		# 发送者类型：AI填“AI”，镜头事件填“STORY”
			return False
		if self.param2:
			idList = self.param2.split( "|" )
			if senderID not in idList:			# 发送者ID：AI填发送者scriptID，镜头事件填镜头ID
				return False
		if self.param3 != conditionKey:						# 通知ID：string类型
			return False
		return True

class SStageTask_getItem( SpaceStageTaskBase ):
	"""
	获取物品
	"""
	def getType( self ):
		return Define.SPACE_STAGE_TASK_GET_ITEM
	
	def getReqItemID( self ):
		return int( self.param1 )
	
	def checkItemID( self, itemID ):
		return int( self.param1 ) == itemID

class SStageTask_enterArea( SpaceStageTaskBase ):
	"""
	进入某区域
	"""
	"""
	def init( self, taskIndex, dict ):
		self.taskIndex = taskIndex
		self.title = dict["title"]
		self.reqVal = dict["reqVal"]
		self.val = dict.get( "val", 0 )
		self.param1 = dict["param1"]	#区域类型:		1圆形，2多边形
		self.param2 = dict["param2"]	#区域z值范围:	最大z值|最小z值
		self.param3 = dict["param3"]	#区域参数:		圆形“x y z：半径”，多边形“x1 y1|x2 y2|...”
	"""
	
	def getType( self ):
		return Define.SPACE_STAGE_TASK_ENTER_AREA

class SStageTask_NPCObjectDestroy( SpaceStageTaskBase ):
	"""
	NPCObject销毁
	"""
	def getType( self ):
		return Define.SPACE_STAGE_TASK_ENTITY_DESTROY
	
	def checkEntityScriptID( self, scriptID ):
		scriptIDList = self.param1.split("|")
		return scriptID in scriptIDList

class SStageTask_CustomTask( SpaceStageTaskBase ):
	"""
	自定义事件
	"""
	def getType( self ):
		return Define.SPACE_STAGE_TASK_CUSTOM_TASK

class SStageTask_UseItem( SpaceStageTaskBase ):
	"""
	使用物品完成阶段目标
	"""
	def getType( self ):
		return Define.SPACE_STAGE_TASK_USE_ITEM
	
	def getReqItemID( self ):
		return int( self.param1 )
	
	def checkItemID( self, itemID ):
		return int( self.param1 ) == itemID

class SStageTask_UseTitle( SpaceStageTaskBase ):
	"""
	装备称号完成阶段目标
	"""
	def getType( self ):
		return Define.SPACE_STAGE_TASK_USE_TITLE
	
	def getReqItemID( self ):
		return int( self.param1 )
	
	def checkTitleID( self, titleID ):
		return int( self.param1 ) == titleID

SpaceStageTaskDataType.MAP_TASK_TYPE_TO_TASK_CLASS( Define.SPACE_STAGE_TASK_KILL_MONSTER, SStageTask_killMonster )
SpaceStageTaskDataType.MAP_TASK_TYPE_TO_TASK_CLASS( Define.SPACE_STAGE_TASK_TRIGGER_BOX, SStageTask_triggerBox )
SpaceStageTaskDataType.MAP_TASK_TYPE_TO_TASK_CLASS( Define.SPACE_STAGE_TASK_CONDITION_CHANGE, SStageTask_conditionChange )
SpaceStageTaskDataType.MAP_TASK_TYPE_TO_TASK_CLASS( Define.SPACE_STAGE_TASK_GET_ITEM, SStageTask_getItem )
SpaceStageTaskDataType.MAP_TASK_TYPE_TO_TASK_CLASS( Define.SPACE_STAGE_TASK_ENTER_AREA, SStageTask_enterArea )
SpaceStageTaskDataType.MAP_TASK_TYPE_TO_TASK_CLASS( Define.SPACE_STAGE_TASK_ENTITY_DESTROY, SStageTask_NPCObjectDestroy )
SpaceStageTaskDataType.MAP_TASK_TYPE_TO_TASK_CLASS( Define.SPACE_STAGE_TASK_CUSTOM_TASK, SStageTask_CustomTask )
SpaceStageTaskDataType.MAP_TASK_TYPE_TO_TASK_CLASS( Define.SPACE_STAGE_TASK_USE_ITEM, SStageTask_UseItem )
SpaceStageTaskDataType.MAP_TASK_TYPE_TO_TASK_CLASS( Define.SPACE_STAGE_TASK_USE_TITLE, SStageTask_UseTitle )
# -*- coding: utf-8 -*-
#
import csdefine
import KBEngine
import KBEDebug
import csconst
from Singleton import Singleton

class TrapConditionMgr( Singleton ):
	"""
	陷阱触发条件管理
	"""
	def __init__( self ):
		"""
		"""
		self.map = {
			"level"			:	TrapConditionLevel,
			"camp"			:	TrapConditionCamp,
			"quest"			:	TrapConditionQuest,
			"death"			:	TrapConditionDeath,
			"hasBuffs"		: 	TrapConditionHasBuffs,
			"entityState"	:	TrapConditionEntityState,
			"belongSide"	:	TrapConditionEntityBelongSide,
			"hasBuffsOr"    : 	TrapConditionHasBuffsOr,
		}

	def getType( self, type ):
		"""
		根据类型给予条件
		"""
		return self.map.get( type, None )

	def validate( self, trapEntity, avatar, type, value ):
		"""
		触发陷阱验证
		@param trapEntity: 陷阱
		@type  trapEntity: ENTITY
		@param avatar: 触发对象
		@type  avatar: ENTITY
		@param type: 条件配置关键字
		@type  type: STRING
		@param value: 条件数据
		@type  value: [str(param1), str(param2),str(param3)]
		@return BOOL
		"""
		conditionFunc = self.getType( type )
		if conditionFunc == None:
			return False

		return conditionFunc.validate( trapEntity, avatar, value )

class TrapConditionBase:
	"""
	陷阱触发条件基础类
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		return True

class TrapConditionLevel( TrapConditionBase ):
	"""
	等级限制
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		if not hasattr( avatar, "level" ):
			return False
		return avatar.level >= int(value[0])
		
class TrapConditionCamp( TrapConditionBase ):
	"""
	阵营限制
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		if not hasattr( avatar, "camp" ):
			return False
		return avatar.getFinalCamp() == int(value[0])
		
class TrapConditionQuest( TrapConditionBase ):
	"""
	任务状态限制
	"qID:qState;tID:tState;tID:tState|...."
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		if not avatar.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			return False
		quests = value[0].split("|")
		for questStr in quests:
			questList = questStr.split(";")
			quest = questList.pop(0)
			questID,questState = quest.split(":")
			if avatar.queryQuestStatus(int(questID)) != int(questState ):
				continue
				
			taskPass = True
			for task in questList:
				taskID,taskState = task.split(":")
				if avatar.queryTaskStatus(int(questID),int(taskID)) != int(taskState):
					taskPass = False
					break
			if taskPass:
				return True
		return False

class TrapConditionRole( TrapConditionBase ):
	"""
	是否为玩家
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		if avatar.__class__.__name__ == "Role":
			return True
		return False
		
class TrapConditionDeath( TrapConditionBase ):
	"""
	玩家死亡是否允许触发
	cs-4045
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		if avatar.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			if not int(value[0]) and avatar.state == csdefine.ENTITY_STATE_DEAD:
				return False
		
		return True

class TrapConditionHasBuffs( TrapConditionBase ):
	"""
	判断Entity身上是否有这些buff
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		buffIDList = [int(i) for i in value[0].split("|")]
		for buffID in buffIDList:
			if not len(avatar.findBuffsByBuffID( int(buffID) )):
				return False
		return True

class TrapConditionEntityState( TrapConditionBase ):
	"""
	判断Entity是否该类型并且不在某个状态下
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		entityType = value[0]
		stateList = [int(i) for i in value[1].split("|")]
		#目标类型判断
		if entityType != csconst.ENTITY_TYPE_DICT.get(avatar.getEntityFlag(),"") or avatar.getState() in stateList:
			return False
		return True

class TrapConditionEntityBelongSide( TrapConditionBase ):
	"""
	判断Entity攻守方（0：攻方，1：守方）
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		return avatar.isBelongSide( int(value[0]) )
		

class TrapConditionHasBuffsOr( TrapConditionBase ):
	"""
	判断Entity身上是否有这些buff中的一个
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def validate( trapEntity, avatar, value ):
		"""
		"""
		buffIDList = [int(i) for i in value[0].split("|")]
		for buffID in buffIDList:
			if len(avatar.findBuffsByBuffID( int(buffID) )):
				return True
		return False

g_trapConditionMgr = TrapConditionMgr()

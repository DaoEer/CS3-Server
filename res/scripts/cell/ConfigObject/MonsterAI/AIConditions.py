# -*- coding: utf-8 -*-
import time
import random
import Math
import Functions
import math

import KBEngine
import KBEDebug
from ConfigObject.MonsterAI.AIBase import AIConditionBase
import csdefine
import csconst
import Const
import KBEMath
import Functions
from NPCMoveScript import MoveBase
import ECBProximityDefine
import csarithmetic


MAPPING_ENTITY_TYPES = {
				1:"Role",
				2:"Space",
				3:"Monster",
				4:"NPC"
		}

class AICondition1( AIConditionBase.AIConditionBase ):
	"""
	是否在自己出生点范围
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radius = 1 		#表示范围

	def initData( self, section ):
		"""
		virtual method
		@param	section	: 	存储数据的数据段
		@type	section	:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData( self, section )
		if section[ "param1" ]:
			self.radius = int(section[ "param1" ])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		vitural method
		@param	ai		: 	拥有此条件的AI  ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AI of instance, AIBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		return  entity.monsterAICheckInSpawnPosition(self.radius)

class AICondition2( AIConditionBase.AIConditionBase ):
	"""
	战斗开始后多少秒
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.combatSecond = 0

	def initData( self ,section):
		"""
		virtual method
		@param section : 存储的数据字段
		@type  section : PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData( self, section )
		self.combatSecond = float( section[ "param1" ] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param 	ai 	:	拥有此条件的ai （做此支持是为了得到或写AI的动态数据）
		@type	ai 	:	AI of instance, AIBase
		@param 	entity:	执行此AICondition的entity
		@type 	entity:	entity
		"""
		return (Functions.getTime() - entity.monsterAICombatTime) > self.combatSecond* csconst.TIME_ENLARGE_MULTIPLE

class AICondition3(AIConditionBase.AIConditionBase):
	"""
	战斗开始后每隔多少秒
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.repeatSecond = 1
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section["param1"]:
			self.repeatSecond = int(float(section["param1"]) * csconst.TIME_ENLARGE_MULTIPLE)

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		t=Functions.getTime()
		#如果差值小于间隔时间，直接返False
		if (t - entity.monsterAICombatTime) < self.repeatSecond:
			return False
		#由于tick到达时间存在偏差，这里作一些修正处理
		tempVal = (t - entity.monsterAICombatTime ) % self.repeatSecond
		tempVal = (float(format(tempVal/csconst.TIME_ENLARGE_MULTIPLE,'.1f'))*csconst.TIME_ENLARGE_MULTIPLE) % self.repeatSecond
		if (entity.monsterAITickSpeed * csconst.TIME_ENLARGE_MULTIPLE < self.repeatSecond) and (tempVal>=entity.monsterAITickSpeed * csconst.TIME_ENLARGE_MULTIPLE):
			return False
		#差值大于等于间隔时间判断余数，误差在一个tick内就算是正确的
		result = entity.monsterAICombatTime > 0 and  (tempVal - entity.monsterAITickSpeed * csconst.TIME_ENLARGE_MULTIPLE)<entity.monsterAITickSpeed * csconst.TIME_ENLARGE_MULTIPLE
		return result

class AICondition4(AIConditionBase.AIConditionBase):
	"""
	自身处于战斗状态
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.getState() == csdefine.ENTITY_STATE_FIGHT

class AICondition5(AIConditionBase.AIConditionBase):
	"""
	自身处于非战斗状态
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.getState() != csdefine.ENTITY_STATE_FIGHT

class AICondition6(AIConditionBase.AIConditionBase):
	"""
	自身处于自由状态
	"""
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData(self, section):
		AIConditionBase.AIConditionBase.initData(self, section)

	def check( self, ai, entity, args, triggerEntity ):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		return entity.getState() == csdefine.ENTITY_STATE_FREE

class AICondition7(AIConditionBase.AIConditionBase):
	"""
	自身处于重置状态
	"""
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData(self, section):
		AIConditionBase.AIConditionBase.initData(self, section)

	def check( self, ai, entity, args, triggerEntity ):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		result = entity.getState() == csdefine.ENTITY_STATE_RESET
		return result

class AICondition8(AIConditionBase.AIConditionBase):
	"""
	自身是否处于死亡状态
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		result = entity.isState(csdefine.ENTITY_STATE_DEAD)
		return result

class AICondition9(AIConditionBase.AIConditionBase):
	"""
	自身生命值不高于某个百分比(参数为百分制)
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.hpPercent = 0
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.hpPercent = float(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		HP = math.ceil(entity.HP_Max * self.hpPercent/100)
		return entity.HP <= HP

class AICondition10(AIConditionBase.AIConditionBase):
	"""
	指定技能可对当前目标使用
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.skillIndex = 0
		self.priorityLevel = csdefine.BEHAVIOUR_COMMON
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.skillIndex = int(section["param1"])
		if len(section["param2"]):
			self.priorityLevel = int( section["param2"] )
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.monsterAIIsCanUseSkillToTarget(self.skillIndex)
		# return entity.monsterAIIsCanUseSkillToTarget(self.skillIndex)  and \
		# 		entity.behaviours[2].isCanAddBehavior( entity,[self.skillIndex, entity.id,False], self.priorityLevel )

class AICondition11(AIConditionBase.AIConditionBase):
	"""
	指定技能可对自身使用
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.skillIndex = 0
		self.priorityLevel = csdefine.BEHAVIOUR_COMMON

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.skillIndex = int(section["param1"])
		if len(section["param2"]):
			self.priorityLevel = int( section["param2"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.monsterAIIsCanUseSkillToSelf(self.skillIndex)  and \
				entity.behaviours[2].isCanAddBehavior( entity,[self.skillIndex, entity.id,False], self.priorityLevel )

class AICondition12(AIConditionBase.AIConditionBase):
	"""
	某记录时间是否到达
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.timeTagName = ""
		self.delaySecond = 0
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.timeTagName = section["param1"]
		self.delaySecond = float(section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if self.timeTagName in entity.monsterAITimeTag :
			recordTime = float(entity.monsterAITimeTag[self.timeTagName])
			return time.time() - recordTime > self.delaySecond
		else:
			return False

class AICondition13(AIConditionBase.AIConditionBase):
	"""
	判断当前AI目标类型
	param1：目标类型 ，判断目标是否为param1类型
	param2: 如果有scriptID，则判断目标scriptID是否在param2中 （选填）
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.aiType = ""
		self.monsterScriptID = []
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.aiType = section["param1"]
		if section["param2"]:
			self.monsterScriptID = section["param2"].split("|")


	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = KBEngine.entities.get( entity.monsterAIGetTarget(), None )
		if not aiTargetEntity:
			return False
			
		if aiTargetEntity.getEntityFlag() not in MAPPING_ENTITY_TYPES:
			return False
			
		eType = MAPPING_ENTITY_TYPES[aiTargetEntity.getEntityFlag()]
		if eType != self.aiType:
			return False
		if not self.monsterScriptID:
			return True
		if eType == "Role":
			return True	
		if aiTargetEntity.getScriptID() in self.monsterScriptID:
			return True
		return False

class AICondition14(AIConditionBase.AIConditionBase):
	"""
	自身存在某BUFF(列表中为或的关系)
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.buffIDs = []
		#self.buffLevel = 0
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if len(section["param1"]):
			self.buffIDs = [int(buffID) for buffID in section["param1"].split("|")]
		#self.buffLevel = int(section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		for buffID in self.buffIDs:
			if len( entity.findBuffsByBuffID(buffID) ):
				return True
		return False

class AICondition15(AIConditionBase.AIConditionBase):
	"""
	自身不存在某BUFF
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.buffIDs = []
		#self.buffLevel = 0
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if len(section["param1"]):
			self.buffIDs = [int(buffID) for buffID in section["param1"].split("|")]
		#self.buffLevel = int(section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		for buffID in self.buffIDs:
			if len( entity.findBuffsByBuffID(buffID) ):
				return False
		return True
		

class AICondition16(AIConditionBase.AIConditionBase):
	"""
	脱离重置状态
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if entity.getLastState() == csdefine.ENTITY_STATE_RESET and entity.getState() != csdefine.ENTITY_STATE_RESET:
			return True
		else:
			return False

class AICondition17(AIConditionBase.AIConditionBase):
	"""
	自身是否在指定位置
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.position = (0,0,0)
		self.radiusDistance = 0
		self.spaceName = []

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		position = Functions.vector3TypeConvert( section["param1"] )
		if position is None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
		else:
			self.position = KBEMath.Unreal2KBEnginePosition( position )
		self.radiusDistance = int(section["param2"])
		if section["param3"]:
			self.spaceName = section["param3"].split("|")
		else:
			self.spaceName = None

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if self.spaceName:
			if entity.getCurrentSpaceScriptID() in self.spaceName:
				if entity.position.distTo(self.position) <= self.radiusDistance:
					return True
		else:
			if entity.position.distTo(self.position) <= self.radiusDistance:
				return True
		return False

class AICondition18(AIConditionBase.AIConditionBase):
	"""
	自身是否不在指定位置
	如果填了地图ID，则需进行地图的判断，需判断自身是否在self.spaceName地图列表中
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.position = (0,0,0)
		self.radiusDistance = 0
		self.spaceName = ""

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		position = Functions.vector3TypeConvert( section["param1"] )
		if position is None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
		else:
			self.position = KBEMath.Unreal2KBEnginePosition( position )
		self.radiusDistance = int(section["param2"])
		if section["param3"]:
			self.spaceName = section["param3"].split("|")
		else:
			self.spaceName = None

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if self.spaceName:
			if entity.getCurrentSpaceScriptID() in self.spaceName:
				if entity.position.flatDistTo(self.position) <= self.radiusDistance:
					return False
		else:
			if entity.position.flatDistTo(self.position) <= self.radiusDistance:
				return False

		return True

class AICondition19(AIConditionBase.AIConditionBase):
	"""
	param1为任务ID，如果填了此参数则表示与任务相关，如果没有填则与任务无关,主要用于判断AI目标玩家是否被执行过当前AI
	任务相关：
			判断AI目标玩家的记录，如果questID与aiid都匹配则表示当前已经执行过
	任务无关：
			判断自身的记录，查看当前aiid与AI目标玩家DBID是否已保存记录匹配，匹配则执行过当前AI
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.questID = 0										#任务ID

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section[ "param1" ]:
			self.questID = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = KBEngine.entities.get( entity.monsterAIGetTarget(), None )
		if not aiTargetEntity or not aiTargetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			return False

		if self.questID:
			exists = True
			for data in aiTargetEntity.questResetAIIDS:
				aiid = int(str(entity.scriptID)+str(ai.getID()))
				if data.questID == self.questID and aiid in data.aiIDS:
					exists = False
					break

			return exists
		else:
			return not entity.monsterAIIsMarkRoleForAIID(ai.getID(),aiTargetEntity.playerDBID)

class AICondition20(AIConditionBase.AIConditionBase):
	"""
	AI目标对某任务的进行状态是否处于指定的任务状态列表中
	任务目标ID及目标状态，如果有任务目标ID以及目标状态参数，则优先进行任务目标的判断，不进行任务状态的判断
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.questID = 0
		self.questStatusList = []
		self.questTargetList = []

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.questID = int(section["param1"])
		self.questStatusList = section["param2"].split("|")
		if section["param3"]:
			self.questTargetList = section["param3"].split("|")

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = KBEngine.entities.get( entity.monsterAIGetTarget(), None )
		if aiTargetEntity and aiTargetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			if len(self.questTargetList):
				result = True
				for questTarget in self.questTargetList:
					quest = questTarget.split(":")
					if len(quest) > 1:
						targetStatus = aiTargetEntity.queryTaskStatus(self.questID, int(quest[0]))
						if not targetStatus == int(quest[1]):
							result = False
					else:
						KBEDebug.ERROR_MSG("AICondition20 questTargetList is error")
						return False
				return result
			else:
				questStatus = str(aiTargetEntity.queryQuestStatus(self.questID))
				if questStatus in self.questStatusList:
					return True
				
		return False

class AICondition21(AIConditionBase.AIConditionBase):
	"""
	某一范围内有指定entityType的scriptID
	如果没有填scriptID，则只判断范围内有没有指定类型的entity
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]
		

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])

		self.entityType  = section["param2"]
		if section[ "param3" ].strip()!="":
			self.scriptIDs  = section["param3"].strip().split("|")
		if section[ "param4" ].strip()!="":
			self.removeStates  = [int(state) for state in section["param4"].strip().split("|")]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs, self.removeStates )
		if len(entities) > 0 :
			return True
		else:
			return False

class AICondition22(AIConditionBase.AIConditionBase):
	"""
	某一范围内没有指定type的scriptID
	如果没有填scriptID，则只判断范围内有没有指定类型的entity
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]
		

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])

		self.entityType  = section["param2"]
		if section[ "param3" ].strip()!="":
			self.scriptIDs  = section["param3"].strip().split("|")
		if section[ "param4" ].strip()!="":
			self.removeStates  = [int(state) for state in section["param4"].strip().split("|")]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType,self.scriptIDs,self.removeStates )
		if len(entities) > 0:
			return False
		else:
			return True

class AICondition23(AIConditionBase.AIConditionBase):
	"""
	自身和攻击目标的距离是不是大于指定值
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.distance = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.distance = float(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetID = entity.getTargetID()
		targetEntity = KBEngine.entities.get( targetID )
		if targetEntity:
			if int(entity.position.flatDistTo(targetEntity.position)*100)/100 <= self.distance:
				return False
		return True

class AICondition24(AIConditionBase.AIConditionBase):
	"""
	自身和攻击目标的距离是不是小于指定值
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.distance = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.distance = float(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetID = entity.getTargetID()
		targetEntity = KBEngine.entities.get( targetID )
		if targetEntity:
			if int(entity.position.flatDistTo(targetEntity.position)*100)/100 <= self.distance:
				return True
		return False


class AICondition25(AIConditionBase.AIConditionBase):
	"""
	AI指令是否合法
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.scriptIDS = []									#可接收指令的scriptID列表
		self.cmds = []

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section[ "param1" ]:
			self.scriptIDS = section[ "param1" ].split("|")
		self.cmds = section[ "param2" ].split("|")

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if len(args) == 0:
			return False

		entityID, scriptID, cmd = args

		if cmd not in self.cmds:
			return False

		if not len(self.scriptIDS):				# 如果没有指定发布者则响应所有发布者的指令
			return True

		if scriptID in self.scriptIDS:
			return True

		return False

class AICondition26(AIConditionBase.AIConditionBase):
	"""
	某个技能释放成功或失败
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.skillID = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.skillID = int(section[ "param1" ])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if len(args) and args[0] == self.skillID:
			KBEDebug.DEBUG_MSG_FOR_AI(entity,"entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) args = %s,skillID = %s AICondition26检测 释放成功"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, args,self.skillID))
			return True
		else:
			KBEDebug.DEBUG_MSG_FOR_AI(entity,"entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) args = %s,skillID = %s AICondition26检测 释放失败"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState,args,self.skillID))
			return False


class AICondition27(AIConditionBase.AIConditionBase):
	"""
	是否存在某些标记
	Param1：sign 支持填写多个，以竖号分隔，表示且的关系
					注意：标记在怪物重置后不清除
	"""		
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self, section ):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.signs = set(section["param1"].strip().split("|"))

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		for sign in self.signs:
			if sign not in entity.signs:
				return False
		
		return True


class AICondition28(AIConditionBase.AIConditionBase):
	"""
	是否不存在某些标记
	Param1：sign 支持填写多个，以竖号分隔，表示且的关系
					注意：标记在怪物重置后不清除
	"""		
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self, section ):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.signs = set(section["param1"].strip().split("|"))

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		for sign in self.signs:
			if sign in entity.signs:
				return False
		
		return True


class AICondition29(AIConditionBase.AIConditionBase):
	"""
	判断一定范围内entity数量是否满足特定的数量关系

	Param1：radius 半径，单位米
	Param2：eType 类型，支持多类型，例如Monster、NPC等
	Param3：scriptID 选填项，支持填写多个，以竖号分隔，表示或的关系
	Param4：relation 0代表“=” 1代表“<” 2代表“>”
	Param5：amount 数量，整型
	"""
	def __init__( self, aiID ):

		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.scriptIDs = [""]
		self.eType = None
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT

	def initData( self, section ):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])

		self.eType = section["param2"]
		self.scriptIDs = section["param3"].split("|")
		self.relation = section["param4"]
		self.amount = int(section["param5"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if self.eType not in MAPPING_ENTITY_TYPES.values():
			KBEDebug.ERROR_MSG("param2 Error!")
			return

		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.eType )
		if self.scriptIDs == [""]:
			amount = len(entities)
		else:
			amount = 0
		for e in entities:
			if e.getScriptID() in self.scriptIDs:
				amount+=1
		if self.relation == "0":
			return amount == self.amount
		elif self.relation =="1":
			return amount < self.amount
		else:
			return amount > self.amount

class AICondition30(AIConditionBase.AIConditionBase):
	"""
	当前状态处于未决状态
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.getState() == csdefine.ENTITY_STATE_PEAD
		
class AICondition31(AIConditionBase.AIConditionBase):
	"""
	当前状态处于表演状态
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.getState() == csdefine.ENTITY_STATE_SHOW

class AICondition32(AIConditionBase.AIConditionBase):
	"""
	当前没有正在播放出场动作
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entityww
		"""
		return  not entity._isPlayAdmissionAction

class AICondition33(AIConditionBase.AIConditionBase):
	"""
	判断与归属玩家的距离
	参数1：大于指定距离 参数2：小于指定距离 2个参数都为选填，2个参数之间为“或”的关系
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.minDist = -1
		self.maxDist = 1000000

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section["param1"].strip():
			self.maxDist = float(section["param1"].strip())
		if section["param2"].strip():
			self.minDist = float(section["param2"].strip())

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if hasattr( entity, 'owner' ):
			if not entity.owner:
				return False
			
			master = KBEngine.entities.get( entity.owner.id, None )
			if not master:
				return False

			distance = entity.position.flatDistTo( master.position )
			if distance > self.maxDist or distance < self.minDist:
				return True
			
		if hasattr(entity, "ownerID"):
			owner = entity.getOwnerEntity()
			if not owner:
				return False
			
			distance = entity.position.flatDistTo( owner.position )
			if distance > self.maxDist or distance < self.minDist:
				return True
		
		return False
		
		
class AICondition34(AIConditionBase.AIConditionBase):
	"""
	判断AI目标有特定Buff
	param1：BuffID，支持多个，以竖号分隔，表示且；

	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.buffIDs = None

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]
			

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = entity.monsterAIGetTargetEntity()
		if not aiTargetEntity:
			return

		for buffID in self.buffIDs:
			if not len(aiTargetEntity.findBuffsByBuffID( buffID )):
				return False
		return True

class AICondition35(AIConditionBase.AIConditionBase):
	"""
	判断AI目标没有特定Buff
	param1：BuffID，支持多个，以竖号分隔，表示且；

	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.buffIDs = None

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]
			

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = entity.monsterAIGetTargetEntity()
		if not aiTargetEntity:
			return

		for buffID in self.buffIDs:
			if  len(aiTargetEntity.findBuffsByBuffID( buffID )):
				return False
		return True

class AICondition36(AIConditionBase.AIConditionBase):
	"""
	某一范围内有特定Buff的entity
	param1：半径，单位米；
	param2：BuffID，支持多个，以竖号分隔，表示且；
	param3：类型；
	param4：选填。 scriptID
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.buffIDs = []
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.buffIDs =  [int(buffID) for buffID in section["param2"].strip().split("|")]
		self.entityType = section["param3"].strip()
		if section["param4"].strip()!="":
			self.scriptIDs = section["param4"].strip().split("|")
		if section["param5"].strip()!="":
			self.removeStates = [int(state) for state in section["param5"].strip().split("|")]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""

		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs, self.removeStates )

		if not len(entities):
			return False
			
		for e in entities:
			isHasBuff = True
			for buffID in self.buffIDs:
				if not len(e.findBuffsByBuffID( buffID )):
					isHasBuff = False
					break
			if isHasBuff:
				return True
		return False

class AICondition37(AIConditionBase.AIConditionBase):
	"""
	某一范围内没有特定Buff的entity
	param1：半径，单位米；
	param2：BuffID，支持多个，以竖号分隔，表示且；
	param3：类型；
	param4：选填。 scriptID
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.buffIDs = []
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])

		self.buffIDs =  [int(buffID) for buffID in section["param2"].strip().split("|")]
		self.entityType = section["param3"].strip()
		if section["param4"].strip()!="":
			self.scriptIDs = section["param4"].strip().split("|")
		if section["param5"].strip()!="":
			self.removeStates = [int(state) for state in section["param5"].strip().split("|")]


	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs, self.removeStates )

		if not len(entities):
			return False
			
		for e in entities:
			isHasBuff = False
			for buffID in self.buffIDs:
				if len(e.findBuffsByBuffID( buffID )):
					isHasBuff = True
					break
			if not isHasBuff:
				return True
		return False


class AICondition38(AIConditionBase.AIConditionBase):
	"""
	entity是否在某个地图
	param1：支持多个，以竖号分隔，表示或
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.spaceScriptID = []

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.spaceScriptID = section["param1"].strip().split("|")
			

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.getCurrentSpaceScriptID() in self.spaceScriptID


class AICondition39(AIConditionBase.AIConditionBase):
	"""
	entity不在某个地图
	param1：支持多个，以竖号分隔，表示或
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.spaceScriptID = []

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.spaceScriptID = section["param1"].strip().split("|")

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return not entity.getCurrentSpaceScriptID() in self.spaceScriptID

class AICondition40(AIConditionBase.AIConditionBase):
	"""
	AI目标当前不处于指定状态
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.state = csdefine.ENTITY_STATE_MAX

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.state = int( section["param1"].strip() )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetEntity = entity.monsterAIGetTargetEntity()
		if not targetEntity:
			KBEDebug.ERROR_MSG("targetEntity is none!")
			return False
		
		return not targetEntity.getState() == self.state


class AICondition41(AIConditionBase.AIConditionBase):
	"""
	怪物出场动作完毕
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entityww
		"""
		return  entity.isMonsterAppearJumpOver()


class AICondition42(AIConditionBase.AIConditionBase):
	"""
	callMonster攻击目标与主人的距离是不是小于指定值
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.distance = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.distance = int(section["param1"])


	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetID = entity.getTargetID()
		targetEntity = KBEngine.entities.get( targetID )
		ownerEntity = KBEngine.entities.get( entity.owner.id, None )
		if targetEntity and ownerEntity:
			if ownerEntity.position.flatDistTo(targetEntity.position) <= self.distance:
				return True
		return False


class AICondition43(AIConditionBase.AIConditionBase):
	"""
	当前为稳定状态
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.distance = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )


	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.getState() == csdefine.ENTITY_STATE_STABLE


class AICondition44(AIConditionBase.AIConditionBase):
	"""
	forAIEvent
	判断当前triggerEntity类型
	param1：目标类型 ，判断目标是否为param1类型
	param2: 如果有scriptID，则判断目标scriptID是否在param2中 （选填）
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.aiType = ""
		self.monsterScriptID = []
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.aiType = section["param1"]
		if section["param2"]:
			self.monsterScriptID = section["param2"].split("|")


	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = triggerEntity
		if not aiTargetEntity:
			return False
			
		if aiTargetEntity.getEntityFlag() not in MAPPING_ENTITY_TYPES:
			return False
			
		eType = MAPPING_ENTITY_TYPES[aiTargetEntity.getEntityFlag()]
		if eType != self.aiType:
			return False
		if not self.monsterScriptID:
			return True
		if eType == "Role":
			return True	
		if aiTargetEntity.getScriptID() in self.monsterScriptID:
			return True
		return False



class AICondition45(AIConditionBase.AIConditionBase):
	"""
	forAIEvent
	param1为任务ID，如果填了此参数则表示与任务相关，如果没有填则与任务无关,主要用于判断AI目标玩家是否被执行过当前AI
	任务相关：
			判断AI目标玩家的记录，如果questID与aiid都匹配则表示当前已经执行过
	任务无关：
			判断自身的记录，查看当前aiid与AI目标玩家DBID是否已保存记录匹配，匹配则执行过当前AI
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.questID = 0										#任务ID

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section[ "param1" ]:
			self.questID = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = triggerEntity
		if not aiTargetEntity or not aiTargetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			return False

		if self.questID:
			exists = True
			for data in aiTargetEntity.questResetAIIDS:
				aiid = int(str(entity.scriptID)+str(ai.getID()))
				if data.questID == self.questID and aiid in data.aiIDS:
					exists = False
					break

			return exists
		else:
			return not entity.monsterAIIsMarkRoleForAIID(ai.getID(),aiTargetEntity.playerDBID)


class AICondition46(AIConditionBase.AIConditionBase):
	"""
	forAIEvent
	触发triggerEntity当前不处于指定状态
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.state = csdefine.ENTITY_STATE_MAX

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.state = int( section["param1"].strip() )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetEntity = triggerEntity
		if not targetEntity:
			KBEDebug.ERROR_MSG("targetEntity is none!")
			return False
		
		return not targetEntity.getState() == self.state


class AICondition47(AIConditionBase.AIConditionBase):
	"""
	forAIEvent
	判断triggerEntity有特定Buff
	param1：BuffID，支持多个，以竖号分隔，表示且；

	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.buffIDs = None

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]
			

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = triggerEntity
		if not aiTargetEntity:
			return

		for buffID in self.buffIDs:
			if not len(aiTargetEntity.findBuffsByBuffID( buffID )):
				return False
		return True

class AICondition48(AIConditionBase.AIConditionBase):
	"""
	forAIEvent
	判断triggerEntity没有特定Buff
	param1：BuffID，支持多个，以竖号分隔，表示且；

	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.buffIDs = None

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]
			

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = triggerEntity
		if not aiTargetEntity:
			return

		for buffID in self.buffIDs:
			if  len(aiTargetEntity.findBuffsByBuffID( buffID )):
				return False
		return True



class AICondition49(AIConditionBase.AIConditionBase):
	"""
	triggerEntity对某任务的进行状态是否处于指定的任务状态列表中
	任务目标ID及目标状态，如果有任务目标ID以及目标状态参数，则优先进行任务目标的判断，不进行任务状态的判断
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.questID = 0
		self.questStatusList = []
		self.questTargetList = []

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.questID = int(section["param1"])
		self.questStatusList = section["param2"].split("|")
		if section["param3"]:
			self.questTargetList = section["param3"].split("|")

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = triggerEntity
		if aiTargetEntity and aiTargetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			if len(self.questTargetList):
				result = True
				for questTarget in self.questTargetList:
					quest = questTarget.split(":")
					if len(quest) > 1:
						targetStatus = aiTargetEntity.queryTaskStatus(self.questID, int(quest[0]))
						if not targetStatus == int(quest[1]):
							result = False
					else:
						KBEDebug.ERROR_MSG("AICondition20 questTargetList is error")
						return False
				return result
			else:
				questStatus = str(aiTargetEntity.queryQuestStatus(self.questID))
				if questStatus in self.questStatusList:
					return True
				
		return False



class AICondition50(AIConditionBase.AIConditionBase):
	"""
	forAIEvent
	判断triggerEntity没有特定Buff
	param1：BuffID，支持多个，以竖号分隔，表示且；

	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.buffIDs = None

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]
			

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = triggerEntity
		if not aiTargetEntity:
			return

		for buffID in self.buffIDs:
			if  len(aiTargetEntity.findBuffsByBuffID( buffID )):
				return False
		return True


class AICondition51(AIConditionBase.AIConditionBase):
	"""
	判断AI目标的阵营和性别
	param1:	阵营
	param2:	性别

	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.camp = csdefine.CMAP_NONE
		self.gender = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.camp =  int(section["param1"].strip())
		self.gender = int(section["param2"].strip())	

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = entity.monsterAIGetTargetEntity()
		if not aiTargetEntity:
			return

		if self.camp == aiTargetEntity.getFinalCamp() and self.gender == aiTargetEntity.gender:
			return True
		return False


class AICondition52(AIConditionBase.AIConditionBase):
	"""
	判断triggerEntity的阵营和性别
	param1:	阵营
	param2:	性别

	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.camp = csdefine.CMAP_NONE
		self.gender = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.camp =  int(section["param1"].strip())
		self.gender = int(section["param2"].strip())	

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = triggerEntity
		if not aiTargetEntity:
			return

		if self.camp == aiTargetEntity.getFinalCamp() and self.gender == aiTargetEntity.gender:
			return True
		return False


class AICondition53(AIConditionBase.AIConditionBase):
	"""
	callMonster主人的敌人列表不为空
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )	

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if entity.getOwnerEntity() and len(entity.getOwnerEntity().enemyList):
			return True
		return False

class AICondition54(AIConditionBase.AIConditionBase):
	"""
	血量增加（只能配置在血量改变事件中）
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )	

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if args[0] > args[1]:
			return True
		return False

class AICondition55(AIConditionBase.AIConditionBase):
	"""
	血量减少（只能配置在血量改变事件中）
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )	

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if args[0] < args[1]:
			return True
		return False

class AICondition56(AIConditionBase.AIConditionBase):
	"""
	是妖魔化身
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )	

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity:
			modelNumber = spaceEntity.queryTemp( "demon_modelNumber", "" )
			if entity.modelNumber != modelNumber:
				return False
			for modelName, modelPart in Const.SEX_TO_MODEL[modelNumber].items():
				if getattr( entity, modelName, "" ) != spaceEntity.queryTemp( "demon_" + modelName, "" ):
					return False
			return True
		else:
			KBEDebug.ERROR_MSG("AICondition56 can not getCurrentSpace!!")
		return False
		
class AICondition57(AIConditionBase.AIConditionBase):
	"""
	不是妖魔化身
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )	

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity:
			modelNumber = spaceEntity.queryTemp( "demon_modelNumber", "" )
			if entity.modelNumber != modelNumber:
				return True
			for modelName, modelPart in Const.SEX_TO_MODEL[modelNumber].items():
				if getattr( entity, modelName, "" ) != spaceEntity.queryTemp( "demon_" + modelName, "" ):
					return True
			return False
		else:
			KBEDebug.ERROR_MSG("AICondition57 can not getCurrentSpace!!")
		return True

class AICondition58(AIConditionBase.AIConditionBase):
	"""
	是否是对话的某个key
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self._key = ""

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )	
		self._key = section["param1"]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if args[0] and self._key:
			if args[0] != self._key:
				return False
		return True

class AICondition59(AIConditionBase.AIConditionBase):
	"""
	自己巡逻路线为某值
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self._patrolList = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self._patrolList = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.patrolRoute == self._patrolList

class AICondition60(AIConditionBase.AIConditionBase):
	"""
	自身是否在某些指定位置
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.positionList = []
		self.radiusDistance = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		for i in section["param1"].split("|"):
			pos = Functions.vector3TypeConvert( i )
			if pos is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
			else:
				self.positionList.append( KBEMath.Unreal2KBEnginePosition( pos ) )
		self.radiusDistance = int(section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		for pos in self.positionList:
			if entity.position.flatDistTo(pos) <= self.radiusDistance:
				return True
		return False
		
class AICondition61(AIConditionBase.AIConditionBase):
	"""
	雷球选择正确
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		target = entity.monsterAIGetTargetEntity()
		if target:
			buffID = Const.LEI_SCRIPTID_TO_BUFFID[entity.scriptID]
			if len( target.findBuffsByBuffID( buffID )):
				return True
		return False
		
class AICondition62(AIConditionBase.AIConditionBase):
	"""
	雷球选择错误
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		target = entity.monsterAIGetTargetEntity()
		if target:
			buffID = Const.LEI_SCRIPTID_TO_BUFFID[entity.scriptID]
			if not len( target.findBuffsByBuffID( buffID )):
				return True
		return False


class AICondition63(AIConditionBase.AIConditionBase):
	"""
	攻击目标有特定Buff
	param1：BuffID，支持多个，以竖号分隔，表示且；

	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.buffIDs = None

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]
			

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetEntity = KBEngine.entities.get(entity.getTargetID(),None)
		if not targetEntity:
			return

		for buffID in self.buffIDs:
			if not len(targetEntity.findBuffsByBuffID( buffID )):
				return False
		return True

class AICondition64(AIConditionBase.AIConditionBase):
	"""
	到达某个高度
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self._height = 0.0
		self._dist = 0.0
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self._height = float( section["param1"] ) / 100		# 厘米转化为米
		self._dist = float( section["param2"] ) / 100

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if abs(entity.position.y - self._height) <= self._dist:
			return True
		return False

class AICondition65(AIConditionBase.AIConditionBase):
	"""
	是否不存在以触发AI者ID为标记的标记， CST-3248
	"""		
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self, section ):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		for sign in entity.signs:
			if sign.startswith("SIGN_ENTITY_ID_"):
				return False
		return True

class AICondition66(AIConditionBase.AIConditionBase):
	"""
	是否存在以本次触发AI者ID为标记的标记， CST-3248
	"""		
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self, section ):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		for sign in entity.signs:
			if sign.startswith("SIGN_ENTITY_ID_" + str(triggerEntity.id)):
				return True
		return False
				
class AICondition67(AIConditionBase.AIConditionBase):
	"""
	判断接收到的AI指令是否为指定指令
	"""		
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self, section ):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.command = section["param1"].strip()	#指令
		
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if len(args) < 3:
			KBEDebug.ERROR_MSG("AICondition66 recv message error")
			return False
		if args[2].strip() == self.command:
				return True
		return False


class AICondition68(AIConditionBase.AIConditionBase):
	"""
	某一范围内有指定entityType的scriptID
	如果没有填scriptID，则只判断范围内有没有指定类型的entity
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radius = 0.0
		self.entityType = ""
		self.scriptIDs = []
		

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.radius = float(section["param1"])
		self.entityType  = section["param2"]
		if section[ "param3" ].strip()!="":
			self.scriptIDs  = section["param3"].strip().split("|")

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtCircle( self.radius, self.entityType, entity.position )
		if not len(self.scriptIDs):
			return len(entities)

		for e in entities:
			if e.scriptID in self.scriptIDs:
				return True
		return False
				
class AICondition69(AIConditionBase.AIConditionBase):
	"""
	判断画卷属性是否为空（CST-3790）
	"""		
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self, section ):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return not entity.queryTemp("attributeType", False)

class AICondition70(AIConditionBase.AIConditionBase):
	"""
	判断画卷属性是否不为空且和机关属性不一致（CST-3790）
	"""		
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self, section ):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.scriptID = section["param1"].strip()	#机关scriptID
		
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if not entity or not entity.queryTemp("attributeType", None):
			return False
		entityIDList = entity.getCurrentSpace().getEntityRecord(self.scriptID)
		if len(entityIDList) != 1:
			KBEDebug.ERROR_MSG("AICondition70: entity[%s] is none or not the only one!" % self.scriptID)
			return False
		gearEntity = KBEngine.entities.get(entityIDList[0], None)
		if not gearEntity or not gearEntity.queryTemp("attributeType", None):	
			return False
		return entity.queryTemp("attributeType", None) != gearEntity.queryTemp("attributeType", None)
			
class AICondition71(AIConditionBase.AIConditionBase):
	"""
	判断画卷属性是否不为空且和机关属性一致（CST-3790）
	"""		
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self, section ):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.scriptID = section["param1"].strip()	#机关scriptID
		
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if not entity or not entity.queryTemp("attributeType", None):
			return False
		entityIDList = entity.getCurrentSpace().getEntityRecord(self.scriptID)
		if len(entityIDList) != 1:
			KBEDebug.ERROR_MSG("AICondition69: entity[%s] is none or not the only one!" % self.scriptID)
			return False
		gearEntity = KBEngine.entities.get(entityIDList[0], None)
		if not gearEntity or not gearEntity.queryTemp("attributeType", None):
			return False
		return entity.queryTemp("attributeType", None) == gearEntity.queryTemp("attributeType", None)

class AICondition72(AIConditionBase.AIConditionBase):
	"""
	巡逻到某个节点
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.position = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.patrolRoute = int(section["param1"])
		self.moveRoutePoint = int(section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		patrolRouteInfo = entity.getMoveScript().getCurrentSpacePatrolnfo( entity.getCurrentSpaceScriptID(), self.patrolRoute )
		if patrolRouteInfo:
			if Math.Vector3(patrolRouteInfo[self.moveRoutePoint]['position']).distTo( Math.Vector3(entity.position) ) < 1.5:
				return True
		return False

class AICondition73(AIConditionBase.AIConditionBase):
	"""
	判断罡气是否处于气竭状态
	"""
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.isQiJie = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""	
		if self.isQiJie:
			return entity.gangQiState == csdefine.GANG_QI_STATE_QI_JIE
		else:
			return entity.gangQiState != csdefine.GANG_QI_STATE_QI_JIE

class AICondition74(AIConditionBase.AIConditionBase):
	"""
	敌人列表里是否有玩家
	"""
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""	
		return len( entity.findEnemyByEntityType( csdefine.ENTITY_FLAG_ROLE ) ) > 0

class AICondition75(AIConditionBase.AIConditionBase):
	"""
	记录当前时间后每隔某个随机时间
	"""
	def __init__( self, aiID ):
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self._minTime = 0
		self._maxTime = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self._minTime = int(float(section["param1"]) * csconst.TIME_ENLARGE_MULTIPLE)
		self._maxTime = int(float(section["param2"]) * csconst.TIME_ENLARGE_MULTIPLE)
		self.timeTag = section["param3"]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if self.timeTag not in entity.monsterAITimeTag:
			return False

		if not entity.queryTemp("aiCondition75RandomTime"):
			_time = random.randint(self._minTime, self._maxTime)
			entity.setTemp("aiCondition75RandomTime", _time)
		recordTime = entity.monsterAITimeTag[self.timeTag]
		t = Functions.getTime()	
		if (t - recordTime * csconst.TIME_ENLARGE_MULTIPLE) < entity.monsterAITickSpeed * csconst.TIME_ENLARGE_MULTIPLE:
			return False
		_randomTime = entity.queryTemp("aiCondition75RandomTime")
		tempVal = (t - recordTime * csconst.TIME_ENLARGE_MULTIPLE ) % _randomTime
		result = recordTime > 0 and abs( entity.monsterAITickSpeed * csconst.TIME_ENLARGE_MULTIPLE - tempVal ) < (0.2 * csconst.TIME_ENLARGE_MULTIPLE )
		if result:
			entity.removeTemp("aiCondition75RandomTime")
		return result	
		
class AICondition76(AIConditionBase.AIConditionBase):
	"""
	判断自己阵营
	param1:	阵营
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.camp = csdefine.CMAP_NONE

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.camp =  int(section["param1"].strip())

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return self.camp == entity.getFinalCamp()


class AICondition77(AIConditionBase.AIConditionBase):
	"""
	模型缩放是否大于指定值
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.scale = 1.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.scale =  float(section["param1"].strip())

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return self.scale < entity.getModelScale()

class AICondition78(AIConditionBase.AIConditionBase):
	"""
	英雄王座：小兵判断当前等阶值
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.levelYXLM = 1

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.levelYXLM = int(section["param1"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return self.levelYXLM == entity.levelYXLM

class AICondition79(AIConditionBase.AIConditionBase):
	"""
	自身生命值高于或等于某个百分比(参数为百分制)
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.hpPercent = 0
		
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.hpPercent = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return (entity.HP / entity.HP_Max ) * 100 >= self.hpPercent

class AICondition80(AIConditionBase.AIConditionBase):
	"""
	针对专属怪物，触发者是创建者
	"""
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.creatorDBID == triggerEntity.playerDBID

class AICondition81(AIConditionBase.AIConditionBase):
	"""
	被中断移动类型是指定类型
	"""
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.oldMoveType = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		oldMoveType = args[0]
		return True if self.oldMoveType == oldMoveType else False
			

class AICondition82(AIConditionBase.AIConditionBase):
	"""
	当前能开启巡逻移动
	"""
	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if entity.isState(csdefine.ENTITY_STATE_DEAD):
			return False
		if entity.actionForbidSign(csdefine.ACTION_FORBID_MOVE):
			return False
		if not entity.getMoveScript().isCanBreak( entity, csdefine.MOVE_TYPE_PATROL ):
			return False
		return True

class AICondition83(AIConditionBase.AIConditionBase):
	"""
	CST-6262 蟠龙秘境 判断怪是否移动到目标位置
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radiusDistance = 0.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.radiusDistance = float( section["param1"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		dstPos = entity.queryTemp("dstPos")
		if dstPos == None:
			return False
		if entity.position.flatDistTo( dstPos ) <= self.radiusDistance:
			entity.removeTemp("dstPos")
			return True
		return False

class AICondition84(AIConditionBase.AIConditionBase):
	"""
	CST-7699 判断某语音是否播放完毕
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.soundID = ""

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.soundID = section["param1"]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		soundID = args[0]
		return soundID == self.soundID

class AICondition85(AIConditionBase.AIConditionBase):
	"""
	特殊属性改变,特殊属性是否为某值
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.attrValue = 0
		if section["param1"]:
			self.attrValue = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if not hasattr(entity,args[0]):
			return False
		
		return self.attrValue == args[1]

class AICondition86(AIConditionBase.AIConditionBase):
	"""
	CST-8727 勇闯夺命岛Boss 是否可以使用该物品
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.itemID = 0
		self.amount = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.itemID = int( section["param1"] )
		self.amount = 1
		if section["param2"]:
			self.amount = int( section["param2"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.isBossCanUseItem( self.itemID, self.amount )

class AICondition87(AIConditionBase.AIConditionBase):
	"""
	触发者血量满足某个数量关系 关系(1代表“>” 2代表“<”3代表“=”4代表“>=”5代表“<=”)
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.hpPercent = 0.0
		self.relationFlag = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.hpPercent = float( section["param1"] )
		self.relationFlag = int(section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		hp = math.ceil( triggerEntity.HP_Max * self.hpPercent )
		if self.relationFlag == 1 and triggerEntity.HP > hp:
			return True
		elif self.relationFlag == 2 and triggerEntity.HP < hp:
			return True
		elif self.relationFlag == 3 and triggerEntity.HP == hp:
			return True
		elif self.relationFlag == 4 and triggerEntity.HP >= hp:
			return True
		elif self.relationFlag == 5 and triggerEntity.HP <= hp:
			return True
		return False

class AICondition88(AIConditionBase.AIConditionBase):
	"""
	判断触发者周围有玩家的数量(在副本内)
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.searchDistance = 0.0
		self.roleCount = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.searchDistance = float( section["param1"] )
		self.roleCount = int( section["param2"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		tempCount = 0
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity:
			for role in spaceEntity._spaceRoles:
				if triggerEntity.position.flatDistTo( role.position ) <= self.searchDistance and role.id != triggerEntity.id:
					tempCount += 1
		return self.roleCount == tempCount

class AICondition89(AIConditionBase.AIConditionBase):
	"""
	CST-8726 勇闯夺命岛 判断小Boss 是否可以指引找到大Boss
	"""
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		bossScriptID = entity.queryTemp("searchBossID")
		if bossScriptID:
			spaceEntity = entity.getCurrentSpace()
			if not spaceEntity:
				return False
			entities = spaceEntity.getEntityMailBoxRecord( bossScriptID )
			if not len(entities):
				return False
			return True
		return False

class AICondition90(AIConditionBase.AIConditionBase):
	"""
	副本中怪物逃跑 是否逃跑下一个点  在MonsterEscapePointCfg.py  JIRA CST-8973
	"""
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		escapePoints = entity.queryTemp( "escapePoints" )
		if not escapePoints:
			return True
		point = escapePoints[0]
		if entity.position.distTo(point) <= 3.0:
			escapePoints.remove( point )
			if not len(escapePoints):
				entity.removeTemp("escapePoints")
			else:
				entity.setTemp( "escapePoints",escapePoints )
			return True
		return False

class AICondition91(AIConditionBase.AIConditionBase):
	"""
	副本中怪物逃跑 是否逃跑结束  在MonsterEscapePointCfg.py  JIRA CST-8973
	"""
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		escapePoints = entity.queryTemp( "escapePoints" )
		if not escapePoints:
			return True
		return False
		
class AICondition92(AIConditionBase.AIConditionBase):
	"""
	是否不存在某个记录时间的标记
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.timeTag = ""

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.timeTag = section["param1"]
	
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if self.timeTag  in entity.monsterAITimeTag:
			return False
		return True

class AICondition93(AIConditionBase.AIConditionBase):
	"""
	副本内判断玩家是否在怪物某个范围内并且满足大于某个数量关系或者血量关系
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.hpPercent = 0.0
		self.roleCount = 0
		self.radius = 0.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.hpPercent = float( section["param1"] )
		self.roleCount = int( section["param2"] )
		self.radius = float( section["param3"] )
	
	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return False
		if not spaceEntity.isInSpaceCopy():
			return False
		if not spaceEntity.isInSpacePlane():
			return False

		inAreaRoles = []
		for role in spaceEntity._spaceRoles:
			if role.position.distTo( entity.position ) <= self.radius:
				inAreaRoles.append( role )

		if len( inAreaRoles ) > self.roleCount:
			return True

		hp = math.ceil( triggerEntity.HP_Max * self.hpPercent )
		for role in inAreaRoles:
			if role.HP >= hp:
				return True

		return False

class AICondition94(AIConditionBase.AIConditionBase):
	"""
	检测怪物背后的矩形范围内是否有指定类型的entity(有为True)
	如果没有填scriptID，则只判断范围内有没有指定类型的entity
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.entityType = ""
		self.scriptIDs = []
		self.length = 0.0
		self.wide = 0.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.entityType = section[ "param1" ]
		if section["param2"].strip()!="":
			self.scriptIDs = section["param2"].strip().split("|")
		self.length = float(section["param3"])
		self.wide = float(section["param4"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtForBehind( self.length, self.wide, self.entityType, self.scriptIDs )
		if len(entities) > 0 :
			return True
		else:
			return False

class AICondition95(AIConditionBase.AIConditionBase):
	"""
	检测怪物背后的矩形范围内是否有指定类型的entity(无为True)
	如果没有填scriptID，则只判断范围内有没有指定类型的entity
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.entityType = ""
		self.scriptIDs = []
		self.length = 0.0
		self.wide = 0.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.entityType = section[ "param1" ]
		if section["param2"].strip()!="":
			self.scriptIDs = section["param2"].strip().split("|")
		self.length = float(section["param3"])
		self.wide = float(section["param4"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtForBehind( self.length, self.wide, self.entityType, self.scriptIDs )
		if len(entities) > 0 :
			return False
		else:
			return True

class AICondition96(AIConditionBase.AIConditionBase):
	"""
	勇闯绝命岛  是否寻找到Boss
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radiusDistance = 0.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.radiusDistance = float( section["param1"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		bossScriptID = entity.queryTemp("FindBossScriptID")
		if not bossScriptID:
			return True
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return True
		entities = spaceEntity.getEntityMailBoxRecord( bossScriptID )
		if not len( entities ):
			return True
		if entity.position.distTo(entities[0].position) <= self.radiusDistance:
			return True
		return False

class AICondition97(AIConditionBase.AIConditionBase):
	"""
	判断怪血量减少某个百分比 与AIAction247(记录怪的当前血量值)配套用
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.reduceHPPercent = 0.0
		self.recordKey = ""

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.reduceHPPercent = float( section["param1"] )
		self.recordKey = section["param2"]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		recordHP = entity.queryTemp( self.recordKey )
		if not recordHP:
			return False

		curPercent = float( entity.HP )/entity.HP_Max
		recordHPercent = float(recordHP)/entity.HP_Max
		reduceHP = float((recordHPercent - curPercent) * 100)
		if reduceHP >= self.reduceHPPercent:
			return True
		return False

class AICondition98(AIConditionBase.AIConditionBase):
	"""
	怪物是否移动到要开的箱子 SpellBoxPickItem
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radiusDistance = 0.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.radiusDistance = float( section["param1"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		spellBoxID = entity.queryTemp("OpenSpellBoxID")
		if spellBoxID == None:
			return False
		spellBoxEntity = KBEngine.entities.get( spellBoxID )
		if not spellBoxEntity:
			return False
		if entity.position.distTo(spellBoxEntity.position) <= self.radiusDistance:
			return True
		return False

class AICondition99(AIConditionBase.AIConditionBase):
	"""
	判断副本是某些怪是否存在
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.scriptIDs = []

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section["param1"]:
			self.scriptIDs = section["param1"].split("|")

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return False
		for scriptID in self.scriptIDs:
			entities = spaceEntity.getEntityMailBoxRecord( scriptID )
			for entity in entities:
				if entity.getState() != csdefine.ENTITY_STATE_DEAD:
					return True

		return False
		
class AICondition100(AIConditionBase.AIConditionBase):
	"""
	AI目标（火炮）是否能被操作
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.isCheckCD = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section["param1"]:
			self.isCheckCD = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		target = entity.monsterAIGetTargetEntity()
		if target is None:
			KBEDebug.ERROR_MSG("monster(%s) ai not set ai target!!"%entity.scriptID)
			return False
		if target.ammo > 0 and not target.operatorID:
			if self.isCheckCD:
				if target.cdEndTime > 0:
					return False
			
			return True
		return False

class AICondition101(AIConditionBase.AIConditionBase):
	"""
	判断是否和AI目标有否都有某buff
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.isTrue = 1
		self.buffIDs = []

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section["param1"]:
			self.isTrue =  int(section["param1"])
		if len(section["param2"]):
			self.buffIDs = [int(buffID) for buffID in section["param2"].split("|")]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		aiTargetEntity = entity.monsterAIGetTargetEntity()
		if not aiTargetEntity:
			return
		isSameBuff = False
		for buffID in self.buffIDs:
			if len( entity.findBuffsByBuffID(buffID) ) and len( aiTargetEntity.findBuffsByBuffID(buffID) ):
				isSameBuff = True
		if self.isTrue and isSameBuff:
			return True
		elif not self.isTrue and not isSameBuff:
			return True
		return False

class AICondition102(AIConditionBase.AIConditionBase):
	"""
	判断云梯的状态 （0:跟随 1:搭建 2:搭建完成）
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.ladderState = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section["param1"]:
			self.ladderState = int( section["param1"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.getAerialLadderState() == self.ladderState


class AICondition103(AIConditionBase.AIConditionBase):
	"""
	用于指定属性改变事件
	指定属性的值为指定的值
	暂时处理int str 判读 后续有别的类型需要再完善
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.propertyStr = section["param1"]
		self.value = section["param2"]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		propertyStr = args[0]
		value = args[1]
		if not propertyStr==self.propertyStr:
			return False

		if not hasattr(entity, self.propertyStr):
			KBEDebug.ERROR_MSG("param1 is invalid!")
			return False
			
		if isinstance(value, str):
			return value == self.value
		elif isinstance(value, int):
			try:
				return value == int(self.value)
			except Exception as err:
				KBEDebug.ERROR_MSG("param2 is invalid! err:%s"%err)
				return False
		
class AICondition104(AIConditionBase.AIConditionBase):
	"""
	判断是否有AI目标
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.monsterAIGetTargetEntity()
		
class AICondition105(AIConditionBase.AIConditionBase):
	"""
	判断是否没有AI目标
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return not entity.monsterAIGetTargetEntity()
		
class AICondition106(AIConditionBase.AIConditionBase):
	"""
	（火炮）能否开炮
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.minAttackDist = 10.0			# 最近攻击距离
		self.maxAttackDist = 120.0			# 最远攻击距离
		self.offsetRadian = 30.0				# 左右各偏移弧度


	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section["param1"]:
			self.minAttackDist = float( section["param1"])
		if section["param2"]:
			self.maxAttackDist = float( section["param2"])
		if section["param3"]:
			self.offsetRadian = float( section["param3"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetEntity = entity.monsterAIGetTargetEntity()
		if targetEntity:
			if targetEntity.isState(csdefine.ENTITY_STATE_DEAD) or targetEntity.isState(csdefine.ENTITY_STATE_PEAD):
				entity.monsterAISetTarget(0)				# 重新选择AI目标
				return False
			dist = entity.position.distTo( targetEntity.position)
			if dist < self.minAttackDist or dist > self.maxAttackDist:
				entity.monsterAISetTarget(0)
				return False
			if not csarithmetic.isInSector(targetEntity.position, entity.position, entity.initialDirection.z, self.maxAttackDist, self.offsetRadian * 2):
				entity.monsterAISetTarget(0)
				return False
		else:
			return False
		return entity.canAutoFire()


class AICondition107(AIConditionBase.AIConditionBase):
	"""
	某一范围内有指定entityType的scriptID,并且可以通过导航到达该位置的一定距离内
	如果没有填scriptID，则只判断范围内有没有指定类型的entity
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]
		self.distance = 1.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.entityType  = section["param2"]
		if section[ "param3" ].strip()!="":
			self.scriptIDs  = section["param3"].strip().split("|")
		if section[ "param4" ].strip()!="":
			self.removeStates  = [int(state) for state in section["param4"].strip().split("|")]
		if section[ "param5" ]:
			self.distance = float( section[ "param5" ])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs, self.removeStates )
		if len(entities) > 0 :
			for e in entities:
				pos = KBEngine.raycast( entity.spaceID, entity.layer, entity.position, e.position )[0]
				if e.position.flatDistTo( pos ) < self.distance:
					return True
		return False	

class AICondition108(AIConditionBase.AIConditionBase):
	"""
	某一范围内没有指定entityType的scriptID或无法通过导航走到entitiy位置的一定距离内
	如果没有填scriptID，则只判断范围内有没有指定类型的entity
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]
		self.distance = 1

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])

		self.entityType  = section["param2"]
		if section[ "param3" ].strip()!="":
			self.scriptIDs  = section["param3"].strip().split("|")
		if section[ "param4" ].strip()!="":
			self.removeStates  = [int(state) for state in section["param4"].strip().split("|")]
		if section[ "param5" ]:
			self.distance = float( section[ "param5" ])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs, self.removeStates )
		if len(entities) > 0 :
			for e in entities:
				pos = KBEngine.raycast( entity.spaceID, entity.layer, entity.position, e.position )[0]
				if e.position.flatDistTo( pos ) < self.distance:
					return False
		return True


class AICondition109(AIConditionBase.AIConditionBase):
	"""
	士兵列阵指令移动已完成
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return not entity.isCmdMoving

class AICondition110(AIConditionBase.AIConditionBase):
	"""
	判断是否移动到云梯位置
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.radiusDistance = 0.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.radiusDistance = float( section["param1"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		dstPos,entityID = entity.queryTemp("dstPosInfo")
		if dstPos == None:
			return False
		if entity.position.flatDistTo( dstPos ) <= self.radiusDistance:
			return True
		return False

class AICondition111(AIConditionBase.AIConditionBase):
	"""
	判断玩家是否给云梯发送AI命令
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.cmds = []

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.cmds = section[ "param1" ].split("|")

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if len(args) == 0:
			return False

		entityID, scriptID, cmd = args

		if cmd not in self.cmds:
			return False
		if entityID != entity.getFollowerID():
			return False

		return True

class AICondition112(AIConditionBase.AIConditionBase):
	"""
	判断将领带领的小兵数量
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.amount = 0
		self.relationFlags = [] #（0代表“=”，1代表“<” ，2代表“>”） 

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.amount = int( section["param1"] )
		self.relationFlags = [ int(i) for i in section["param2"].split("|") ]		#满足一个即可

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		amount = len(entity.getAllMember())
		for flag in self.relationFlags:
			if flag == 0 and amount == self.amount:
				return True
			if flag == 1 and amount < self.amount:
				return True
			if flag == 2 and amount > self.amount:
				return True
		return False

class AICondition113(AIConditionBase.AIConditionBase):
	"""
	判断将领伤害列表中士兵数量
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.amount = 0
		self.relationFlags = [] #（0代表“=”，1代表“<” ，2代表“>”） 

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.amount = int( section["param1"] )
		self.relationFlags = [ int(i) for i in section["param2"].split("|") ]		#满足一个即可

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		enemySoldiers = []
		for entityID in entity.damageList.keys():
			entity = KBEngine.entities.get( entityID, None )
			if entity and entity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
				enemySoldiers.append( entity )
		amount = len( enemySoldiers )
		for flag in self.relationFlags:
			if flag == 0 and amount == self.amount:
				return True
			if flag == 1 and amount < self.amount:
				return True
			if flag == 2 and amount > self.amount:
				return True
		return False

class AICondition114(AIConditionBase.AIConditionBase):
	"""
	判断将领带领士兵血量平均值
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.hpPercent = 0.0
		self.relationFlags = [] #（0代表“=”，1代表“<” ，2代表“>”） 

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.hpPercent = float( section["param1"] )
		self.relationFlags = [ int(i) for i in section["param2"].split("|") ]		#满足一个即可

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		memberDict = entity.getAllMember()
		amount = len(memberDict)
		totalHPPercent = 0.0
		for memberEntity in memberDict.values():
			totalHPPercent += float(memberEntity.HP) / memberEntity.HP_Max
		if totalHPPercent == 0.0:
			percent = 0.0
		else:
			percent = totalHPPercent / amount
		for flag in self.relationFlags:
			if flag == 0 and percent == self.hpPercent:
				return True
			if flag == 1 and percent < self.hpPercent:
				return True
			if flag == 2 and percent > self.hpPercent:
				return True
		return False

class AICondition115(AIConditionBase.AIConditionBase):
	"""
	判断将领找到的最近点是否存在
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.isHasBarracks = False

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section["param1"]:
			self.isHasBarracks = bool( int(section["param1"]) )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		isFind = False
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_GCZ:
			barracksID = entity.queryTemp( "barracksID","")
			if barracksID and spaceEntity.getRecordNotOccupyBarracks( barracksID ) != None:
				isFind = True
		return self.isHasBarracks == isFind

class AICondition116(AIConditionBase.AIConditionBase):
	"""
	判断将领带领的兵种
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.scriptID = ""

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.scriptIDs = section["param1"].split("|")

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		memberDict = entity.getAllMember()
		for memberEntity in memberDict.values():
			if memberEntity.scriptID in self.scriptIDs:
				return True
			else:
				return False
		return False

class AICondition117(AIConditionBase.AIConditionBase):
	"""
	判断将领某个范围内的士兵数量
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.amount = 0
		self.relationFlags = [] #（0代表“=”，1代表“<” ，2代表“>”） 
		self.radius = 0.0
		self.entityType = ""

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.amount = int( section["param1"] )
		self.relationFlags = [ int(i) for i in section["param2"].split("|") ]		#满足一个即可
		self.radius = float( section["param3"] )
		self.entityType = section["param4"]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtForAI( self.radius, csconst.AI_ENTITIES_IN_RANGE_HEIGHT, self.entityType )
		amount = len( entities )
		for flag in self.relationFlags:
			if flag == 0 and amount == self.amount:
				return True
			if flag == 1 and amount < self.amount:
				return True
			if flag == 2 and amount > self.amount:
				return True
		return False

class AICondition118(AIConditionBase.AIConditionBase):
	"""
	判断将领某个范围内的士兵的血量百分比
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.hpPercent = 0.0
		self.relationFlags = [] #（0代表“=”，1代表“<” ，2代表“>”） 
		self.radius = 0.0
		self.entityType = ""

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.hpPercent = float( section["param1"] )
		self.relationFlags = [ int(i) for i in section["param2"].split("|") ]		#满足一个即可
		self.radius = float( section["param3"] )
		self.entityType = section["param4"]

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		entities = entity.entitiesInRangeExtForAI( self.radius, csconst.AI_ENTITIES_IN_RANGE_HEIGHT, self.entityType )
		amount = len( entities )
		totalHPPercent = 0.0
		for e in entities:
			totalHPPercent += float(e.HP) / e.HP_Max
		if totalHPPercent == 0.0:
			percent = 0.0
		else:
			percent = totalHPPercent / amount
		for flag in self.relationFlags:
			if flag == 0 and percent == self.hpPercent:
				return True
			if flag == 1 and percent < self.hpPercent:
				return True
			if flag == 2 and percent > self.hpPercent:
				return True
		return False


class AICondition119(AIConditionBase.AIConditionBase):
	"""
	判断目标与自身位置高度的差异
	参数一：目标与自身高度对比 正数表示高于，负数表示低于
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.distance = 0.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.distance = float( section["param1"] )


	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetEntity = KBEngine.entities.get(entity.getTargetID(), None)
		if targetEntity:
			if self.distance<0:
				return entity.position.y - targetEntity.position.y <= self.distance
			elif self.distance>0:
				return entity.position.y - targetEntity.position.y >= self.distance
		return False


class AICondition120(AIConditionBase.AIConditionBase):
	"""
	判断攻击目标类型
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.entityFlag = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.entityFlag = int( section["param1"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			return False
		if targetEntity.getEntityFlag() != self.entityFlag:
			return False
		return True

class AICondition121(AIConditionBase.AIConditionBase):
	"""
	怪物血量累计变化（只能配置在血量改变事件中，需要行为AIAction287清除怪物累计血量）
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.value = 0
		self.isAdd = False

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.value = float( section["param1"])
		if section["param2"]:
			self.isAdd = bool(int( section["param2"]))

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if self.isAdd:
			value = entity.queryTemp( "MonsterHPAddValue", 0 )
			if value >= int(self.value * entity.HP_Max):
				return True
			else:
				value += max(0, args[0]-args[1])
				entity.setTemp( "MonsterHPAddValue", value )
		else:
			value = entity.queryTemp( "MonsterHPSubValue", 0 )
			if value >= int(self.value * entity.HP_Max):
				return True
			else:
				value += max(0, args[1]-args[0])
				entity.setTemp( "MonsterHPSubValue", value )
		return False


class AICondition122(AIConditionBase.AIConditionBase):
	"""
	判断自身主动反应陷阱中玩家数量与将领数量的差值是否为某值
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.value = 0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.value = int( section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		roleList = []
		cmderList = []
		proximityID = entity.findProximityByUserArg( ECBProximityDefine.PROXIMITY_AI_INITIATIVE_1 )
		if proximityID in entity.shapeProximityEnters:
			entityIDList = entity.shapeProximityEnters[proximityID]
			for id in entityIDList:
				e = KBEngine.entities.get(id, None)
				if not e:
					continue
				if e.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE:
					roleList.append(id)
				if e.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_COMMANDER:
					cmderList.append(id)

			return (len(roleList) - len(cmderList))==self.value
		return False

class AICondition123(AIConditionBase.AIConditionBase):
	"""
	判断指定scriptID的对象占领度是否大于某值
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.scriptID = ""
		self.percent = 0.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.scriptID = section["param1"]
		self.percent = float( section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		s = entity.getCurrentSpace()
		idList = s.getEntityRecord(self.scriptID)
		if not len(idList):
			return False
		e = KBEngine.entities.get(idList[0], None)
		if not e:
			return False
		return e.getOccurProgress()>self.percent


class AICondition124(AIConditionBase.AIConditionBase):
	"""
	指定区域是否有将领
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.scriptID = ""
		self.bValue = False

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.scriptID = section["param1"]
		self.bValue = bool(section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		s = entity.getCurrentSpace()
		idList = s.getEntityRecord(self.scriptID)
		
		for id in idList:
			e = KBEngine.entities.get(id, None)
			if e:
				proximityID = e.findProximityByUserArg( ECBProximityDefine.PROXIMITY_AI_INITIATIVE_1 )
				if proximityID in e.shapeProximityEnters:
					entityIDList = e.shapeProximityEnters[proximityID]
				for id in entityIDList:
					entity = KBEngine.entities.get(id, None)
					if not entity:
						continue
					if entity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_COMMANDER:
						return self.bValue == True
						
		return self.bValue == False


class AICondition125(AIConditionBase.AIConditionBase):
	"""
	判断与目标关系
	参数一：1:友好，2:敌对，3:中立，4:无关系
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.dstRelation = csdefine.COMBAT_RELATION_DEFAULT

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.dstRelation = int( section["param1"] )


	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return entity.queryRelation( triggerEntity ) == self.dstRelation
		

class AICondition126(AIConditionBase.AIConditionBase):
	"""
	玩家是否成功添加物品
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.itemID = 0
		self.num = 1

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.itemID = int( section["param1"] )
		self.num = int( section["param2"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if triggerEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			result, itemInst = triggerEntity.addItemByID( self.itemID, self.num, csdefine.ITEM_ADD_BY_MONSTER_AI )
			if result != csstatus.ITEM_GO_ON:
				triggerEntity.statusMessage( result, "" )
			else:
				return True
		return False

class AICondition127(AIConditionBase.AIConditionBase):
	"""
	移动类型变换
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.oldMoveType = int( section["param1"])
		self.newMoveType = int( section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if self.oldMoveType == args[0] and self.newMoveType == args[1]:
			return True
		return False

class AICondition128(AIConditionBase.AIConditionBase):
	"""
	是否处于在停止移动中
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if entity.moveControlID == 0:
			return True
		return False


class AICondition129(AIConditionBase.AIConditionBase):
	"""
	攻城战 是否处于在停止移动中
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if entity.moveScriptID == csdefine.MOVE_TYPE_STOP:
			return True
		return False

class AICondition130(AIConditionBase.AIConditionBase):
	"""
	攻城战 指令移动完成类型是否为指定类型
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.moveScriptID = csdefine.MOVE_TYPE_SOLDIER_FOLLOW

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.moveScriptID = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		moveScriptID = args[0]
		if self.moveScriptID == moveScriptID:
			return True
		return False

class AICondition131(AIConditionBase.AIConditionBase):
	"""
	是否是 攻方(守方)
	0:攻方，1：守方
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.belongSide = csdefine.BELONG_SIDE_ATTACK

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.belongSide = int(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		return triggerEntity.isBelongSide( self.belongSide)

class AICondition132(AIConditionBase.AIConditionBase):
	"""
	是否是 挑战洞府的玩家
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		if triggerEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			if entity.belongDBID and entity.belongDBID == triggerEntity.challengeDBID:
				return True
		return False

class AICondition133(AIConditionBase.AIConditionBase):
	"""
	范围内，是否有攻（守）方玩家
	0:攻方，1：守方
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self.radius = float(section["param1"])
		self.belongSide = int( section["param2"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity:
			for player in spaceEntity._spaceRoles:
				if player.isBelongSide( self.belongSide ):
					if entity.position.flatDistTo( player.position ) <= self.radius:
						return True
		return False

class AICondition134(AIConditionBase.AIConditionBase):
	"""
	判断玩家不在跳跃状态情况下怪物是否不能寻路到玩家所在位置
	"""

	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )
		self.distance = 1.0

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		if section["param1"]:
			self.distance = float(section["param1"])

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		targetEntity = KBEngine.entities.get(entity.getTargetID(), None)
		if targetEntity:
			if not targetEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
				return False
			if targetEntity.jumpShowState != csdefine.JUMP_SHOW_STATE_STAND:
				return False
			targetPos = Math.Vector3(targetEntity.position)
			path = entity.navigatePathPoints(targetPos, 0xFFFF, entity.layer, 0xFFFF)
			if path:
				navTargetPos = path[-1]
				if navTargetPos.distTo(targetPos) <= max(self.distance, 1.0):
					return False
		return True

class AICondition135(AIConditionBase.AIConditionBase):
	"""
	判断仇恨值最高者，是否比当前目标的仇恨值高多少个百分比
	"""
	def __init__( self, aiID ):
		"""
		初始化
		"""
		AIConditionBase.AIConditionBase.__init__( self, aiID )

	def initData( self ,section):
		"""
		virtual method
		@param  section:	存储的数据字段
		@type 	section:	PyDataSection
		"""
		AIConditionBase.AIConditionBase.initData(self, section )
		self._percent = float( section["param1"] )

	def check( self, ai, entity, args, triggerEntity ):
		"""
		virtual method
		@param ai: 	拥有此条件的ai (做此支持是为了得到或写AI的动态数据)
		@type  ai:  AI of instance,AIBase
		@param entity: 执行此AIConditon的entity
		@type  entity：entity
		"""
		value = entity.hatredList.get( entity.getTargetID(), 0 )
		if not value:
			return True
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			return False

		maxID = 0
		maxValue = 0
		hatredDatas = sorted(entity.hatredList,key=lambda x:entity.hatredList[x], reverse = True)		
		for id in hatredDatas:
			maxDamEntity = KBEngine.entities.get( id )
			if maxDamEntity and maxDamEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
				continue
			if entity.monsterAIIsCanAttackUseID(id):
				maxID = id
				maxValue = entity.hatredList[id]
				break
		if maxID == entity.getTargetID():
			return False
		percent = (maxValue - value) * 100 / value
		if percent <= self._percent:
			return False
		return True



AIConditionBase.AIConditionBase.setConditionClass( "AICondition1", AICondition1 )
AIConditionBase.AIConditionBase.setConditionClass( "AICondition2", AICondition2 )
AIConditionBase.AIConditionBase.setConditionClass( "AICondition3", AICondition3 )
AIConditionBase.AIConditionBase.setConditionClass( "AICondition4", AICondition4 )
AIConditionBase.AIConditionBase.setConditionClass( "AICondition5", AICondition5 )
AIConditionBase.AIConditionBase.setConditionClass( "AICondition6", AICondition6 )
AIConditionBase.AIConditionBase.setConditionClass( "AICondition7", AICondition7 )
AIConditionBase.AIConditionBase.setConditionClass( "AICondition8", AICondition8 )
AIConditionBase.AIConditionBase.setConditionClass( "AICondition9", AICondition9 )
AIConditionBase.AIConditionBase.setConditionClass( "AICondition10", AICondition10)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition11", AICondition11)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition12", AICondition12)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition13", AICondition13)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition14", AICondition14)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition15", AICondition15)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition16", AICondition16)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition17", AICondition17)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition18", AICondition18)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition19", AICondition19)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition20", AICondition20)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition21", AICondition21)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition22", AICondition22)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition23", AICondition23)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition24", AICondition24)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition25", AICondition25)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition26", AICondition26)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition27", AICondition27)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition28", AICondition28)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition29", AICondition29)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition30", AICondition30)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition31", AICondition31)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition32", AICondition32)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition33", AICondition33)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition34", AICondition34)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition35", AICondition35)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition36", AICondition36)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition37", AICondition37)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition38", AICondition38)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition39", AICondition39)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition40", AICondition40)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition41", AICondition41)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition42", AICondition42)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition43", AICondition43)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition44", AICondition44)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition45", AICondition45)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition46", AICondition46)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition47", AICondition47)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition48", AICondition48)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition49", AICondition49)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition50", AICondition50)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition51", AICondition51)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition52", AICondition52)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition53", AICondition53)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition54", AICondition54)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition55", AICondition55)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition56", AICondition56)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition57", AICondition57)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition58", AICondition58)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition59", AICondition59)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition60", AICondition60)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition61", AICondition61)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition62", AICondition62)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition63", AICondition63)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition64", AICondition64)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition65", AICondition65)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition66", AICondition66)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition67", AICondition67)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition68", AICondition68)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition69", AICondition69)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition70", AICondition70)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition71", AICondition71)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition72", AICondition72)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition73", AICondition73)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition74", AICondition74)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition75", AICondition75)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition76", AICondition76)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition77", AICondition77)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition78", AICondition78)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition79", AICondition79)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition80", AICondition80)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition81", AICondition81)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition82", AICondition82)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition83", AICondition83)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition84", AICondition84)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition85", AICondition85)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition86", AICondition86)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition87", AICondition87)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition88", AICondition88)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition89", AICondition89)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition90", AICondition90)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition91", AICondition91)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition92", AICondition92)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition93", AICondition93)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition94", AICondition94)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition95", AICondition95)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition96", AICondition96)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition97", AICondition97)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition98", AICondition98)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition99", AICondition99)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition100", AICondition100)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition101", AICondition101)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition102", AICondition102)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition103", AICondition103)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition104", AICondition104)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition105", AICondition105)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition106", AICondition106)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition107", AICondition107)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition108", AICondition108)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition109", AICondition109)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition110", AICondition110)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition111", AICondition111)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition112", AICondition112)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition113", AICondition113)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition114", AICondition114)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition115", AICondition115)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition116", AICondition116)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition117", AICondition117)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition118", AICondition118)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition119", AICondition119)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition120", AICondition120)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition121", AICondition121)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition122", AICondition122)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition123", AICondition123)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition124", AICondition124)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition125", AICondition125)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition126", AICondition126)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition127", AICondition127)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition128", AICondition128)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition129", AICondition129)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition130", AICondition130)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition131", AICondition131)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition132", AICondition132)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition133", AICondition133)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition134", AICondition134)
AIConditionBase.AIConditionBase.setConditionClass( "AICondition135", AICondition135)
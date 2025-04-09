# -*- coding: utf-8 -*-
import Math
import math
import random
import Functions
# 用于AI动作的拓展
from ConfigObject.MonsterAI.AIBase import AIActionBase
import KBEDebug
import Const
import csdefine
import FightRuleMgr
import KBEngine
import KBEMath
import csarithmetic
import time
import csstatus
from ConfigObject import PatrolRouteLoader
import Functions
import csconst
import XinMoSkillConfig
import MonsterModelNumberCopyPlayer
import ECBProximityDefine
import ConfigObject.Skill.SkillLoader as SkillLoader
from ConfigObject.Drop.DropBase import DropMgr
from ConfigObject.MonsterEscapePointLoader import g_MonsterEscapePoint
import KST

mapping = {
				1:"Role",
				2:"Space",
				3:"Monster",
				4:"NPC",
				9:"VehiclePet"
		}

SIGN_ENTITY_ID = "SIGN_ENTITY_ID_"

class AIAction1(AIActionBase.AIActionBase):
	"""
	移动到某个坐标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.movePosition = []
		self.faceMovement = True
		self.moveType = csdefine.MOVE_TYPE_NORMAL
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		position = Functions.vector3TypeConvert( section["param1"] )
		if position is None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
		else:
			self.movePosition = KBEMath.Unreal2KBEnginePosition( position )
		if section["param2"]:
			self.faceMovement = bool(int(section["param2"]))
		if section["param3"].strip():
			self.moveSpeed = float(section["param3"].strip())


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
		
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)

		moveArgs = [ Math.Vector3(self.movePosition),0.0,self.faceMovement,True ]
		entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )



class AIAction2(AIActionBase.AIActionBase):
	"""
	在一个范围随机移动
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.range = 0
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.range = int(section["param1"])
		if section["param2"].strip():
			self.moveSpeed = float(section["param2"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.range <= 0:
			KBEDebug.WARNING_MSG("AIAction2 randomWalkRange <=0 ")
			return

		randomPoint = Functions.getRandomMovePoint( Math.Vector3(entity.spawnPos),Math.Vector3( entity.position ),0,self.range )
		if randomPoint and len(randomPoint) > 0:
			behType = csdefine.BEHAVIOUR_TYPE_MOVING
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
			(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
			moveArgs = [ Math.Vector3(randomPoint) ]
			entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )
		else:
			KBEDebug.WARNING_MSG("spaceID = %s , id = %s can't get randomPoint"%(entity.getCurrentSpaceScriptID(),entity.scriptID))

class AIAction3(AIActionBase.AIActionBase):
	"""
	切换状态
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._newAIState = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._newAIState = int(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self._newAIState != 0 and entity.monsterAIGetCurSubState() != self._newAIState:
			entity.monsterAIChangeSubState(self._newAIState)

class AIAction4(AIActionBase.AIActionBase):
	"""
	对攻击目标使用技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.spellSkillID = 0  # 使用自身配置的技能，对应AIUseSkills配置表
		self.priorityLevel = csdefine.BEHAVIOUR_COMMON
		
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.spellSkillID = int(section["param1"])
		if not self.checkSkillIsExit( self.spellSkillID ):
			self.spellSkillID = 0
			
		if len(section["param2"]):
			self.priorityLevel = int( section["param2"] )
			
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.spellSkillID:
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.spellSkillID, entity.getTargetID(),False])
		else:
			KBEDebug.WARNING_MSG("entity %d not config spellSkillID %s" % (entity.id, self.spellSkillID))

class AIAction5(AIActionBase.AIActionBase):
	"""
	将一定范围内离自己最近的指定entity作为AI目标
	如果不填参数scriptID,则不进行此参数的判断，只进行类型的判断
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.entityType = section[ "param2" ]
		if section["param3"].strip()!="":
			self.scriptIDs = section["param3"].strip().split("|")
		if section["param4"].strip()!="":
			self.removeStates = [int(state) for state in section["param4"].strip().split("|")]
		


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		eid = 0
		distance = 10000.0
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs,self.removeStates )
		for e in entities:													# 选择最近目标的ID
			if e.hasEffectState( csdefine.EFFECT_STATE_HIDE ):continue		# 隐身单位不能选择
			dis = entity.position.flatDistTo(e.position)
			if distance > dis:
				eid = e.id
				distance = dis

		e = KBEngine.entities.get( eid,None )
		if e and e.getState() != csdefine.ENTITY_STATE_DEAD:
			entity.monsterAISetTarget( eid )

class AIAction6(AIActionBase.AIActionBase):
	"""
	回走到出生点
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.faceMovement = True
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.faceMovement = bool(section["param1"])
		if section["param2"].strip():			
			self.moveSpeed = float(section["param2"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		moveArgs = [ Math.Vector3(entity.spawnPos) ]
		entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )

class AIAction7(AIActionBase.AIActionBase):
	"""
	跳回默认AI状态
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.AIChangeState(entity.AIGetDefaultState())

class AIAction8(AIActionBase.AIActionBase):
	"""
	把伤害最高的entity设置成攻击目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		damageDatas = sorted(entity.damageList,key=lambda x:entity.damageList[x], reverse = True)
		for id in damageDatas:
			maxDamEntity = KBEngine.entities.get( id )
			if maxDamEntity and maxDamEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
				continue
			if id == entity.getTargetID():
				return
		
			if entity.monsterAIIsCanAttackUseID(id):
				entity.setTargetID(id)
				return

class AIAction9(AIActionBase.AIActionBase):
	"""
	重置某行为
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.behaviourType = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.behaviourType = int(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.AIBControlReset(self.behaviourType)

class AIAction10(AIActionBase.AIActionBase):
	"""
	向指定entity发送AI指令
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptIDs = []
		self.commandID = ""
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.commandID = section["param3"]
		if section["param2"].strip()!="":
			self.scriptIDs = section["param2"].strip().split("|")
		if section["param4"].strip()!="":
			self.removeStates = [int(state) for state in section["param4"].strip().split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.commandID:
			entitys = entity.entitiesInRangeExtForAI(self.radius, self.height, None, self.scriptIDs, self.removeStates )
			for e in entitys:
				if not e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
					entity.monsterAISendCommand(e.id, self.commandID)

class AIAction11(AIActionBase.AIActionBase):
	"""
	把当前AI目标加入敌人列表
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get( entity.monsterAIGetTarget(), None )
		if targetEntity:
			if entity.canBuildEnemyRelation(targetEntity) :
				FightRuleMgr.g_fightMgr.buildEnemyRelation( entity, targetEntity)

class AIAction12(AIActionBase.AIActionBase):
	"""
	播放动作
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.actionName = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.actionName = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.allClients.CLIENT_OnPlayAction(self.actionName,-1.0)

class AIAction13(AIActionBase.AIActionBase):
	"""
	将最先进入敌人列表的作为攻击目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		enemyDatas = sorted(entity.enemyList.items(), key = lambda asd:asd[1] )
		for id, time in enemyDatas:
			enemy = KBEngine.entities.get( id )
			if enemy and enemy.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
				continue
				
			entity.setTargetID(id)
			return

class AIAction14(AIActionBase.AIActionBase):
	"""
	改变AI目标为攻击目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get( entity.monsterAIGetTarget(), None )
		if targetEntity:
			if targetEntity.id in entity.enemyList:
				entity.setTargetID(targetEntity.id)
				return
			if entity.canBuildEnemyRelation(targetEntity):
				if targetEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):return
				FightRuleMgr.g_fightMgr.buildEnemyRelation( entity, targetEntity)
				entity.setTargetID(targetEntity.id)

class AIAction15(AIActionBase.AIActionBase):
	"""
	呼叫同伴
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		#如果自身处于呼叫状态中，则不能呼叫别人
		if entity.callSign:
			KBEDebug.DEBUG_MSG("entity id = %d is called,can't call others!"%entity.id)
			return
		else:
			entity.callSign = True

		es = entity.entitiesInRangeExtForAI(entity.getScript().getCallRange(), csconst.AI_ENTITIES_IN_RANGE_HEIGHT, "Monster" )
		for e in es:
			if e.scriptID in entity.getScript().getCallList():
				e.onFightCall( entity.getTargetID())

class AIAction16(AIActionBase.AIActionBase):
	"""
	对自身使用技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.spellSkillID = 0
		self.priorityLevel = csdefine.BEHAVIOUR_COMMON

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		skillID= int(section["param1"])
		if self.checkSkillIsExit( skillID ):
			self.spellSkillID = skillID
			
		if len(section["param2"]):
			self.priorityLevel = int( section["param2"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.spellSkillID:
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.spellSkillID, entity.id,False], self.priorityLevel )

class AIAction17(AIActionBase.AIActionBase):
	"""
	记录当前时间（如记录则不进行再次记录）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.timeTag = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.timeTag = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not self.timeTag in entity.monsterAITimeTag:
			entity.monsterAITimeTag[self.timeTag] = 0
			entity.monsterAITimeTag[self.timeTag] = time.time()

class AIAction18(AIActionBase.AIActionBase):
	"""
	清除记录时间
	|分隔，可同时清除多个
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.timeTag =[]

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.timeTag = section["param1"].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		for tag in self.timeTag:
			if tag in entity.monsterAITimeTag:
				entity.monsterAITimeTag.pop(tag)

class AIAction19(AIActionBase.AIActionBase):
	"""
	将一定范围内指定entity加入敌人列表
	如果是monster/npc并且填了scriptID,则需要进行scriptID的判断，
	否则不进行scriptID的判断
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.entityType = section["param2"]
		if section["param3"].strip()!="":
			self.scriptIDs = section["param3"].strip().split("|")
		if section["param4"].strip()!="":
			self.removeStates = [int(state) for state in section["param4"].strip().split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		tempRadius = self.radius
		if self.radius > entity.viewRange:
			KBEDebug.ERROR_MSG("AIAction19 entity id = %d scriptID = %s aiID = %d search radius(%d) > viewRange(%d) "%( entity.id,entity.scriptID,ai.getID(),self.radius,entity.viewRange))
			tempRadius = entity.viewRange
			
		entities = entity.entitiesInRangeExtForAI(tempRadius, self.height, self.entityType,self.scriptIDs,self.removeStates )

		for e in entities:
			if entity.canBuildEnemyRelation(e):
				FightRuleMgr.g_fightMgr.buildEnemyRelation( entity, e)


class AIAction20(AIActionBase.AIActionBase):
	"""
	死亡
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.changeState(csdefine.ENTITY_STATE_DEAD)

class AIAction21(AIActionBase.AIActionBase):
	"""
	清除一组EAI标记
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.eaiIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.eaiIDs = section["param1"].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		for e in self.eaiIDs:
			if entity.monsterAIHasEAI(int(e)):
				entity.monsterAIRemoveEAI(int(e))


class AIAction22(AIActionBase.AIActionBase):
	"""
	设置当前位置为出生点
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.parent:
			entity.spawnPos = Math.Vector3(entity.localPosition)
		else:
			entity.spawnPos = Math.Vector3(entity.position)

class AIAction23(AIActionBase.AIActionBase):
	"""
	在指定位置刷出一个entity
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptID = ""
		self.position = None
		self.direction = None
		self.isSetLevel = 0 			#是否按照当前entity的等级进行设置新刷出来的NPC

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.scriptID = section["param1"]
		
		if section["param2"].strip() != "":
			position = Functions.vector3TypeConvert( section["param2"] )
			if position is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param2(%s)" %( self.getAIID(), section["param2"] ) )
			else:
				self.position = KBEMath.Unreal2KBEnginePosition( position )
			
		if section["param3"].strip() != "":
			direction = Functions.vector3TypeConvert( section["param3"] )
			if direction is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param3(%s)" %( self.getAIID(), section["param3"] ) )
			else:
				self.direction = KBEMath.Unreal2KBEngineDirection( direction )
			
		if section["param4"]:
			self.isSetLevel = int(section["param4"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.position == None:
			targetPosition = Math.Vector3(entity.position)
		else:
			targetPosition = self.position
		if self.direction == None:
			targetDirection = Math.Vector3(entity.direction)
		else:
			targetDirection = self.direction

		newEntity = None
		if not self.isSetLevel:
			newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(targetPosition), targetDirection,{ "spawnPos":Math.Vector3( targetPosition ),"spawnDir":targetDirection})
		else:
			newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(targetPosition), targetDirection,{"level":entity.level,"spawnPos":Math.Vector3( targetPosition ),"spawnDir":targetDirection})
		if not newEntity:
			KBEDebug.WARNING_MSG("AIActions23 scriptID = %s is not exist!"%self.scriptID)

class AIAction24(AIActionBase.AIActionBase):
	"""
	停止巡逻
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.isMovingType(csdefine.MOVE_TYPE_PATROL):
			entity.stopMoving( csdefine.MOVE_TYPE_PATROL )

class AIAction25(AIActionBase.AIActionBase):
	"""
	向当前副本或位面记录的指定entity发送AI指令
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptIDS = []
		self.commandID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.scriptIDS = section["param1"].split("|")
		self.commandID = section["param2"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if len(self.scriptIDS) > 0:
			for ids in self.scriptIDS:
				entitiesIDS = entity.getCurrentSpace().getEntityRecord(ids)
				for e in entitiesIDS:
					entities = KBEngine.entities.get(e, None)
					if entities:
						entity.monsterAISendCommand(entities.id, self.commandID)

class AIAction26(AIActionBase.AIActionBase):
	"""
	改变自身朝向
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.direction = None

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		direction = Functions.vector3TypeConvert( section["param1"] )
		if direction is None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
		else:
			self.direction = KBEMath.Unreal2KBEngineDirection( direction )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.hasFlag( csdefine.FLAG_CANT_ROTATE ):
			return
		if self.direction != None:
			entity.changeDirection(self.direction, csdefine.REASON_CHANGE_DIR_VOLUNTARY)
		else:
			KBEDebug.DEBUG_MSG("AIActions26 direction format is error--%s"%self.direction)

class AIAction27(AIActionBase.AIActionBase):
	"""
	改变自身朝向至指定范围内的指定entity
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptID = ""
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.angularVelocity = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.entityType = section["param2"]
		self.scriptID = section["param3"]
		if len( section["param4"] ):
			self.angularVelocity = float(section["param4"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.hasFlag( csdefine.FLAG_CANT_ROTATE ):
			return
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType )
		direction = Math.Vector3()
		if self.angularVelocity == 0.0:
			for e in entities:
				v = e.position-entity.position
				if not self.entityType == "Role":
					if e.scriptID == self.scriptID:
						direction = (0.0,0.0,csarithmetic.getYawByVector3( v ))
						break
				else:
					direction = (0.0,0.0,csarithmetic.getYawByVector3( v ))
					break
			entity.changeDirection(direction, csdefine.REASON_CHANGE_DIR_VOLUNTARY)
		else:
			for e in entities:
				if not self.entityType == "Role":
					if e.scriptID == self.scriptID:
						entity.allClients.CLIENT_SimulationCircle( self.angularVelocity, e.id )
						break
				else:
					entity.allClients.CLIENT_SimulationCircle( self.angularVelocity, e.id )
					break


class AIAction28(AIActionBase.AIActionBase):
	"""
	设置最低血量百分比
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.minHpPercent = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.minHpPercent = float(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.setMinHPPercent( self.minHpPercent )
		entity.setOldMinHPPercent( self.minHpPercent )

class AIAction29(AIActionBase.AIActionBase):
	"""
	怪物非战斗状态下销毁
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not entity.getState() == csdefine.ENTITY_STATE_FIGHT:
			entity.delayDestroy( 0.1 )

class AIAction30(AIActionBase.AIActionBase):
	"""
	一定范围内的玩家显示界面并播放语音
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.voiceID = ""
		self.questID = 0
		self.questStatusList = []
		self.questTargetList = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.voiceID = section["param2"]
		if len(section["param3"]):
			self.questID = int(section["param3"])
		self.questStatusList = section["param4"].split("|")
		if len(section["param5"]):
			self.questTargetList = section["param5"].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.radius > 0:
			entities = entity.entitiesInRangeExtForAI(self.radius, self.height, "Role" )
			if not self.questID:
				for e in entities:
					entity.monsterAIShowMessagePlaySound(e, self.voiceID)
				return True

			if len(self.questTargetList):
				for e in entities:
					result = True
					for questTarget in self.questTargetList:
						quest = questTarget.split(":")
						if len(quest) > 1:
							targetStatus = e.queryTaskStatus(self.questID, int(quest[0]))
							if not targetStatus == int(quest[1]):
								result = False
								continue
						else:
							KBEDebug.ERROR_MSG("AICondition20 param5 is error")
							return False
					if result:
						entity.monsterAIShowMessagePlaySound(e, self.voiceID)	
			else:
				for e in entities:
					questStatus = str(e.queryQuestStatus(self.questID))
					if questStatus in self.questStatusList:
						entity.monsterAIShowMessagePlaySound(e, self.voiceID)		

					

class AIAction31(AIActionBase.AIActionBase):
	"""
	AI目标玩家显示界面并播放语音
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.voiceID = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.voiceID = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get(entity.monsterAIGetTarget(),None)
		if targetEntity and targetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and targetEntity.getState() != csdefine.ENTITY_STATE_PEAD \
		and targetEntity.getState() != csdefine.ENTITY_STATE_DEAD and not targetEntity.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):
			entity.monsterAIShowMessagePlaySound(targetEntity, self.voiceID)

class AIAction32(AIActionBase.AIActionBase):
	"""
	自身销毁
	如果没有填时间参数，则默认8秒
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.delaySecond = Const.NPC_DESTORY_SELF

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section[ "param1" ]:
			second = float(section["param1"])
			if second > 0:
				self.delaySecond = second

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.delayDestroy(self.delaySecond)

class AIAction33(AIActionBase.AIActionBase):
	"""
	清空敌人列表
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.resetEnemyList()

class AIAction34(AIActionBase.AIActionBase):
	"""
	对AI目标使用技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.spellSkillID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		skillID = int(section["param1"])
		if self.checkSkillIsExit( skillID ):
			self.spellSkillID = skillID

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.spellSkillID:
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.spellSkillID, entity.monsterAIGetTarget(),False])
		else:
			KBEDebug.WARNING_MSG("entity scriptID %s not config spellSkillID%s" % (entity.scriptID, self.spellSkillID))

class AIAction35(AIActionBase.AIActionBase):
	"""
	触发AI目标自己对自己使用技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.spellSkillID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.spellSkillID = int(section["param1"])
		if not self.checkSkillIsExit( self.spellSkillID ):
			self.spellSkillID = 0

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.spellSkillID:
			AIEntity = KBEngine.entities.get(entity.monsterAIGetTarget(),None)
			if AIEntity :
				if not AIEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
					AIEntity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.spellSkillID, entity.monsterAIGetTarget(),False])
				else:
					AIEntity.useSkillToEntity(self.spellSkillID, AIEntity.id)
		else:
			KBEDebug.WARNING_MSG("entity scriptID %s not config spellSkillID%s" % (entity.scriptID, self.spellSkillID))

class AIAction36(AIActionBase.AIActionBase):
	"""
	触发一定范围内所有玩家完成某一个事件目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.questID = 0
		self.questTargetID = 0
		#self.questTargetCount = 1

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.questID = int(section["param2"])
		self.questTargetID = int(section["param3"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, "Role" )
		for e in entities:
			e.questTaskIncreaseState(self.questID,self.questTargetID)

class AIAction37(AIActionBase.AIActionBase):
	"""
	触发AI目标完成某一个事件目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.questID = 0
		self.questTargetID = 0
		self.questTargetCount = 1

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.questID = int(section["param1"])
		self.questTargetID = int(section["param2"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get(entity.monsterAIGetTarget(),None)
		if targetEntity.getState() != csdefine.ENTITY_STATE_PEAD and targetEntity.getState() != csdefine.ENTITY_STATE_DEAD and \
		not targetEntity.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):  #玩家未决状态下与死亡状态下不会完成任务
			targetEntity.questTaskIncreaseState(self.questID, self.questTargetID)

class AIAction38(AIActionBase.AIActionBase):
	"""
	增加标志位
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.flags = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.flags = section["param1"].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		for flag in self.flags:
			if not entity.hasFlag(int(flag)):
				entity.addFlag(int(flag))

class AIAction39(AIActionBase.AIActionBase):
	"""
	移除标志位
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.flags = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.flags = section["param1"].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		for flag in self.flags:
			if entity.hasFlag(int(flag)):
				entity.removeFlag(int(flag))

class AIAction40(AIActionBase.AIActionBase):
	"""
	param1为任务ID，如果填了此参数则表示与任务相关，如果没有填则与任务无关，主要用于AI目标玩家是否被执行过当前AI
	任务相关：
			在AI目标玩家身上记录当前任务ID与aiid，当该任务ID重置或者放弃时清除该任务ID下保存的数据
	任务无关：
			在自身数据记录aiid与玩家DBID
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.questID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.questID = int(section[ "param1" ])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		aiTargetEntity = KBEngine.entities.get( entity.monsterAIGetTarget(), None )
		if not aiTargetEntity or not aiTargetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			return
		if  aiTargetEntity.getState() == csdefine.ENTITY_STATE_PEAD or aiTargetEntity.getState() == csdefine.ENTITY_STATE_DEAD and \
		aiTargetEntity.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):  #玩家未决状态下与死亡状态下不会完成任务
			return
			
		if self.questID:
			aiid = int(str(entity.scriptID)+str(ai.getID()))
			aiTargetEntity.addQuestRecordAIIDS(self.questID,aiid)
		else:
			entity.monsterAIMarkRoleForAIID(ai.getID(),aiTargetEntity.playerDBID)

class AIAction41(AIActionBase.AIActionBase):
	"""
	指定巡逻路线上的最近点巡逻
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.route = -1
		self.pointIndex = 0
		self.isOnGround = 0
		self.isFaceTo = 1
		self.accVelocity = 0.0
		self.moveSpeed = 0.0
		self.patrolMoveSpeedMax = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if len(section[ "param1" ]):
			strList = section["param1"].split("|")
			self.route = int(strList[0])
			if len(strList)>1:
				self.pointIndex = int(strList[1])
				
		strList = section["param2"].split("|")
		if len(strList) >= 1:
			self.isOnGround = int(strList[ 0 ])
		if len(strList) >= 2:
			self.isFaceTo = int(strList[ 1 ])
		
		if section["param3"]:	#加速度
			self.accVelocity = float(section["param3"])
		if section["param4"].strip():
			self.moveSpeed = float(section["param4"].strip())
		if section["param5"].strip():
			self.patrolMoveSpeedMax = float(section["param5"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		route = self.route if self.route!= -1 else entity.patrolRoute
		pointIndex = 0
		patrolRouteInfo = entity.getCurrentSpacePatrolnfo( route )
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		if 0 != self.pointIndex:
			spaceEntity = entity.getCurrentSpace()
			if not spaceEntity:
				return
			routeData = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute(spaceEntity.scriptID, route)
			if routeData:
				routePoints = PatrolRouteLoader.g_patrolRouteLoader.getRoutePoints(routeData)
				if self.pointIndex in routePoints:
					pointIndex = self.pointIndex
				else:
					KBEDebug.ERROR_MSG("routPoint = %d not in route = %d"%(self.pointIndex, route))
					return
		else:
			nearestPoint = PatrolRouteLoader.g_patrolRouteLoader.getNearestRoutePoint(entity.getCurrentSpaceScriptID(), route,Math.Vector3(entity.position))
			if nearestPoint:
				pointIndex = nearestPoint
			else:
				KBEDebug.ERROR_MSG("AIActions41 can't find nearestPoint!")
				return
		entity.patrolRoute = route
		entity.patrolMoveSpeedMax = self.patrolMoveSpeedMax
		if self.isOnGround:
			#贴地使用导航进行移动
			if self.isFaceTo:
				faceType = csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION
			else:
				faceType = csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION_NOT_FACE
			entity.startPatrol(moveSpeed, isUpdateSpeed, (patrolRouteInfo, pointIndex, faceType, self.accVelocity))
		else:
			#补贴地则不使用导航进行移动，直接移动到目标点
			if self.isFaceTo:
				faceType = csdefine.MOVE_PATROL_MOVE_GOTO_POSITION
			else:
				faceType = csdefine.MOVE_PATROL_MODE_GOTO_POSITION_NOT_FACE
			entity.startPatrol(moveSpeed, isUpdateSpeed, (patrolRouteInfo, pointIndex, faceType, self.accVelocity))
				

class AIAction42(AIActionBase.AIActionBase):
	"""
	对攻击目标使用一组技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.skillIDs = []  								#技能索引列表

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		skillList = [ int( skillID ) for skillID in section["param1"].split("|") ]
		for skillID in skillList:
			if  self.checkSkillIsExit( skillID ):
				self.skillIDs.append( skillID )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spellList = []
		for spellSkillID in self.skillIDs:
			if spellSkillID:
				tempList = [spellSkillID, entity.getTargetID(),True]
				spellList.append(tempList)

		if len(spellList):
			entity.behAdds(csdefine.BEHAVIOUR_TYPE_SPELL, spellList,csdefine.BEHAVIOUR_LOOP)
		else:
			KBEDebug.WARNING_MSG("AIAction42 entity id = %d, scriptID = %s has no skill"%(entity.id, entity.scriptID))

class AIAction43(AIActionBase.AIActionBase):
	"""
	清除自身某些buff
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)	
		if len(section["param1"]):
			self.buffIDs = [int(x) for x in section["param1"].split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not len(self.buffIDs):
			entity.removeAllBuff()
			return

		for buffID in self.buffIDs:
			entity.removeBuffByID( buffID )

class AIAction44(AIActionBase.AIActionBase):
	"""
	清除目标身上某些buff
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)	
		if len(section["param1"]):
			self.buffIDs = [int(x) for x in section["param1"].split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get( entity.monsterAIGetTarget(), None )
		if not targetEntity:
			return
		if not len(self.buffIDs):
			targetEntity.removeAllBuff()
			return

		for buffID in self.buffIDs:
			targetEntity.removeBuffByID( buffID )	

class AIAction45(AIActionBase.AIActionBase):
	"""
	在战斗列表中随机选取一个敌人作为当前目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)		

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.enemyList:			
			enemyIDList = []
			for enemyID in entity.enemyList.keys():
				enemyIDList.append(enemyID)
		
			targetID = enemyIDList[ random.randint(0,len(enemyIDList)-1)]
			targetEntity = KBEngine.entities.get( targetID, None )

			if targetEntity:
				entity.monsterAISetTarget( targetID )
				return

class AIAction46(AIActionBase.AIActionBase):
	"""
	改变自身模型
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.model = ""
		self.scale = 1.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.model = section["param1"].strip()
		self.scale = float(section["param2"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.setExtraModelNumber( self.model )
		entity.setModelScale( self.scale )

class AIAction47(AIActionBase.AIActionBase):
	"""
	跟随当前目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )	
		if section["param1"].strip():
			self.moveSpeed = float(section["param1"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			KBEDebug.ERROR_MSG("targetEntity is not exist")
			return
		randomDistance = random.uniform(Const.CHASE_ENTITY_RANGE[0],Const.CHASE_ENTITY_RANGE[1])
		
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
			
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		moveArgs = [ Math.Vector3(targetEntity.position), randomDistance ]
		entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )

class AIAction48(AIActionBase.AIActionBase):
	"""
	以某个坐标为中心(如果没有指定则表示以自身为中心），在一定范围内(圆内或者圆上)随机召唤数个entity。 位置随机，entity类型可以是monster，npc,陷阱
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.isJudge = []
		self.centerPos = None	#param1 中心点坐标	
		self.radius = 0.0 		#param2	指定半径
		self.isAtTheCircle = False #param3 是否在圆上
		self.isHasFlag = False  #param3是否是浮空召唤
		self.number = 0 		#param4	entity的数量
		self.scriptID = ""		#param5	entity的scriptID

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )	
		if not section["param1"].strip():
			self.centerPos = None
		else:
			position = Functions.vector3TypeConvert( section["param1"] )
			if position is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
			else:
				self.centerPos = KBEMath.Unreal2KBEnginePosition( position )
		
		self.radius = float(section[ "param2" ])

		if len(section["param3"]):
			self.isJudge = [int(x) for x in section["param3"].split("|")]
			self.isAtTheCircle = bool(int(self.isJudge[0]))
			if len(self.isJudge) > 1:
				self.isHasFlag = bool(int(self.isJudge[1]))

		self.number = int( section[ "param4" ] )

		self.scriptID = section[ "param5" ]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""

		def getRandPosInCircle( centerPos, radius, num, entity ):
			"""
			在圆内获得随机点坐标
			"""
			posList = []
			while num:
				x = centerPos[2]+random.uniform(-1,1)*radius
				y = centerPos[0]+random.uniform(-1,1)*radius
				posList.append(Math.Vector3( y, entity.position[1], x ))
				num-=1
			return posList

		def getRandPosAtTheCircle( centerPos, radius, num, entity ):
			"""
			在圆边缘上获得随机点坐标
			"""
			PIE = 3.1415926
			radian = PIE*2/num
			posList = []
			while num:
				x = centerPos[2]+radius*math.cos(radian*num)
				y = centerPos[0]+radius*math.sin(radian*num)
				posList.append(Math.Vector3( y, entity.position[1], x ))
				num-=1
			return posList

		posList = []
		if not self.centerPos:
			centerPos = Math.Vector3( entity.position )
		else:
			centerPos = Math.Vector3( self.centerPos )
		if self.isAtTheCircle:
			posList = getRandPosAtTheCircle( centerPos, self.radius, self.number, entity )
		else:
			posList = getRandPosInCircle( centerPos, self.radius, self.number, entity )
		
		targetDirection = Math.Vector3(0.0, 0.0, entity.direction.z)
		for targetPosition in posList:
			tarPosition = KBEngine.collideVertical( entity.spaceID, entity.layer, targetPosition, 10, - 10 )
			if self.isHasFlag:
				newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(targetPosition), targetDirection,{ "spawnPos":Math.Vector3( targetPosition ) ,"spawnDir":Math.Vector3( targetDirection )})
			elif tarPosition:
				newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(tarPosition[0]), targetDirection,{ "spawnPos":Math.Vector3( tarPosition[0] ) ,"spawnDir":Math.Vector3( targetDirection )})

class AIAction49(AIActionBase.AIActionBase):
	"""
	将敌人列表中离自己最远的指定entity作为攻击目标
	Param1：entityType
	Param2：scriptID 选填，若不填则不进行scriptID的判断

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.eType = section["param1"]
		self.scriptID = section["param2"]
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		

		maxDis = 0.0
		targetEntity = None
		if self.scriptID == "":
			for key in entity.enemyList:
				tEntity = KBEngine.entities.get( int(key),None )
				if tEntity and mapping[tEntity.getEntityFlag()] == self.eType:
					if maxDis < entity.position.flatDistTo( tEntity.position ):
						if tEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):continue
						maxDis = entity.position.flatDistTo( tEntity.position )
						targetEntity = tEntity
		else:
			for key in entity.enemyList:
				tEntity = KBEngine.entities.get( int(key),None )
				if tEntity and mapping[tEntity.getEntityFlag()] == self.eType and tEntity.getScriptID() == self.scriptID:
					if maxDis < entity.position.flatDistTo( tEntity.position ):
						if tEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):continue
						maxDis = entity.position.flatDistTo( tEntity.position )
						targetEntity = tEntity			
		if targetEntity:
			entity.targetID = targetEntity.id

class AIAction50(AIActionBase.AIActionBase):
	"""
	重新指定怪物出生点
	param1：position，以空格分隔
	param2：direction，以空格分隔
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = None
		self.direction = None

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"].strip()=="" and  section["param2"].strip()=="":
			KBEDebug.ERROR_MSG("you must fill in at least one param!")
			return
		position = Functions.vector3TypeConvert( section["param1"] )
		if position==None and section["param1"].strip() != "":
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
		if position!=None:
			self.position = KBEMath.Unreal2KBEnginePosition( position )

		direction = Functions.vector3TypeConvert( section["param2"] )
		if direction==None and section["param2"].strip() != "":
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param2(%s)" %( self.getAIID(), section["param2"] ) )
		if direction!=None:
			self.direction = KBEMath.Unreal2KBEngineDirection( direction )


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		
		if self.position!=None:
			entity.spawnPos = Math.Vector3(self.position)
		if self.direction!=None:	
			entity.spawnDir = Math.Vector3(self.direction)

class AIAction51(AIActionBase.AIActionBase):
	"""
	将一定范围内的所有玩家传送到某个地图的某个位置
	Param1：半径，单位米
	Param2：地图名
	Param3：position，以空格分隔
	Param4：direction，以空格分隔

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = None
		self.direction = None
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.spaceScriptID = section["param2"]
		position = Functions.vector3TypeConvert( section["param3"] )
		if not position:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param3(%s)" %( self.getAIID(), section["param3"] ) )
		else:
			self.position = KBEMath.Unreal2KBEnginePosition( position )

		direction = Functions.vector3TypeConvert( section["param4"] )
		if direction==None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param4(%s)" %( self.getAIID(), section["param4"] ) )
		else:
			self.direction = KBEMath.Unreal2KBEngineDirection( direction )


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, "Role" )
		if self.position == None or self.direction == None :
			return	
		for e in entities:
			e.gotoSpace(self.spaceScriptID, self.position, self.direction )



class AIAction52(AIActionBase.AIActionBase):
	"""
	将单个玩家（AI目标）传送到某个地图的某个位置
	Param1：地图名
	Param2：position，以空格分隔
	Param3：direction，以空格分隔

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = None
		self.direction = None

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

		self.spaceScriptID = section["param1"]
		position = Functions.vector3TypeConvert( section["param2"] )
		if not position:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param2(%s)" %( self.getAIID(), section["param2"] ) )
		else:
			self.position = KBEMath.Unreal2KBEnginePosition( position )

		direction = Functions.vector3TypeConvert( section["param3"] )
		if  direction==None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param3(%s)" %( self.getAIID(), section["param3"] ) )
		else:
			self.direction = KBEMath.Unreal2KBEngineDirection( direction )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		
		targetEntity = entity.monsterAIGetTargetEntity()
		if not targetEntity:
			return
		if targetEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		if self.position == None or self.direction == None:
			return
		targetEntity.gotoSpace(self.spaceScriptID, self.position, self.direction)


class AIAction53(AIActionBase.AIActionBase):
	"""
	改变朝向为出生时的朝向

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		
		if entity.direction.z != entity.spawnDir.z:					# 降低服务器与客户端传输
			direction = Math.Vector3(entity.spawnDir)
			entity.changeDirection(direction, csdefine.REASON_CHANGE_DIR_VOLUNTARY)
			


class AIAction54(AIActionBase.AIActionBase):
	"""
	将敌人列表中离自己最近的指定entity作为攻击目标
	Param1：entityType
	Param2：选填，若不填则不进行scriptID的判断

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.eType = section["param1"]
		self.scriptID = section["param2"].strip()
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		

		minDis = 10000.0
		targetEntity = None
		if self.scriptID == "":
			for key in entity.enemyList:
				tEntity = KBEngine.entities.get( int(key),None )
				if tEntity and (mapping[tEntity.getEntityFlag()] == self.eType or self.eType == ""):
					if minDis > entity.position.flatDistTo( tEntity.position ):
						if tEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):continue
						minDis = entity.position.flatDistTo( tEntity.position )
						targetEntity = tEntity
		else:
			for key in entity.enemyList:
				tEntity = KBEngine.entities.get( int(key),None )
				if tEntity and (mapping[tEntity.getEntityFlag()] == self.eType or self.eType == "") and tEntity.getScriptID() == self.scriptID:
					if minDis > entity.position.flatDistTo( tEntity.position ):
						if tEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):continue
						minDis = entity.position.flatDistTo( tEntity.position )
						targetEntity = tEntity			
		if targetEntity:
			entity.targetID = targetEntity.id


class AIAction55(AIActionBase.AIActionBase):
	"""
	设置标记
	Param1：支持填写多个，以竖号分隔，表示且的关系

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.signs = set(section["param1"].strip().split("|"))

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		
		entity.signs = entity.signs|self.signs


class AIAction56(AIActionBase.AIActionBase):
	"""
	移除标记
	Param1：支持填写多个，以竖号分隔，表示且的关系

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.signs = set(section["param1"].strip().split("|"))

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		
		entity.signs = entity.signs-self.signs

class AIAction57(AIActionBase.AIActionBase):
	"""
	中断当前正在释放的技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		entity.interruptSkill( csstatus.SKILL_AI_INTERRUPT )
		
class AIAction58(AIActionBase.AIActionBase):
	"""
	开始怪物的随机移动/巡逻
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"].strip():
			self.moveSpeed = float(section["param1"].strip())
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		if entity.patrolRoute: #有配巡逻路径的不会随机移动
			entity.startPatrol(moveSpeed,isUpdateSpeed)
		else:
			entity.startRandomWalk(moveSpeed,isUpdateSpeed)

class AIAction59(AIActionBase.AIActionBase):
	"""
	给副本发送通知
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.key = section["param1"]	#string类型
		self.exceptValue = section["param2"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity and (entity.isInSpaceCopy() or entity.isInSpacePlane()):
			spaceEntity.getScript().onConditionChange( spaceEntity, "AI", entity.scriptID, self.key, self.exceptValue )
			KBEDebug.DEBUG_MSG("AI notify space condition change. entity id:%s. "%entity.id, spaceEntity.id, self.key )

class AIAction60(AIActionBase.AIActionBase):
	"""
	切换到自由状态
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )


	def do(self, ai, entity, triggerEntity):
		entity.changeState(csdefine.ENTITY_STATE_FREE)

class AIAction61(AIActionBase.AIActionBase):
	"""
	切换到表演状态
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )


	def do(self, ai, entity, triggerEntity):
		entity.changeState(csdefine.ENTITY_STATE_SHOW)

class AIAction62(AIActionBase.AIActionBase):
	"""
	播放动作
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.actionID = ""
		self.playTime = 0.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.actionID = section["param1"]
		if self.actionID.strip() == "":
			KBEDebug.ERROR_MSG("param1 is None")
		self.playTime = float(section["param2"].strip())
				
	def do(self, ai, entity, triggerEntity):
		if not self.actionID:
			return
		entity.addTimerCallBack( 0.2, 'playAdmissionAction', ( self.actionID, ))
		entity.addTimerCallBack( 0.2 + self.playTime, 'setIsPlayAdmissionAction', (False,) )


class AIAction63(AIActionBase.AIActionBase):
	"""
	将一定范围内的随机一名玩家作为AI目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
	
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, "Role" )
		if len( entities ) == 0:
			return
		e = random.choice( entities )
		entity.monsterAISetTarget( e.id )

class AIAction64(AIActionBase.AIActionBase):
	"""
	新增AI行为：随机选择以自身为圆心的环形范围内的位置为目标释放技能。需要配置的参数有：
	param1：较小半径，float
	param2：较大半径，float
	param4：技能ID。	int

	PS：param1和param2可填相同数值
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius1 = 0.0
		self.radius2 = 0.0
		self.skillID = 0
	
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.radius1 = float(section[ "param1" ])
		self.radius2 = float(section[ "param2" ])
		useSkillID = int(section[ "param3" ])
		if self.checkSkillIsExit( useSkillID ):
			self.skillID = useSkillID

	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.radius1 == 0.0 or self.radius2 == 0.0 or self.skillID == 0:
			KBEDebug.ERROR_MSG("please check your param IsValid!")
			return
		minR = min(self.radius1,self.radius2)
		maxR = max(self.radius1,self.radius2)
		radius = random.uniform( minR, maxR )
		angel = random.uniform( 0, math.pi*2 )
		posX = radius*math.cos( angel )+entity.position.x
		posY = entity.position.y
		posZ = radius*math.sin( angel )+entity.position.z
		targetPosition = Math.Vector3( posX,posY,posZ )
		entity.useSkillToPosition( self.skillID, targetPosition )

class AIAction65(AIActionBase.AIActionBase):
	"""
	指定位置，朝向（默认为本身位置，朝向），创建一个与当前目标玩家外形一样，技能一样的心魔类型怪物
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = None
		self.direction = None
		self.scriptID = None

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		
		position = Functions.vector3TypeConvert( section["param1"] )
		if position:
			self.position = KBEMath.Unreal2KBEnginePosition( position )

		direction = Functions.vector3TypeConvert( section["param2"] )
		if direction:
			self.direction = KBEMath.Unreal2KBEngineDirection( direction )
		
		self.scriptID = section["param3"].strip()

	def do(self, ai, entity, triggerEntity):

		position = self.position or Math.Vector3(entity.position)
		direction = self.direction or Math.Vector3(entity.direction)

		targetEntity = KBEngine.entities.get(entity.monsterAIGetTarget(),None)
		if not targetEntity:
			return

		def getXinMoSkills( skillIDList ):
			"""
			通过带对表替换相应技能
			"""
			attrSkills = []
			skillData = XinMoSkillConfig.datas
			for skillID in skillIDList:
				if skillID not in skillData:
					#KBEDebug.ERROR_MSG("skillID = %s is not in XinMoSkillConfig.datas"%skillID)
					continue
				attrSkills.append(skillData[skillID])
			return attrSkills

		tmpAttrSkills = getXinMoSkills(targetEntity.attrSkills)
		param = {}
		param.update( {"ownerID":targetEntity.id} )
		param.update( {"spawnPos":tuple(Math.Vector3(targetEntity.position))} )
		param.update( {"spawnDir":tuple(Math.Vector3(0.0, 0.0, targetEntity.direction.z))} )
		param.update( {"level":targetEntity.level} )
		param.update( {"attrSkills":tmpAttrSkills} )

		if MonsterModelNumberCopyPlayer.datas.get("MonsterExtXinMo",None):
			modelNumber =  MonsterModelNumberCopyPlayer.datas["MonsterExtXinMo"][targetEntity.getGender()][targetEntity.getCamp()][targetEntity.getProfession()]
			param.update( {"modelNumber":modelNumber} )
		else:
			KBEDebug.ERROR_MSG("MonsterModelNumberCopyPlayer config is not has MonsterExtXinMo")
		newEntity = entity.createMonster( self.scriptID, position, direction, param )

		if not newEntity:
			KBEDebug.ERROR_MSG("createMonster failed!")

class AIAction66(AIActionBase.AIActionBase):
	"""
	对攻击目标使用自身技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		targetEntity = KBEngine.entities.get(entity.getTargetID(),None)
		if not targetEntity:
			return
		spellList = []
		for spellSkillID in entity.attrSkills:
			if spellSkillID:
				tempList = [spellSkillID, entity.getTargetID(),True]
				spellList.append(tempList)

		if len( entity.attrSkills ):
			entity.behAdds(csdefine.BEHAVIOUR_TYPE_SPELL, spellList,csdefine.BEHAVIOUR_LOOP)
		else:
			KBEDebug.WARNING_MSG(" entity id = %d, scriptID = %s has no skill"%(entity.id, entity.scriptID))

class AIAction67(AIActionBase.AIActionBase):
	"""
	怪物对攻击目标随机使用一个攻击技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.skillIDs = []
		self.priorityLevel = csdefine.BEHAVIOUR_COMMON

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if len(section["param1"].strip()):
			tSkillIDs = [ int( skillID ) for skillID in section["param1"].strip().split("|") ]
			for skillID in tSkillIDs:
				if self.checkSkillIsExit( skillID ):
					self.skillIDs.append( skillID )

	def do(self, ai, entity, triggerEntity):

		if not len(self.skillIDs):
			KBEDebug.ERROR_MSG("skillIDs is []")
			return
		skillIDs = list( self.skillIDs )
		for skillID in self.skillIDs:
			result	= entity.monsterAIIsCanUseSkillToTarget( skillID )  and \
				entity.behaviours[2].isCanAddBehavior( entity,[ skillID, entity.id,False], self.priorityLevel )
			if not result:
				skillIDs.remove( skillID )
			
		if entity.lastRandomSkillID in skillIDs:
			skillIDs.remove( entity.lastRandomSkillID )

		if not len(skillIDs):
			return
		skillID = random.choice( skillIDs )
			
		entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [ skillID, entity.getTargetID(),False])

class AIAction68(AIActionBase.AIActionBase):
	"""
	从当前位置跳到指定位置
	1、原地跳出，播放出场动作。				不配参数
	2、跳出到指定坐标，播放出场动作。		param1：指定坐标
	3、跳出到指定坐标周围，播放出场动作。	param1：指定坐标，param3：范围,float,米
	4、跳出到AI目标周围，播放出场动作。 	param2：填1表示指定位置为AI目标位置，param3

	param1: 坐标，必填 三种方式 一 填 0：表示当前坐标；二 填 1 表示指定坐标为AI目标的坐标 三 填指定坐标；
	param2: 范围：必填
	param3: 动作ID 必填
	param4: 动作播放时间 必填
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = None
		self.distanceTable = None        #( rMin, rMax )
		self.actionID = None
		self.playTime = None

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if not len( section["param1"] ):
			KBEDebug.ERROR_MSG("param1 is None!")
			return
		if not len( section["param2"] ):
			KBEDebug.ERROR_MSG("param2 is None!")
			return
		if not len(section["param3"]):
			KBEDebug.ERROR_MSG("param3 is None")
			return
		if not len(section["param4"].strip()):
			KBEDebug.ERROR_MSG("param4 is None")
			return
		
		self.position = section["param1"]
		
		self.distanceTable = tuple(map(float,section["param2"].strip().split('|')))

		self.actionID = section["param3"].strip()

		self.playTime = float(section["param4"])

	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not self.position  or not self.actionID or not self.playTime:
			return
		isChangeDir = True
		if self.position == "0":
			isChangeDir = False
			targetPosition = Math.Vector3( entity.position )
		elif self.position == "1":
			targetEntity = entity.monsterAIGetTargetEntity()
			if not targetEntity:
				KBEDebug.ERROR_MSG("entity.id = %s: monsterAITarget is None!"%entity.id)
				return		
			targetPosition = Math.Vector3( targetEntity.position )
		else:
			targetPosition = Functions.vector3TypeConvert( self.position )
			if not targetPosition:
				KBEDebug.ERROR_MSG("param1 is invalid!")
				return
			targetPosition = Math.Vector3(KBEMath.Unreal2KBEnginePosition(targetPosition))


		rMin = self.distanceTable[0]
		rMax = self.distanceTable[1]
		if rMin<0 or rMin > rMax or rMax<0:
			KBEDebug.ERROR_MSG( "rMin = %f,rMax = %f,param2  is invalid!"%(rMin,rMax) )
			return	
		r = random.uniform( rMin, rMax )
		angle = random.uniform( -3.14,3.14 )


		targetPosition = (targetPosition.x + r*math.cos(angle), targetPosition.y, targetPosition.z + r*math.sin(angle))
		
		playTime = self.playTime
		actionID = self.actionID

		entity.monsterShow( actionID, playTime, targetPosition, isChangeDir )

class AIAction69(AIActionBase.AIActionBase):
	"""
	随从怪跟随归属玩家
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.minDist = 3.0
		self.maxDist = 20.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		if hasattr( entity, 'owner' ):
			master = KBEngine.entities.get( entity.owner.id, None )
			if not master:
				return
				
			entity.monsterExtCallChaseOwner(self.minDist,self.maxDist)
			return
		
		if hasattr( entity, "ownerID" ):
			entity.monsterExtCallChaseOwner(self.minDist,self.maxDist)

class AIAction70(AIActionBase.AIActionBase):
	"""
	播放一组动作
	param1: 动作ID，用'|'分隔
	param2: 时间，用'|'分隔
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.actionIDs = []
		self.delayTimes = []

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.actionIDs = section["param1"].strip().split('|')
		self.delayTimes = [ float(t) for t in section["param2"].strip().split('|')]

				
	def do(self, ai, entity, triggerEntity):
		entity.playGroupActions( self.actionIDs, self.delayTimes )
		
class AIAction71(AIActionBase.AIActionBase):
	"""
	释放技能或者远离
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.oddList = []		#释放技能的概率:远离的概率:游走的概率
		self.backDist = 1.0
		self.moveSpeed = 2.0
		self.spellSkillIDs = []
		self.skillLastCount = 5.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if len(section["param1"].strip()):
			self.oddList = section["param1"].strip().split("|")
		if len( self.oddList ) > 0 and len( self.oddList ) < 2:
			self.oddList.append( str( 1 - float( self.oddList[0] ) ) )
		self.backDist = float( section["param2"] )
		self.moveSpeed = float( section["param3"] )
		if len(section["param4"].strip()):
			skillIDs = [ int(skillID) for skillID in section["param4"].strip().split("|") ]
			isConfigTrue = True
			for skillID in skillIDs:
				if not self.checkSkillIsExit( skillID ):
					isConfigTrue = False
			
			if isConfigTrue:
				self.spellSkillIDs = skillIDs
				
		if len(section["param5"].strip()):
			self.skillLastCount = float(section["param5"].strip())
		

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			return
			
		targetPosition = Math.Vector3( targetEntity.position )
		if not len(self.spellSkillIDs):
			KBEDebug.ERROR_MSG("skillIDs is []")
			return
				
		skillIDs = list( self.spellSkillIDs )
		if entity.lastRandomSkillID in skillIDs:
			skillIDs.remove( entity.lastRandomSkillID )
		if len(skillIDs) <= 0:
			return
		skillID = random.choice( skillIDs )
		
		if entity.monsterAISkillLastTime > 0 and (Functions.getTime() - entity.monsterAISkillLastTime)/csconst.TIME_ENLARGE_MULTIPLE < self.skillLastCount:
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [skillID, entity.getTargetID(), False ] )
			return
		randOdd = random.random()
		if randOdd < float( self.oddList[0] ):
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [skillID, entity.getTargetID(), False ] )
			entity.monsterAISkillLastTime = Functions.getTime()
		elif randOdd < float( self.oddList[0] ) + float( self.oddList[1] ) and randOdd >= float( self.oddList[0] ):
			entity.moveAwayFromTarget( targetPosition, self.moveSpeed, False, self.backDist )
			entity.monsterAISkillLastTime = 0
		else:
			entity.walkAroundTarget( entity.getTargetID(), targetPosition, math.pi*3/4, self.moveSpeed, False )
		
class AIAction72(AIActionBase.AIActionBase):
	"""
	靠近或者游走
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.odds = 0.5		#靠近的概率
		self.moveDist = 2.0
		self.moveSpeed = 2.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.odds = float( section["param1"] )
		self.moveDist = float( section["param2"] )
		self.moveSpeed = float( section["param3"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			return
			
		targetPosition = Math.Vector3( targetEntity.position )
		#entities = entity.entitiesInRangeExtForAI(entity, 0.2, "Monster")
		#if len(entities) > 0 and random.random() < 0.7:
		#	entity.walkAroundTarget( targetPosition, self.moveSpeed )
		#else:
		randOdd = random.random()
		if randOdd < self.odds:
			entity.moveNearToTarget( targetPosition, self.moveSpeed, False, self.moveDist )
			KBEDebug.DEBUG_MSG("moveNearToTarget")
		else:
			entity.walkAroundTarget( entity.getTargetID(), targetPosition, math.pi/2, self.moveSpeed, False )
			KBEDebug.DEBUG_MSG("walkAroundTarget")

class AIAction73(AIActionBase.AIActionBase):
	"""
	跟随当前目标到一定范围内
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.chaseDist = 0.0
		self.moveSpeed = 0.0
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.chaseDist = float( section["param1"] )
		if section["param2"].strip():
			self.moveSpeed = float(section["param2"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			KBEDebug.ERROR_MSG("targetEntity is not exist")
			return
		chaseDist = random.uniform(self.chaseDist - 0.5, self.chaseDist - 0.1)
		
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
		
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		moveArgs = [ Math.Vector3(targetEntity.position), chaseDist ]
		entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )


		
class AIAction74(AIActionBase.AIActionBase):
	"""
	将一定范围内持有特定Buff的entity作为AI目标
	param1：半径，单位米；
	param2：BuffID，支持多个，以竖号分隔，表示且；
	param3：类型；
	param4：选填，若存在多个选择距离自身最近的一个。

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.buffIDs = []
		self.entityTypes = None
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]
	
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])

		self.buffIDs =  [int(buffID) for buffID in section["param2"].strip().split("|")]
		if section["param3"].strip():
			self.entityTypes = section["param3"].strip().split("|")
		if section["param4"].strip()!="":
			self.scriptIDs = section["param4"].strip().split("|")
		if section["param5"].strip()!="":
			self.removeStates = [int(state) for state in section["param5"].strip().split("|")]

	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entities = []
		if  self.entityTypes == None:
			entities = entity.entitiesInRangeExtForAI(self.radius, self.height, None, self.scriptIDs,self.removeStates )
		else:
			for entityType in self.entityTypes:
				entities += entity.entitiesInRangeExtForAI(self.radius, self.height, entityType, self.scriptIDs,self.removeStates )
		if not len(entities):
			return False
		AITargetEntity = None
		minDist = 100000000

		for e in entities:
				isHasBuffIDs = True
				for buffID in self.buffIDs:
					if not len(e.findBuffsByBuffID( buffID )):
						isHasBuffIDs = False
						break
				if isHasBuffIDs:
					if e.position.flatDistTo( entity.position ) < minDist:
						AITargetEntity = e

		if AITargetEntity:
			entity.monsterAISetTarget( AITargetEntity.id )


class AIAction75(AIActionBase.AIActionBase):
	"""
	增加自身身上的Buff
	
	param1：BuffID，支持多个，以竖号分隔，表示且；


	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""

		for buffID in self.buffIDs:
			entity.addBuff( entity, buffID )


class AIAction76(AIActionBase.AIActionBase):
	"""
	增加目标身上的Buff
	
	param1：BuffID，支持多个，以竖号分隔，表示且；


	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		AITargetEntity = entity.monsterAIGetTargetEntity()
		if not AITargetEntity:
			return
		for buffID in self.buffIDs:
			AITargetEntity.addBuff( entity, buffID )


class AIAction77(AIActionBase.AIActionBase):
	"""
	清空敌人列表（强制脱战）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.resetEnemyList()

class AIAction78(AIActionBase.AIActionBase):
	"""
	改变自身名字
	param1：uname
	"""

	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.uname = ""

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.uname = section["param1"].strip()

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.setUname( self.uname )


class AIAction79(AIActionBase.AIActionBase):
	"""
	设置最近巡逻点为出生点
	param1：巡逻路线ID

	"""

	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.route = -1

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.route = int(section["param1"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.spawnRoute = self.route

class AIAction80(AIActionBase.AIActionBase):
	"""
	脱离表演状态
	param1 配置脱离表演状态后需要切换的状态，如果不填则自动切换

	"""

	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.newState = csdefine.ENTITY_STATE_FREE
		self.isResetSpawPos = True

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if  section["param1"].strip():
			self.newState = int(section["param1"].strip())
		if section["param2"].strip():
			self.isResetSpawPos = int(section["param2"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.isResetSpawPos:
			entity.setSpawnPos(entity.position)

		if len(entity.enemyList):
			entity.changeState( csdefine.ENTITY_STATE_FIGHT )
		else:
			if self.newState == csdefine.ENTITY_STATE_FREE or self.newState == csdefine.ENTITY_STATE_RESET:
				entity.changeState( self.newState )
				return
			KBEDebug.ERROR_MSG("param Error:scriptID = %s,  AIID(%s) param2 must 1 or 5" %(entity.scriptID, self.getAIID() ))
			entity.changeState(csdefine.ENTITY_STATE_FREE)

class AIAction81(AIActionBase.AIActionBase):
	"""
	心魔将拥有者设置为攻击目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		tEntity = KBEngine.entities.get( entity.ownerID )
		if tEntity and tEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
			return
		entity.setTargetID( entity.ownerID )

class AIAction82(AIActionBase.AIActionBase):
	"""
	心魔对拥有者释放蛊惑技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.spellSkillID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.spellSkillID = int(section["param1"])
		if not self.checkSkillIsExit( self.spellSkillID ):
			self.spellSkillID = 0

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		owner = KBEngine.entities.get( entity.ownerID, None )
		if owner:
			if self.spellSkillID:
				entity.behAdd( csdefine.BEHAVIOUR_TYPE_SPELL, [self.spellSkillID, entity.ownerID, False] )
			else:
				KBEDebug.WARNING_MSG("entity scriptID %s not config spellSkillID%s" % (entity.scriptID, self.spellSkillID))

class AIAction83(AIActionBase.AIActionBase):
	"""
	延迟脱离准备状态
	"""

	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.delayTime = 1.0                                 #延迟时间
		self.newState = csdefine.ENTITY_STATE_MAX            #新状态


	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"].strip() != "":
			self.delayTime = float(section["param1"])
		else:
			self.delayTime = 1.0
		if section["param2"].strip() != "":
			self.newState = int(section["param2"].strip())
		else:
			self.newState = csdefine.ENTITY_STATE_MAX

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.monsterAIQuitPeadTimeID:
			entity.popTimer(entity.monsterAIQuitPeadTimeID)

		if self.delayTime<0:
			return
			
		if self.newState>csdefine.ENTITY_STATE_PEAD and self.newState<csdefine.ENTITY_STATE_MAX:
			entity.monsterAIQuitPeadTimeID = entity.addTimerCallBack( self.delayTime, "changeState", (self.newState,) )
			return
		else:
			if len(entity.enemyList):
				newState = csdefine.ENTITY_STATE_FIGHT
			else:
				newState = csdefine.ENTITY_STATE_FREE

		if entity.monsterAIQuitPeadTimeID:
			entity.popTimer(entity.monsterAIQuitPeadTimeID)
		
		entity.monsterAIQuitPeadTimeID = entity.addTimerCallBack( self.delayTime, "onMonsterAIQuitPeadCB", () )
		return

class AIAction84(AIActionBase.AIActionBase):
	"""
	随机切换子状态
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._isSpawnShuijin = False

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		subStateIDList = entity.monsterAIGetCurGroupStateObj().getSubStatesID()
		if len(subStateIDList) < 2:
			return
		enterSubStateID = random.randint(0,len(subStateIDList) - 1)
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity and entity.isInSpaceCopy():
			entityList = spaceEntity.getEntityRecord( entity.scriptID )
			if len(entityList) == 1 and not self._isSpawnShuijin:
				self._isSpawnShuijin = True
				entity.monsterAIChangeSubState(subStateIDList[1])
				return
		if enterSubStateID == 0:
			return
		if self._isSpawnShuijin and len(subStateIDList) > 2:
			enterSubStateID = random.randint(2,len(subStateIDList) - 1)
		if enterSubStateID == 1 and entity.isInSpaceCopy():
			self._isSpawnShuijin = True
		entity.monsterAIChangeSubState(subStateIDList[enterSubStateID])

class AIAction85(AIActionBase.AIActionBase):
	"""
	在该怪物位置创建一个怪物
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._entityID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._entityID = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.createEntityByScriptID(self._entityID,entity.position, Math.Vector3(0.0, 0.0, entity.direction.z), { "spawnPos": entity.position })

class AIAction88(AIActionBase.AIActionBase):
	"""
	怪物出场跳向指定坐标
	param1 actions 三段跳动作列表 |隔开
	param2 targetPos 目标坐标点
	param3 distanceTable 范围
	param4 jumpSpeed  跳跃速度 gravity 重力加速度 actionTime 起跳动作时间
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.actions = []
		self.targetPos = None
		self.distanceTable = []
		self.jumpSpeed = -1.0
		self.gravity = -1.0
		self.actionTime = -1.0
		self.direction = None
		self.effectIDs = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.actions = section["param1"].strip().split("|")
		if len(self.actions)!=3:
			KBEDebug.ERROR_MSG("AIAction88 param1 is invalid!")

		targetPos = section["param2"].strip().split("|")[0]
		targetPos = Functions.vector3TypeConvert( targetPos )
		if not targetPos:
			KBEDebug.ERROR_MSG("AIAction88 param2 is invalid!")
			return
		self.targetPos = Math.Vector3(KBEMath.Unreal2KBEnginePosition(targetPos))

		if len(section["param2"].strip().split("|"))>1:		
			direction = Functions.vector3TypeConvert( section["param2"].strip().split("|")[1] )
			if direction:
				self.direction = KBEMath.Unreal2KBEngineDirection( direction )

		self.distanceTable = tuple(map(float,section["param3"].strip().split('|')))
		if len( self.distanceTable )!=2:
			KBEDebug.ERROR_MSG("AIAction88 param3 is invalid!")
	
		if section["param4"].strip()!="":
			jumpDatas = section["param4"].strip().split( "|" )
			if len( jumpDatas ) > 0:
				self.jumpSpeed = float( jumpDatas[0] )
			if len( jumpDatas ) > 1:
				self.gravity = float( jumpDatas[1] )
			if len( jumpDatas ) > 2:
				self.actionTime = float( jumpDatas[2] )

		self.effectIDs = section["param5"].strip()



	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not self.targetPos:
			return

		rMin = self.distanceTable[0]
		rMax = self.distanceTable[1]
		if rMin<0 or rMin > rMax or rMax<0:
			KBEDebug.ERROR_MSG( "rMin = %f,rMax = %f,param2  is invalid!"%(rMin,rMax) )
			return	
		r = random.uniform( rMin, rMax )
		angle = random.uniform( -3.14,3.14 )
		targetPosition = (self.targetPos.x + r*math.cos(angle), self.targetPos.y, self.targetPos.z + r*math.sin(angle))
		tarPosition = KBEngine.collideVertical( entity.spaceID, entity.layer, Math.Vector3(targetPosition), 10, - 10 )
		pos = tarPosition[0] if len(tarPosition) else self.targetPos
		if pos:
			if self.actionTime > 0:
				entity.monsterAppearJump( self.actions, self.effectIDs, Math.Vector3(pos), self.direction, self.jumpSpeed, self.gravity, self.actionTime )
			elif self.gravity > 0:
				entity.monsterAppearJump( self.actions, self.effectIDs, Math.Vector3(pos), self.direction, self.jumpSpeed, self.gravity )
			elif self.jumpSpeed > 0:
				entity.monsterAppearJump( self.actions, self.effectIDs, Math.Vector3(pos), self.direction, self.jumpSpeed )
			else:
				entity.monsterAppearJump( self.actions, self.effectIDs, Math.Vector3(pos), self.direction )

class AIAction89(AIActionBase.AIActionBase):
	"""
	怪物出场跳向AI目标
	param1 actions 三段跳动作列表 |隔开
	param2 distanceTable 范围
	param3 jumpSpeed 跳跃速度 gravity 重力加速度 actionTime 起跳动作时间
	param4 direction
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.actions = []
		self.distanceTable = []
		self.jumpSpeed = -1.0
		self.gravity = -1.0
		self.actionTime = -1.0
		self.direction = None
		self.effectIDs = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

		self.actions = section["param1"].strip().split("|")
		if len(self.actions)!=3:
			KBEDebug.ERROR_MSG("AIAction89 param1 is invalid!")

		self.distanceTable = tuple(map(float,section["param2"].strip().split('|')))
		if len( self.distanceTable )!=2:
			KBEDebug.ERROR_MSG("AIAction89 param2 is invalid!")
	
		if section["param3"].strip()!="":
			jumpDatas = section["param3"].strip().split( "|" )
			if len( jumpDatas ) > 0:
				self.jumpSpeed = float( jumpDatas[0] )
			if len( jumpDatas ) > 1:
				self.gravity = float( jumpDatas[1] )
			if len( jumpDatas ) > 2:
				self.actionTime = float( jumpDatas[2] )
		if section["param4"].strip()!="":
			self.direction = ( section["param4"] )

		self.effectIDs = section["param5"].strip()


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		aiTargetEntity = KBEngine.entities.get(entity.monsterAIGetTarget(),None)
		if not aiTargetEntity:
			return


		rMin = self.distanceTable[0]
		rMax = self.distanceTable[1]
		if rMin<0 or rMin > rMax or rMax<0:
			KBEDebug.ERROR_MSG( "rMin = %f,rMax = %f,param2  is invalid!"%(rMin,rMax) )
			return	
		r = random.uniform( rMin, rMax )
		angle = random.uniform( -3.14,3.14 )
		targetPosition = Math.Vector3(aiTargetEntity.position.x + r*math.cos(angle), aiTargetEntity.position.y, aiTargetEntity.position.z + r*math.sin(angle))

		direction = None
		if self.direction == '1':
			if entity.hasFlag( csdefine.FLAG_CANT_ROTATE ):
				return
			yaw = csarithmetic.getYawByVector3(aiTargetEntity.position-targetPosition)
			direction = Math.Vector3((0,0,yaw))

		if self.actionTime > 0:
			entity.monsterAppearJump( self.actions, self.effectIDs, targetPosition, direction, self.jumpSpeed, self.gravity, self.actionTime )
		elif self.gravity > 0:
			entity.monsterAppearJump( self.actions, self.effectIDs, targetPosition, direction, self.jumpSpeed, self.gravity )
		elif self.jumpSpeed > 0:
			entity.monsterAppearJump( self.actions, self.effectIDs, targetPosition, direction, self.jumpSpeed )
		else:
			entity.monsterAppearJump( self.actions, self.effectIDs, targetPosition, direction )


class AIAction90(AIActionBase.AIActionBase):
	"""
	怪物出场跳原地三段跳
	param1 actions 三段跳动作列表 |隔开
	param2 loopTime stageProcess播放时长
	param2 jumpSpeed 跳跃速度
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.actions = []
		self.loopTime = 0.0
		self.effectIDs = ""
	

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.actions = section["param1"].strip().split("|")
		if len(self.actions)!=3:
			KBEDebug.ERROR_MSG("AIAction90 param1 is invalid!")

		self.loopTime = float(section["param2"].strip())
		self.effectIDs = section["param3"].strip()

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""

		entity.monsterAppearJumpWithoutMove( self.actions, self.effectIDs, self.loopTime )


class AIAction91(AIActionBase.AIActionBase):
	"""
	播放指定光效
	@param1 effectID 光效ID
	@param2 slotName 插槽
	@param3 scale 模型缩放倍率
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.effectID = None
		self.slotName = ""
		self.scale = -1.0
	

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.effectID = section["param1"].strip()
		if len(section["param2"].strip()):
			self.slotName = section["param2"].strip()
		if len(section["param3"].strip()):
			self.scale = float( section["param3"].strip() )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.effectID:
			entity.allClients.CLIENT_OnPlayParticles( entity.id,self.effectID,self.slotName, self.scale, Math.Vector3(0,0,0) )

class AIAction92(AIActionBase.AIActionBase):
	"""
	显示特殊进度条
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.text = ""
		self.persistTime = 0.0
		self.iconName = ""
	
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.text = section["param1"]
		self.persistTime = float(section["param2"].strip())
		self.iconName = section["param3"]
	
	def do(self, ai, entity, triggerEntity):
		entity.allClients.CLIENT_ShowSpecialProgress( self.text, self.persistTime, self.iconName )

class AIAction93(AIActionBase.AIActionBase):
	"""
	隐藏特殊进度条
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
	
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
	
	def do(self, ai, entity, triggerEntity):
		entity.allClients.CLIENT_HideSpecialProgress()


class AIAction94(AIActionBase.AIActionBase):
	"""
	销毁一定范围内指定的entity
	@param1 scriptID
	@param2 radius
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.eType = None
		self.scriptID = []
		self.radius = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.eType = section["param1"].strip()
		if len(section["param2"].strip()):
			self.scriptID = section["param2"].strip().split("|")
		self.radius = float(section["param3"].strip())
	
	def do(self, ai, entity, triggerEntity):
		if self.eType == "Role":
			KBEDebug.ERROR_MSG("can't destroy Role type entity! ")
			return
		if 	len(self.scriptID):
			entities = [e for e in entity.entitiesInRangeExt(self.radius,self.eType) if e.scriptID in self.scriptID]
		else:
			entities=entity.entitiesInRangeExt(self.radius,self.eType)

		for e in entities:
			e.destroySelf()

class AIAction95(AIActionBase.AIActionBase):
	"""
	标记回走不移除的buffID
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.buffIDs = [ int(i) for i in section["param1"].split("|") ]
	
	def do(self, ai, entity, triggerEntity):
		entity.resetKeepBuffs = self.buffIDs

class AIAction96(AIActionBase.AIActionBase):
	"""
	清除回走不移除的buffID标记
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.buffIDs = [ int(i) for i in section["param1"].split("|") ]
	
	def do(self, ai, entity, triggerEntity):
		tempList = []
		for i in entity.resetKeepBuffs:
			if i not in self.buffIDs:
				tempList.append(i)
		entity.resetKeepBuffs = tempList


class AIAction97(AIActionBase.AIActionBase):
	"""
	callmonster选择主人敌人列表中距离主人最近的一个作为攻击目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	
	def do(self, ai, entity, triggerEntity):
		if not hasattr( entity, 'owner' ):
			return
		if not entity.owner:
			return
		master = KBEngine.entities.get( entity.owner.id, None )
		if not master:
			return
		enemyListCopy = dict(master.enemyList)
		enemyIDList = [e for e in enemyListCopy.keys() if entity.monsterAICheckInViewRange(e)]
		if not len(enemyIDList):
			return
			
		minDis = 100000.0
		targetID = 0
		for eID in enemyIDList:
			e = KBEngine.entities.get(eID,None)
			if not e:
				continue
			distance = e.position.flatDistTo( master.position )
			if distance<=minDis:
				if e.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
					continue
				minDis = distance
				targetID = eID
		entity.behControlReset(csdefine.BEHAVIOUR_TYPE_SPELL)
		entity.setTargetID(targetID)

class AIAction98(AIActionBase.AIActionBase):
	"""
	废弃
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.oddList = []		#释放技能的概率:远离的概率:游走的概率
		self.backDist = 1.0
		self.moveSpeed = 2.0
		self.skillLastCount = 5.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if len(section["param1"].strip()):
			self.oddList = section["param1"].strip().split("|")
		if len( self.oddList ) > 0 and len( self.oddList ) < 2:
			self.oddList.append( str( 1 - float( self.oddList[0] ) ) )
		self.backDist = float( section["param2"] )
		self.moveSpeed = float( section["param3"] )
		if len(section["param4"].strip()):
			self.skillLastCount = float(section["param4"].strip())
		

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			return
			
		targetPosition = Math.Vector3( targetEntity.position )
		if not len(entity.attrSkills):
			KBEDebug.ERROR_MSG("entity attrSkills is []")
			return
				
		skillIDs = list( entity.attrSkills )
		if entity.lastRandomSkillID in skillIDs:
			skillIDs.remove( entity.lastRandomSkillID )
		skillID = random.choice( skillIDs )
		
		if entity.monsterAISkillLastTime > 0 and (Functions.getTime() - entity.monsterAISkillLastTime)/csconst.TIME_ENLARGE_MULTIPLE < self.skillLastCount:
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [int(skillID), entity.getTargetID(), False ] )
			return
		randOdd = random.random()
		if randOdd < float( self.oddList[0] ):
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [int(skillID), entity.getTargetID(), False ] )
			entity.monsterAISkillLastTime = Functions.getTime()
		elif randOdd < float( self.oddList[0] ) + float( self.oddList[1] ) and randOdd >= float( self.oddList[0] ):
			entity.moveAwayFromTarget( targetPosition, self.moveSpeed, False, self.backDist )
			entity.monsterAISkillLastTime = 0
		else:
			entity.walkAroundTarget( entity.getTargetID(), targetPosition, math.pi*3/4, self.moveSpeed, False )

class AIAction99( AIActionBase.AIActionBase ):
	"""
	对自己随机使用一个技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.skillIDs = []
		self.priorityLevel = csdefine.BEHAVIOUR_COMMON

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			tSkillIDs = [ int( skillID ) for skillID in section["param1"].split("|") ]
			for skillID in tSkillIDs:
				if self.checkSkillIsExit( skillID ):
					self.skillIDs.append( skillID )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not len(self.skillIDs):
			KBEDebug.ERROR_MSG("param1 config error!!")
			return
		skillIDs = list( self.skillIDs )
		for skillID in self.skillIDs:
			result = entity.monsterAIIsCanUseSkillToSelf(skillID) and \
					entity.behaviours[2].isCanAddBehavior( entity,[skillID,entity.id,False], self.priorityLevel )
			if not result:
				skillIDs.remove(skillID)

		if not len(skillIDs):
			return
		skillID = skillIDs[ random.randint(0,len(skillIDs)-1) ]

		entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [skillID, entity.id,False],self.priorityLevel)


class AIAction100( AIActionBase.AIActionBase ):
	"""
	选择某个坐标位置释放技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.skillID = 0
		self.targetPosition = None

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.skillID = int(section["param1"])
		if not self.checkSkillIsExit( self.skillID ):
			self.skillID = 0
		targetPosition = Functions.vector3TypeConvert(section["param2"])
		if targetPosition:
			self.targetPosition = KBEMath.Unreal2KBEnginePosition(targetPosition)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not self.skillID or not self.targetPosition:
			KBEDebug.ERROR_MSG("AIAction100: please check param1 or param2 is valid!")
			return
		entity.useSkillToPosition( self.skillID, self.targetPosition )


class AIAction101( AIActionBase.AIActionBase ):
	"""
	选择攻击目标当前位置释放技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.skills = []
		self.radiusMin = 0.0
		self.radiusMax = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.skills = [int(x) for x in section["param1"].split("|") if self.checkSkillIsExit(int(x))]
		if section["param2"]:
			self.radiusMax = float(section["param2"])
		if section["param3"]:
			self.radiusMin = float(section["param3"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not len(self.skills):
			return
		skillID = random.choice(self.skills)
		targetEntity = KBEngine.entities.get(entity.getTargetID(),None)
		if not targetEntity:
			KBEDebug.ERROR_MSG("AIAction101: entity  targetEntity is None !")
			return

		if self.radiusMax<=0:
			entity.useSkillToPosition( skillID, targetEntity.position )
			return

		radius = random.uniform( self.radiusMin, self.radiusMax )
		angel = random.uniform( 0, math.pi*2 )
		posX = radius*math.cos( angel )+targetEntity.position.x
		posY = targetEntity.position.y
		posZ = radius*math.sin( angel )+targetEntity.position.z
		targetPosition = Math.Vector3( posX,posY,posZ )
		entity.useSkillToPosition( skillID, targetPosition )


class AIAction102( AIActionBase.AIActionBase ):
	"""
	废弃
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.route = 0
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.route = int (section["param1"])
		if section["param2"].strip():
			self.moveSpeed = float(section["param2"].strip())
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		entity.monsterExtMachineStartPatrol( self.route, moveSpeed, isUpdateSpeed )	
		
class AIAction103( AIActionBase.AIActionBase ):
	"""
	向AI目标相反方向移动
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._velocity = 0.0								#移速

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._velocity = section["param1"] and float( section["param1"]) or 0.0

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get(entity.monsterAIGetTarget(),None)
		if not targetEntity:
			KBEDebug.ERROR_MSG("AIAction103: entity  targetEntity is None !")
			return
		
		dist = 0.3
		if self._velocity:
			speed = self._velocity
			isUpdateSpeed = False
		else:
			speed = entity.getSpeed()
			isUpdateSpeed = True
		diffPos = entity.position - targetEntity.position
		diffPos.normalise()
		dstPos = diffPos * speed + entity.position
		# 为表现，加入随机角度
		randomY = random.uniform( math.pi/6, -math.pi/6 )
		yaw = csarithmetic.getYawByVector3( diffPos ) + randomY
		distance = entity.position.flatDistTo( dstPos )
		dstPos = Math.Vector3( entity.position.x + distance * math.sin(yaw), entity.position.y, entity.position.z + distance * math.cos(yaw) )
		#加行为
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
		moveArgs = [ Math.Vector3(dstPos) ]
		entity.behAdd( behType, [ moveScriptID, speed, isUpdateSpeed,  moveArgs ] )

class AIAction104( AIActionBase.AIActionBase ):
	"""
	废弃
	设置智能追击参数
	param1：chaseMaxDist|chaseSpeedUp 加速距离，与追击目标距离大于加速距离开始加速|加速百分比
	param2：chaseMinDist|chaseSpeedDonw 减速距离，与追击目标距离小于减速距离开始减速|减速百分比
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.chaseMaxDist = 100000.0    #追击时，距离目标大于此值时，加速追击
		self.chaseMinDist = -1.0      #追击时，距离目标小于此值时，减速追击
		self.chaseSpeedUp = 0.0 	 #加速追击的速度百分比
		self.chaseSpeedDown = 0.0 	 #减速追击的速度百分比

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.chaseMaxDist =  [float(i) for i in section["param1"].split("|")][0]
		self.chaseSpeedUp =  [float(i) for i in section["param1"].split("|")][1]
		self.chaseMinDist =  [float(i) for i in section["param2"].split("|")][0]
		self.chaseSpeedDown =  [float(i) for i in section["param2"].split("|")][1]


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.chaseMaxDist = self.chaseMaxDist
		entity.chaseMinDist = self.chaseMinDist
		entity.chaseSpeedUp = self.chaseSpeedUp
		entity.chaseSpeedDown = self.chaseSpeedDown	


class AIAction105( AIActionBase.AIActionBase ):
	"""
	改变怪物领域范围
	param1： 领域范围

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.territoryRange = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.territoryRange = int(section["param1"])


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.territoryRange = self.territoryRange


class AIAction106( AIActionBase.AIActionBase ):
	"""
	给当前触发主动反应陷阱范围的entity发送AI指令
	param1： AI指令

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.commandID = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.commandID = section["param1"]


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.commandID and triggerEntity:
			entity.monsterAISendCommand(triggerEntity.id, self.commandID)


class AIAction107(AIActionBase.AIActionBase):
	"""
	把当前triggerEntity目标加入敌人列表
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = triggerEntity
		if targetEntity:
			if entity.canBuildEnemyRelation(targetEntity) :
				FightRuleMgr.g_fightMgr.buildEnemyRelation( entity, targetEntity)


class AIAction108(AIActionBase.AIActionBase):
	"""
	改变triggerEntity为攻击目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = triggerEntity
		if targetEntity:
			if targetEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
				return
			if entity.canBuildEnemyRelation(targetEntity):
				FightRuleMgr.g_fightMgr.buildEnemyRelation( entity, targetEntity)
				entity.setTargetID(targetEntity.id)


class AIAction109(AIActionBase.AIActionBase):
	"""
	triggerEntity显示界面并播放语音
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.voiceID = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.voiceID = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = triggerEntity
		if targetEntity and targetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and targetEntity.getState() != csdefine.ENTITY_STATE_PEAD \
		and targetEntity.getState() != csdefine.ENTITY_STATE_DEAD and not targetEntity.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):
			entity.monsterAIShowMessagePlaySound(targetEntity, self.voiceID)


class AIAction110(AIActionBase.AIActionBase):
	"""
	对triggerEntity使用技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.spellSkillID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.spellSkillID = int(section["param1"])
		if not self.checkSkillIsExit( self.spellSkillID ):
			self.spellSkillID = 0

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.spellSkillID:
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.spellSkillID, triggerEntity.id,False])
		else:
			KBEDebug.WARNING_MSG("entity scriptID %s not config spellSkillID%s" % (entity.scriptID, self.spellSkillID))


class AIAction111(AIActionBase.AIActionBase):
	"""
	触发triggerEntity自己对自己使用技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.spellSkillID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.spellSkillID = int(section["param1"])
		if not self.checkSkillIsExit( self.spellSkillID ):
			self.spellSkillID = 0

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.spellSkillID:
			AIEntity = triggerEntity
			if AIEntity :
				if not AIEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
					AIEntity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.spellSkillID, triggerEntity, False])
				else:
					AIEntity.useSkillToEntity(self.spellSkillID, AIEntity.id)
		else:
			KBEDebug.WARNING_MSG("entity scriptID %s not config spellSkillID%s" % (entity.scriptID, self.spellSkillID))


class AIAction112(AIActionBase.AIActionBase):
	"""
	触发triggerEntity完成某一个事件目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.questID = 0
		self.questTargetID = 0
		self.questTargetCount = 1

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.questID = int(section["param1"])
		self.questTargetID = int(section["param2"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = triggerEntity
		if targetEntity.getState() != csdefine.ENTITY_STATE_PEAD and targetEntity.getState() != csdefine.ENTITY_STATE_DEAD and \
		not targetEntity.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):  #玩家未决状态下与死亡状态下不会完成任务
			targetEntity.questTaskIncreaseState(self.questID, self.questTargetID)

class AIAction113(AIActionBase.AIActionBase):
	"""
	清除triggerEntity身上某些buff
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIndexs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)	
		self.buffIDs = [int(x) for x in section["param1"].split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = triggerEntity
		if not targetEntity:
			return

		for buffID in self.buffIDs:
			targetEntity.removeBuffByID( buffID )


class AIAction114(AIActionBase.AIActionBase):
	"""
	将单个玩家（triggerEntity）传送到某个地图的某个位置
	Param1：地图名
	Param2：position，以空格分隔
	Param3：direction，以空格分隔

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = None
		self.direction = None

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

		self.spaceScriptID = section["param1"]
		position = Functions.vector3TypeConvert( section["param2"] )
		if not position:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param2(%s)" %( self.getAIID(), section["param2"] ) )
		else:
			self.position = KBEMath.Unreal2KBEnginePosition( position )

		direction = Functions.vector3TypeConvert( section["param3"] )
		if  direction==None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param3(%s)" %( self.getAIID(), section["param3"] ) )
		else:
			self.direction = KBEMath.Unreal2KBEngineDirection( direction )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		
		targetEntity = triggerEntity
		if not targetEntity:
			return
		if targetEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		if self.position == None or self.direction == None:
			return
		targetEntity.gotoSpace(self.spaceScriptID, self.position, self.direction)


class AIAction115(AIActionBase.AIActionBase):
	"""
	指定位置，朝向（默认为本身位置，朝向），创建一个与当前triggerEntity(玩家)外形一样，技能一样的心魔类型怪物
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = None
		self.direction = None
		self.scriptID = None

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		
		position = Functions.vector3TypeConvert( section["param1"] )
		if position:
			self.position = KBEMath.Unreal2KBEnginePosition( position )

		direction = Functions.vector3TypeConvert( section["param2"] )
		if direction:
			self.direction = KBEMath.Unreal2KBEngineDirection( direction )
		
		self.scriptID = section["param3"].strip()

	def do(self, ai, entity, triggerEntity):

		position = self.position or Math.Vector3(entity.position)
		direction = self.direction or Math.Vector3(entity.direction)

		targetEntity = triggerEntity
		if not targetEntity:
			return

		def getXinMoSkills( skillIDList ):
			"""
			通过带对表替换相应技能
			"""
			attrSkills = []
			skillData = XinMoSkillConfig.datas
			for skillID in skillIDList:
				if skillID not in skillData:
					#KBEDebug.ERROR_MSG("skillID = %s is not in XinMoSkillConfig.datas"%skillID)
					continue
				attrSkills.append(skillData[skillID])
			return attrSkills

		self.attrSkills = getXinMoSkills(targetEntity.attrSkills)

		param = {}
		param.update( {"ownerID":targetEntity.id} )
		param.update( {"spawnPos":tuple(Math.Vector3(targetEntity.position))} )
		param.update( {"spawnDir":tuple(Math.Vector3(0.0, 0.0, targetEntity.direction.z))} )
		param.update( {"level":targetEntity.level} )
		param.update( {"attrSkills":self.attrSkills} )
		if MonsterModelNumberCopyPlayer.datas.get("MonsterExtXinMo",None):
			modelNumber =  MonsterModelNumberCopyPlayer.datas["MonsterExtXinMo"][targetEntity.getGender()][targetEntity.getCamp()][targetEntity.getProfession()]
			param.update( {"modelNumber":modelNumber} )
		else:
			KBEDebug.ERROR_MSG("MonsterModelNumberCopyPlayer config is not has MonsterExtXinMo")
		newEntity = entity.createMonster( self.scriptID, position, direction, param )
		if not newEntity:
			KBEDebug.ERROR_MSG("createMonster failed!")


class AIAction116(AIActionBase.AIActionBase):
	"""
	增加triggerEntity身上的Buff
	
	param1：BuffID，支持多个，以竖号分隔，表示且；


	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.scriptID == "20010881":
			KBEDebug.ERROR_MSG("entity.id = %d"%entity.id)
		AITargetEntity = triggerEntity
		if not AITargetEntity:
			return
		for buffID in self.buffIDs:
			AITargetEntity.addBuff( entity, buffID )


class AIAction117(AIActionBase.AIActionBase):
	"""
	怪物出场跳向triggerEntity
	param1 actions 三段跳动作列表 |隔开
	param2 distanceTable 范围
	param3 jumpSpeed 跳跃速度 gravity 重力加速度 actionTime 起跳动作时间
	param4 direction
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.actions = []
		self.distanceTable = []
		self.jumpSpeed = -1.0
		self.gravity = -1.0
		self.actionTime = -1.0
		self.direction = None
		self.effectIDs = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

		self.actions = section["param1"].strip().split("|")
		if len(self.actions)!=3:
			KBEDebug.ERROR_MSG("AIAction89 param1 is invalid!")

		self.distanceTable = tuple(map(float,section["param2"].strip().split('|')))
		if len( self.distanceTable )!=2:
			KBEDebug.ERROR_MSG("AIAction89 param2 is invalid!")
	
		if section["param3"].strip()!="":
			jumpDatas = section["param3"].strip().split( "|" )
			if len( jumpDatas ) > 0:
				self.jumpSpeed = float( jumpDatas[0] )
			if len( jumpDatas ) > 1:
				self.gravity = float( jumpDatas[1] )
			if len( jumpDatas ) > 2:
				self.actionTime = float( jumpDatas[2] )
		if section["param4"].strip()!="":
			self.direction = ( section["param4"] )

		self.effectIDs = section["param5"].strip()


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		aiTargetEntity = triggerEntity
		if not aiTargetEntity:
			return


		rMin = self.distanceTable[0]
		rMax = self.distanceTable[1]
		if rMin<0 or rMin > rMax or rMax<0:
			KBEDebug.ERROR_MSG( "rMin = %f,rMax = %f,param2  is invalid!"%(rMin,rMax) )
			return	
		r = random.uniform( rMin, rMax )
		angle = random.uniform( -3.14,3.14 )
		targetPosition = Math.Vector3(aiTargetEntity.position.x + r*math.cos(angle), aiTargetEntity.position.y, aiTargetEntity.position.z + r*math.sin(angle))

		direction = None
		if self.direction == '1':
			if entity.hasFlag( csdefine.FLAG_CANT_ROTATE ):
				return
			yaw = csarithmetic.getYawByVector3(aiTargetEntity.position-targetPosition)
			direction = Math.Vector3((0,0,yaw))

		if self.actionTime > 0:
			entity.monsterAppearJump( self.actions, self.effectIDs, targetPosition, direction, self.jumpSpeed, self.gravity, self.actionTime )
		elif self.gravity > 0:
			entity.monsterAppearJump( self.actions, self.effectIDs, targetPosition, direction, self.jumpSpeed, self.gravity )
		elif self.jumpSpeed > 0:
			entity.monsterAppearJump( self.actions, self.effectIDs, targetPosition, direction, self.jumpSpeed )
		else:
			entity.monsterAppearJump( self.actions, self.effectIDs, targetPosition, direction )


class AIAction118( AIActionBase.AIActionBase ):
	"""
	向triggerEntity相反方向移动
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._velocity = 0.0								#移速

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._velocity = section["param1"] and float( section["param1"]) or 0.0

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = triggerEntity
		if not targetEntity:
			KBEDebug.ERROR_MSG("AIAction118: entity  targetEntity is None !")
			return
		
		dist = 0.3
		if self._velocity:
			speed = self._velocity
			isUpdateSpeed = False
		else:
			speed = entity.getSpeed()
			isUpdateSpeed = True
		
		diffPos = entity.position - targetEntity.position
		diffPos.normalise()
		dstPos = diffPos * speed + entity.position
		# 为表现，加入随机角度
		randomY = random.uniform( math.pi/6, -math.pi/6 )
		yaw = csarithmetic.getYawByVector3( diffPos ) + randomY
		distance = entity.position.flatDistTo( dstPos )
		dstPos = Math.Vector3( entity.position.x + distance * math.sin(yaw), entity.position.y, entity.position.z + distance * math.cos(yaw) )
		
		#加行为
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT

		moveArgs = [ Math.Vector3(dstPos) ]
		entity.behAdd( behType, [ moveScriptID, speed, isUpdateSpeed, moveArgs ] )

class AIAction119(AIActionBase.AIActionBase):
	"""
	param1为任务ID，如果填了此参数则表示与任务相关，如果没有填则与任务无关，主要用于AI目标玩家是否被执行过当前AI
	任务相关：
			在AI目标玩家身上记录当前任务ID与aiid，当该任务ID重置或者放弃时清除该任务ID下保存的数据
	任务无关：
			在自身数据记录aiid与玩家DBID
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.questID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.questID = int(section[ "param1" ])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		aiTargetEntity = triggerEntity
		if not aiTargetEntity or not aiTargetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			return
		if  aiTargetEntity.getState() == csdefine.ENTITY_STATE_PEAD or aiTargetEntity.getState() == csdefine.ENTITY_STATE_DEAD and \
		aiTargetEntity.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):  #玩家未决状态下与死亡状态下不会完成任务
			return
			
		if self.questID:
			aiid = int(str(entity.scriptID)+str(ai.getID()))
			aiTargetEntity.addQuestRecordAIIDS(self.questID,aiid)
		else:
			entity.monsterAIMarkRoleForAIID(ai.getID(),aiTargetEntity.playerDBID)


class AIAction120( AIActionBase.AIActionBase ):
	"""
	根据AI目标的职业对AI目标使用技能，根据策划的配置习惯从战士，剑客，链刃，法师依次填写技能ID，用“|”隔开
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.professions = [csdefine.CLASS_FIGHTER, csdefine.CLASS_SWORDMAN, csdefine.CLASS_ARCHER, csdefine.CLASS_MAGE]						
		self.Dict = {}

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		tskillIDs = [int(skillID) for skillID in section["param1"].strip().split("|")]
		result = True
		for skillID in tskillIDs:
			if not self.checkSkillIsExit( skillID ): #如果不存在
				result = False
				
		if result:
			self.Dict = dict(zip(self.professions, tskillIDs ))

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if len( self.Dict ) == 0 :
			KBEDebug.CRITICAL_MSG( "Param1 Config Error!!( entityScriptID:%s, AIID: %d )" % ( triggerEntity.getScriptID(), self._aiID ) )
			return
			
		targetEntity = entity.monsterAIGetTargetEntity()
		if not targetEntity:
			KBEDebug.ERROR_MSG("AIAction120: entity  targetEntity is None !")
			return
		
		entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.Dict[targetEntity.profession], targetEntity.id, False])


class AIAction121( AIActionBase.AIActionBase ):
	"""
	根据triggerEntity的职业对AI目标使用技能，根据策划的配置习惯从战士，剑客，链刃，法师依次填写技能ID，用“|”隔开
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.professions = [csdefine.CLASS_FIGHTER, csdefine.CLASS_SWORDMAN, csdefine.CLASS_ARCHER, csdefine.CLASS_MAGE]						
		self.Dict = {}

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		tskillIDs = [int(skillID) for skillID in section["param1"].strip().split("|")]
		result = True
		for skillID in tskillIDs:
			if not self.checkSkillIsExit( skillID ): #如果不存在
				result = False
		if result:
			self.Dict = dict(zip(self.professions, tskillIDs ))

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if len( self.Dict ) == 0 :
			KBEDebug.CRITICAL_MSG( "Param1 Config Error!!( entityScriptID:%s, AIID: %d )" % ( triggerEntity.getScriptID(), self._aiID ) )
			return
			
		targetEntity = triggerEntity
		if not targetEntity:
			KBEDebug.ERROR_MSG("AIAction120: entity  targetEntity is None !")
			return
		
		entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.Dict[targetEntity.profession], targetEntity.id, False])

class AIAction122( AIActionBase.AIActionBase ):
	"""
	转圈
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.velocity = 0.0		#每秒转多少弧度

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.velocity = float( section["param1"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.startLoopRotator( self.velocity )

class AIAction123( AIActionBase.AIActionBase ):
	"""
	停止转圈
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.stopMoving( csdefine.MOVE_TYPE_LOOP_ROTATOR )

class AIAction124( AIActionBase.AIActionBase ):
	"""
	雷之泉：根据雷球获得Buff
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		scriptIDs = []
		
		# 添加Buff
		if spaceEntity:
			for entityID in spaceEntity.spawnInfo.keys():
				entity_ = KBEngine.entities.get( entityID )
				if entity_:					
					scriptID = entity_.scriptID
					if scriptID in Const.LEI_SCRIPTID_TO_BUFFID and "LQ" in entity_.signs:
						scriptIDs.append( scriptID )
			if scriptIDs:
				choiceSID = random.choice( scriptIDs )
				buffID = Const.LEI_SCRIPTID_TO_BUFFID[choiceSID]
				entity.addBuff( entity, buffID )


class AIAction125( AIActionBase.AIActionBase ):
	"""
	callMonster复制主人敌人列表
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.mExtCallCopyOwnerEnemyList()

class AIAction126( AIActionBase.AIActionBase ):
	"""
	弹出对话框（MonsterExtClick/MonsterExtClickAndModel）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.gossipText = ""
		self.gossipOption = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.gossipText = section["param1"]						# MSG
		for sect in [ section["param2"], section["param3"], section["param4"], section["param5"] ]:
			sSect = sect.split("|")
			if len(sSect) >= 3:
				self.gossipOption.append( ( sSect[0], sSect[1], int(sSect[2]) ) )	# (key, title, type)
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if triggerEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			triggerEntity.setMonsterGossipText( entity.id, self.gossipText )
			
			for m in self.gossipOption:
				triggerEntity.addMonsterGossipOption(*m)

class AIAction127( AIActionBase.AIActionBase ):
	"""
	改变临时阵营（CST-2129）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._camp = 0
	
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._camp = int(section["param1"])
		if self._camp not in csdefine.CAMP_LIST:
			KBEDebug.ERROR_MSG("AIAction(%s) config error camp:%s!" % (self.getAIID(), self._camp))
	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.setTempCamp( self._camp )

class AIAction128( AIActionBase.AIActionBase ):
	"""
	改变临时势力（CST-2129）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._faction = 0
	
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._faction = int(section["param1"])
	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.setTempFaction( self._faction )
		
class AIAction129( AIActionBase.AIActionBase ):
	"""
	关闭对话框
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
	
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if triggerEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			triggerEntity.sendMonsterGossipComplete( entity.id )



class AIAction130(AIActionBase.AIActionBase):
	"""
	在选好的多个坐标位置中随机选择一个坐标位置召唤一个entity。
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.posList = []     #坐标列表
		self.dirList = []	  #朝向列表
		self.scriptID = None  #entityID

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )	
		#坐标与朝向一一对应
		posListStr = section["param1"].strip().split("|")
		dirListStr = section["param2"].strip().split("|")

		for index in range(0,len(posListStr)):
			position = Functions.vector3TypeConvert( posListStr[index] )
			if position:
				position = KBEMath.Unreal2KBEnginePosition( position )
			else:
				position = (0,0,0)
			self.posList.append(position)

			direction = Functions.vector3TypeConvert( dirListStr[index] )
			if direction:
				direction = KBEMath.Unreal2KBEngineDirection( direction )
			else:
				direction = (0,0,0)
			self.dirList.append(direction)

		self.scriptID = section["param3"].strip()
		

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		index = random.randint(0,len(self.posList)-1)

		position = self.posList[index]
		direction = self.dirList[index]

		newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(position), Math.Vector3(direction),{ "spawnPos":Math.Vector3(position) ,"spawnDir":(direction)})

class AIAction131(AIActionBase.AIActionBase):
	"""
	根据性别播放语音
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.mvoiceID = ""			# 男性语音
		self.fvoiceID = ""			# 女性语音

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.mvoiceID = section["param1"]
		self.fvoiceID = section["param2"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = triggerEntity
		if targetEntity and targetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and targetEntity.getState() != csdefine.ENTITY_STATE_PEAD \
		and targetEntity.getState() != csdefine.ENTITY_STATE_DEAD and not targetEntity.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):
			if entity.gender == csdefine.MALE and self.mvoiceID:
				entity.monsterAIShowMessagePlaySound(targetEntity, self.mvoiceID)
			elif entity.gender == csdefine.FEMALE and self.fvoiceID:
				entity.monsterAIShowMessagePlaySound(targetEntity, self.fvoiceID)
				

class AIAction132(AIActionBase.AIActionBase):
	"""
	在某范围内随机播放一定数量光效
	@param1 effectID:影子effectID;effecID:影子effectID|effectID:影子effectID;effectID:影子effectID 光效ID1;光效ID2|光效ID3;光效ID4 其中光效ID1和光效ID2为同类型光效
	@param2 ratio 每种类型光效播放的概率 一一对应
	@param3 amount|radius 总数量|半径范围  用于光效偏移
	@param4 语言ID|语音ID...
	@param5	计时key|计时key...
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.effectIDList = []
		self.ratio = []
		self.amount = 0
		self.radius = 0.0
		self.soundIDList = []
		self.timeKeyList = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.effectIDList = section["param1"].split("|")
		self.ratio = [float(i) for i in section["param2"].split("|")]
		if section["param3"]:
			data = section["param3"].split("|")
			self.amount = int(data[0])
			if len(data) > 1:
				self.radius = float(data[1])
		if section["param4"]:
			self.soundIDList = section["param4"].split("|")
		if section["param5"]:
			self.timeKeyList = section["param5"].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		tempAmdount = self.amount
		def random_pick(tempList,probabilityList):
			temp = random.uniform(0,1)
			tempProbability = 0.0
			for item,item_probability in zip(tempList,probabilityList):
				if item_probability == "":
					item_probability = 0
				tempProbability += float(item_probability)
				if temp < tempProbability:break
			return item
		while tempAmdount:
			resultEffectID = random_pick( self.effectIDList,self.ratio ) #"光效ID1:影子effectID;光效ID2:影子effectID"
			effectIDList = random.choice(resultEffectID.split(";")) #"光效ID1:影子effectID"
			offsetPos = Math.Vector3(0,0,0)
			if self.radius:
				pos = csarithmetic.getPositionByCircular( entity.position , self.radius )
				offsetPos = pos - entity.position
				offsetPos = Math.Vector3(offsetPos.z * 100,offsetPos.x * 100,offsetPos.y * 100)
			effectIDList = effectIDList.split(":")
			entity.allClients.CLIENT_OnPlayParticles( entity.id,effectIDList[0],"", 1.0, Math.Vector3(offsetPos) )
			if len(effectIDList) > 1:
				entity.allClients.CLIENT_OnPlayParticles( entity.id,effectIDList[1],"", 1.0, Math.Vector3(offsetPos) )
			if resultEffectID in self.effectIDList:
				index = self.effectIDList.index(resultEffectID)
				if self.timeKeyList[index] not in entity.monsterAITimeTag:
					entity.monsterAITimeTag[self.timeKeyList[index]] = time.time()
					spaceEntity = entity.getCurrentSpace()
					if not spaceEntity:
						return
					for player in spaceEntity._spaceRoles:
						entity.monsterAIShowMessagePlaySound(player, self.soundIDList[index])
			tempAmdount -= 1			

class AIAction133(AIActionBase.AIActionBase):
	"""
	将一定范围内指定entity Type随机选择一个作为AI目标”的AI行为
	如果不填参数scriptID,则不进行此参数的判断，只进行类型的判断
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])

		self.entityType = section[ "param2" ]
		if section["param3"].strip()!="":
			self.scriptIDs = section["param3"].strip().split("|")
		if section["param4"].strip()!="":
			self.removeStates = [int(state) for state in section["param4"].strip().split("|")]
		


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		eid = 0
		distance = 10000.0
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs,self.removeStates )
		if len(entities)<=0:
			KBEDebug.DEBUG_MSG("len entities is 0")
			return
		index = random.randint(0,len(entities)-1)
		e = entities[index]
		if e and e.getState() != csdefine.ENTITY_STATE_DEAD:
			entity.monsterAISetTarget( e.id )


class AIAction134(AIActionBase.AIActionBase):
	"""
	将攻击目标移除敌人列表
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		target = KBEngine.entities.get(entity.getTargetID(), None)
		FightRuleMgr.g_fightMgr.breakEnemyRelation( entity, target )
		
class AIAction135(AIActionBase.AIActionBase):
	"""
	开启光墙
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.countDownTime = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.countDownTime = int(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.wallCountDownTime = self.countDownTime
		entity.startLightWallCountDown()
		entity.allClients.CLIENT_CreateFightArea()

class AIAction136(AIActionBase.AIActionBase):
	"""
	关闭光墙
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.stopLightWallCountDown()
		entity.allClients.CLIENT_OnLeaveFightArea()

class AIAction137(AIActionBase.AIActionBase):
	"""
	在一个矩形范围内，圆形范围外随机移动
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		pos = Functions.vector3TypeConvert( section["param1"] )
		self._circlePoint = Math.Vector3( KBEMath.Unreal2KBEnginePosition(pos) )
		self._radius = float( section["param2"] )
		self._length = float( section["param3"] )
		self._width = float( section["param4"] )
		if section["param5"].strip():
			self.moveSpeed = float(section["param5"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		randNum = random.randint(0,5)
		if randNum == 0:
			if entity.position.x <= self._circlePoint.x:
				randXMin = self._circlePoint.x - self._length / 2
				randXMax = self._circlePoint.x - self._radius
				randZMin = self._circlePoint.z - self._width / 2
				randZMax = self._circlePoint.z + self._width / 2
			else:
				randXMin = self._circlePoint.x + self._radius
				randXMax = self._circlePoint.x + self._length / 2
				randZMin = self._circlePoint.z - self._width / 2
				randZMax = self._circlePoint.z + self._width / 2
		elif randNum == 1:
			if entity.position.z <= self._circlePoint.z:
				randZMin = self._circlePoint.z - self._width / 2
				randZMax = self._circlePoint.z - self._radius
				randXMin = self._circlePoint.x - self._length / 2
				randXMax = self._circlePoint.x + self._length / 2
			else:
				randZMin = self._circlePoint.z + self._radius
				randZMax = self._circlePoint.z + self._width / 2
				randXMin = self._circlePoint.x - self._length / 2
				randXMax = self._circlePoint.x + self._length / 2
		else:
			return
		
		pos = self.selectPoint( entity, randXMin, randXMax, randZMin, randZMax )
		#加行为
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
			
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		moveArgs = [ Math.Vector3(pos) ]
		entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )
		
	def selectPoint( self, entity, randXMin, randXMax, randZMin, randZMax ):
		""""""
		x = random.uniform( randXMin, randXMax )
		z = random.uniform( randZMin, randZMax )
		return Math.Vector3(x, entity.position.y, z)
		
class AIAction138(AIActionBase.AIActionBase):
	"""
	移动到最近一个点
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._pos = []
		self._moveType = csdefine.MOVE_TYPE_NORMAL
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		for posStr in section["param1"].split("|"):
			pos = Functions.vector3TypeConvert( posStr )
			self._pos.append( Math.Vector3( KBEMath.Unreal2KBEnginePosition(pos) ) )
		if section["param2"]:
			self._moveType = int( section["param2"] )
		if section["param3"].strip():
			self.moveSpeed = float(section["param3"].strip())
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		minDis = 99999
		minPos = None
		for pos in self._pos:
			dst = entity.position.flatDistTo( pos )
			if minDis > dst:
				minDis = dst
				minPos = pos
		if minPos is None:
			KBEDebug.ERROR_MSG("AIAction138 get nearest pos Error!")
			return
		entity.behControlReset( csdefine.BEHAVIOUR_TYPE_MOVING )
		#加行为
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if  self._moveType == csdefine.MOVE_TYPE_NORMAL:
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
			
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		moveArgs = [ Math.Vector3(minPos), 1.0 ]
		entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )
		
class AIAction139(AIActionBase.AIActionBase):
	"""
	增加高度
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._height = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._height = int( section["param1"] ) / 100.0
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.position.y += self._height
		
class AIAction140(AIActionBase.AIActionBase):
	"""
	收集灵气（吃豆子，按巡逻路线跟随玩家）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"].strip():
			self.moveSpeed = float(section["param1"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.isMovingType( csdefine.MOVE_TYPE_STOP ):
			target = entity.monsterAIGetTargetEntity()
			if not target:
				KBEDebug.ERROR_MSG("AIAction140: entity  targetEntity is None !")
				return
			curRoute = entity.queryTemp( "MazeRoute", None )
			pointPos = entity.queryTemp( "pointPos", Math.Vector3() )
			if curRoute == None:
				curRoute, pointPos = PatrolRouteLoader.g_patrolRouteLoader.getNearestRouteAndPosByEntity( entity )
			else:
				curRoute, pointPos = PatrolRouteLoader.g_patrolRouteLoader.getNearestRouteAndPosByRouteInfo\
				( target, curRoute, pointPos )
			entity.setTemp( "MazeRoute", curRoute )
			entity.setTemp( "pointPos", pointPos )

			if pointPos != None:
				#加行为
				behType = csdefine.BEHAVIOUR_TYPE_MOVING
				if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
					moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
				else:
					moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
				(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
				moveArgs = [ Math.Vector3(pointPos) ]
				entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )

class AIAction141(AIActionBase.AIActionBase):
	"""
	收集灵气（吃豆子，随机移动）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"].strip():
			self.moveSpeed = float(section["param1"].strip())
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.isMovingType( csdefine.MOVE_TYPE_STOP ):
			target = entity.monsterAIGetTargetEntity()
			if not target:
				KBEDebug.ERROR_MSG("AIAction141: entity  targetEntity is None !")
				return
			curRoute = entity.queryTemp( "MazeRoute", None )
			pointPos = entity.queryTemp( "pointPos", Math.Vector3() )
			if curRoute == None:
				curRoute, pointPos = PatrolRouteLoader.g_patrolRouteLoader.getNearestRouteAndPosByEntity( entity )
			else:
				curRoute, pointPos = PatrolRouteLoader.g_patrolRouteLoader.getRangeRouteAndPosByRouteInfo\
				( target.getCurrentSpaceScriptID(), curRoute, pointPos )
			entity.setTemp( "MazeRoute", curRoute )
			entity.setTemp( "pointPos", pointPos )
			if pointPos != None:
				entity.behControlReset( csdefine.BEHAVIOUR_TYPE_MOVING )
				#加行为
				behType = csdefine.BEHAVIOUR_TYPE_MOVING
				if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
					moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
				else:
					moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
				(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
				moveArgs = [ Math.Vector3(pointPos) ]
				entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )
		
class AIAction142(AIActionBase.AIActionBase):
	"""
	收集灵气（吃豆子，按巡逻路线远离玩家）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"].strip():
			self.moveSpeed = float(section["param1"].strip())
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.isMovingType( csdefine.MOVE_TYPE_STOP ):
			target = entity.monsterAIGetTargetEntity()
			if not target:
				KBEDebug.ERROR_MSG("AIAction142: entity  targetEntity is None !")
				return
			curRoute = entity.queryTemp( "MazeRoute", None )
			pointPos = entity.queryTemp( "pointPos", Math.Vector3() )
			if curRoute == None:
				curRoute, pointPos = PatrolRouteLoader.g_patrolRouteLoader.getNearestRouteAndPosByEntity( entity )
			else:
				curRoute, pointPos = PatrolRouteLoader.g_patrolRouteLoader.getFarestRouteAndPosByRouteInfo\
				( target, curRoute, pointPos )
			entity.setTemp( "MazeRoute", curRoute )
			entity.setTemp( "pointPos", pointPos )
			if pointPos != None:
				#加行为
				behType = csdefine.BEHAVIOUR_TYPE_MOVING
				if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
					moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
				else:
					moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
				(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
				moveArgs = [ Math.Vector3(pointPos) ]
				entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )
				
				
class AIAction143(AIActionBase.AIActionBase):
	"""
	收集灵气（吃豆子，预判玩家移动）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"].strip():
			self.moveSpeed = float(section["param1"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.isMovingType( csdefine.MOVE_TYPE_STOP ):
			target = entity.monsterAIGetTargetEntity()
			if not target:
				KBEDebug.ERROR_MSG("AIAction143: entity  targetEntity is None !")
				return
			curRoute = entity.queryTemp( "MazeRoute", None )
			pointPos = entity.queryTemp( "pointPos", Math.Vector3() )
			if curRoute == None:
				curRoute, pointPos = PatrolRouteLoader.g_patrolRouteLoader.getNearestRouteAndPosByEntity( entity )
			else:
				curRoute, pointPos = PatrolRouteLoader.g_patrolRouteLoader.getYawRouteAndPosByRouteInfo\
				( target, curRoute, pointPos )
			entity.setTemp( "MazeRoute", curRoute )
			entity.setTemp( "pointPos", pointPos )
			if pointPos != None:
				#加行为
				behType = csdefine.BEHAVIOUR_TYPE_MOVING
				if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
					moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
				else:
					moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
				(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
				moveArgs = [ Math.Vector3(pointPos) ]
				entity.behAdd( behType, [ moveScriptID, moveSpeed,  moveArgs ] )
		
class AIAction144(AIActionBase.AIActionBase):
	"""
	沿着高度上下 移动
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._height = 0.0
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._height = float( section["param1"] )
		if section["param2"].strip():
			self.moveSpeed = float(section["param2"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		pos = Math.Vector3( entity.position ) + Math.Vector3(0, self._height, 0)
		entity.behControlReset( csdefine.BEHAVIOUR_TYPE_MOVING )
		#加行为
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		moveArgs = [ Math.Vector3(pos), 0.0 ]
		entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )

class AIAction145(AIActionBase.AIActionBase):
	"""
	停止当前动作
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.StopCurrentAction()
		
class AIAction146(AIActionBase.AIActionBase):
	"""
	改变朝向，朝向以触发AI者ID为标记的ID的entity，CST-3248
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity
		"""
		target = None
		for sign in entity.signs:
			if isinstance(sign, str) and sign.startswith(SIGN_ENTITY_ID):
				id = int(sign.split(SIGN_ENTITY_ID)[-1])
				target = KBEngine.entities.get(id, None)
				break
		if not target:
			return
		v = target.position - entity.position
		direction = (0.0,0.0,csarithmetic.getYawByVector3( v ))
		entity.changeDirection(direction, csdefine.REASON_CHANGE_DIR_VOLUNTARY)
		
class AIAction147(AIActionBase.AIActionBase):
	"""
	停止巡逻，一段时间后继续巡逻， CST-3248
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.delayTime = float(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		speed = entity.moveSpeed
		isUpdateSpeed = entity.isUpdateSpeed
		moveArgs = entity.moveArgs
		entity.stopMoving(entity.moveScriptID)
		
		entity.addTimerCallBack(self.delayTime, "startPatrol", (speed, isUpdateSpeed, moveArgs,))
			
class AIAction148(AIActionBase.AIActionBase):
	"""
	添加标记, 以触发AI者ID为标记， CST-3248
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		if triggerEntity:
			signs = set([SIGN_ENTITY_ID + str(triggerEntity.id)])
			entity.signs = entity.signs|signs

class AIAction149(AIActionBase.AIActionBase):
	"""
	移除标记, 以触发AI者ID为标记， CST-3248
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		signs = set([SIGN_ENTITY_ID + str(triggerEntity.id)])
		entity.signs = entity.signs - signs

class AIAction150(AIActionBase.AIActionBase):
	"""
	将触发者加入警告列表(MonsterExtDemonGuard怪)， CST-3248
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		if triggerEntity and not entity.hasBaffle(triggerEntity.position, entity.position):
			entity.warningList.append(triggerEntity)

class AIAction151(AIActionBase.AIActionBase):
	"""
	将警告列表加入敌人列表(MonsterExtDemonGuard怪)， CST-3248
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		entity.checkWarningList()
		for targetEntity in entity.warningList:
			if targetEntity:
				if entity.canBuildEnemyRelation(targetEntity) :
					FightRuleMgr.g_fightMgr.buildEnemyRelation( entity, targetEntity)


class AIAction152(AIActionBase.AIActionBase):
	"""
	摄魂 灵魂之誓副本 陷阱专用 （CST-3704）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffID = 0
		self.cmd = []

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.buffID = int(section["param1"])
		self.cmd = section["param2"].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		if not triggerEntity or triggerEntity.isDestroyed:
			return
		
		if triggerEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		if not triggerEntity.isInSpaceCopy():
			return

		spaceEntity = entity.getCurrentSpace()

		buffs = triggerEntity.findBuffsByBuffScript("BuffUsurp") + triggerEntity.findBuffsByBuffScript("BuffChangeBody")
		#有附身buff则移除buff
		if len(buffs):
			for index in list(triggerEntity.getAttrBuffs()):
				if index in buffs:
					triggerEntity.removeBuff(index)
			triggerEntity.addBuff(triggerEntity, self.buffID)
			spaceEntity.getScript().onConditionChange( spaceEntity, "AI", entity.scriptID, self.cmd[0], "" )
		#没有附身buff直接死亡
		else:
			triggerEntity.changeState(csdefine.ENTITY_STATE_DEAD)
			spaceEntity.getScript().onConditionChange( spaceEntity, "AI", entity.scriptID, self.cmd[1], "" )

class AIAction153(AIActionBase.AIActionBase):
	"""
	设置画卷、机关、分身属性 （CST-3790）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.matrixType = section["param1"]
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity	
		"""
		entity.setTemp("attributeType", self.matrixType)

class AIAction154(AIActionBase.AIActionBase):
	"""
	移除画卷、机关、分身属性 （CST-3790）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity	
		"""
		entity.removeTemp("attributeType")

class AIAction155(AIActionBase.AIActionBase):
	"""
	将指定entity位置设置为出生位置（CST-3790）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.scriptID = section["param1"]
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity	
		"""
		entityIDList = entity.getCurrentSpace().getEntityRecord(self.scriptID)
		if len(entityIDList) != 1:
			KBEDebug.ERROR_MSG("AIAction155: entity[%s] is none or not the only one!" % self.scriptID)
			return
		target = KBEngine.entities.get(entityIDList[0], None)
		if target:
			entity.spawnPos = Math.Vector3(target.position)

class AIAction156(AIActionBase.AIActionBase):
	"""
	机关随机性改变属性和buff（CST-3790）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.pictureScrollList = section["param1"].split("|")	#画卷scriptID
		self.elements = section["param2"].split("|")		#机关属性
		self.buffs = []
		buffs = section["param3"].split("|")		#BuffID，bA1:bA2...|bB1:bB2...，顺序和机关属性一致
		for buff in buffs:
			self.buffs.append(buff.split(":"))
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity	
		"""
		#从机关属性列表中随机出一个属性（金、木、水、火、土），但不包括当前的机关属性和画卷中没有的属性，
		#如果画卷全部都已经为空，则将机关的属性也移除
		tempElements = []
		elements = list(self.elements)
		currType = entity.queryTemp("attributeType", "")
		for scriptID in self.pictureScrollList:
			entityIDList = entity.getCurrentSpace().getEntityRecord(scriptID)
			if len(entityIDList) != 1:
				KBEDebug.ERROR_MSG("AIAction156: entity[%s] is none or not the only one!" % scriptID)
				return
			target = KBEngine.entities.get(entityIDList[0], None)
			if target and target.queryTemp("attributeType", None):
				tempElements.append(target.queryTemp("attributeType"))
		for element in self.elements:		#排除所有画卷中没有的属性
			if element not in tempElements:
				elements.remove(element)
		if entity.queryTemp("attributeType", None):		#排除当前机关的属性
			#如果还有和机关当前属性相同的画卷，并且只剩一个画卷有分身，则不需要改变机关属性
			if currType in elements and len(elements) > 1:
				elements.remove(currType)
		
		#移除当前的Buff
		if currType:
			currBuffIDs = self.buffs[self.elements.index(currType)]
			for buffID in currBuffIDs:
				entity.removeBuffByID(int(buffID))
		if elements:
			attributeType = elements[random.randint(0, len(elements) - 1)]
			entity.setTemp("attributeType", attributeType)
			spaceEntity = entity.getCurrentSpace()
			#添加新的Buff
			index = self.elements.index(attributeType)
			for role in spaceEntity._spaceRoles:
				role.client.CLIENT_WXHJChangeAttr( index )
			buffs = self.buffs[index]
			for buffID in buffs:
				entity.addBuff(entity, int(buffID))
		else:
			entity.removeTemp("attributeType")
			
class AIAction157(AIActionBase.AIActionBase):
	"""
	机关根据当前属性向目标释放技能（CST-3790）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.skillIDList = []
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.elements = section["param1"].split("|")		#机关属性
		skillIDs = [ int(skillID) for skillID in section["param2"].split("|") ]	#技能ID
		for skillID in skillIDs:
			if self.checkSkillIsExit( skillID ):
				self.skillIDList.append( skillID )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity	
		"""
		if len(self.elements) !=len(self.skillIDList):
			KBEDebug.ERROR_MSG("AIAction157: skillIDList or elements config error!")
			return
		curAttributeType = entity.queryTemp("attributeType", None)
		if not curAttributeType:
			return
		if curAttributeType not in self.elements:
			KBEDebug.ERROR_MSG("AIAction157: elements config error!")
			return
		if curAttributeType in self.elements:
			index = self.elements.index(curAttributeType)
			skillID = self.skillIDList[index]
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [skillID, entity.getTargetID(), False])
		else:
			KBEDebug.ERROR_MSG("AIAction157: curAttributeType: %s is not in config elements: %s !" % (curAttributeType, self.elements))

class AIAction158(AIActionBase.AIActionBase):
	"""
	根据画卷当前属性在指定位置刷一个entity（CST-3790）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.elements = section["param1"].split("|")		#机关属性
		self.scriptIDList = section["param2"].split("|")	#分身scriptID
		self.position = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(section["param3"]))	#位置
		self.direction = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(section["param4"]))	#朝向
		self.signs = set(section["param5"].strip().split("|"))	#标记
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity	
		"""
		if len(self.elements) !=len(self.scriptIDList):
			KBEDebug.ERROR_MSG("AIAction158: scriptIDList or elements config error!")
			return
		curAttributeType = entity.queryTemp("attributeType", None)
		if not curAttributeType:
			return
		if curAttributeType not in self.elements:
			KBEDebug.ERROR_MSG("AIAction158: elements config error!")
			return
		scriptID = self.scriptIDList[self.elements.index(curAttributeType)]
		newEntity = entity.createEntityByScriptID(scriptID, Math.Vector3(self.position), self.direction, {"spawnPos":Math.Vector3( self.position ),"spawnDir": self.direction})
		newEntity.signs = newEntity.signs|self.signs

class AIAction159(AIActionBase.AIActionBase):
	"""
	根据机关属性设置画卷属性（CST-3790）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.scriptID = section["param1"]		#机关scriptID
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity	
		"""
		entityIDList = entity.getCurrentSpace().getEntityRecord(self.scriptID)
		if len(entityIDList) != 1:
			KBEDebug.ERROR_MSG("AIAction159: entity[%s] is none or not the only one!" % self.scriptID)
			return
		gearEntity = KBEngine.entities.get(entityIDList[0], None)
		if gearEntity and gearEntity.queryTemp("attributeType", None):
			entity.setTemp("attributeType", gearEntity.queryTemp("attributeType"))

class AIAction160(AIActionBase.AIActionBase):
	"""
	创建贴图（CST-3790）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.elements = section["param1"].split("|")		#属性
		self.scriptIDList = section["param2"].split("|")		#贴图scriptID
		self.effectIDList = section["param3"].split("|")		#效果ID
		self.position = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(section["param4"]))	#位置
		self.direction = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(section["param5"]))	#朝向
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity	
		"""
		if entity.queryTemp("chartletType", None):
			KBEDebug.ERROR_MSG("AIAction160: Picture scroll[%s] has already had chartlet" % entity.scriptID)
			return
		attributeType = entity.queryTemp("attributeType")
		if not attributeType:
			KBEDebug.ERROR_MSG("AIAction160: Picture scroll[%s] is Empty" % entity.scriptID)
			return
		if attributeType not in self.elements:
			KBEDebug.ERROR_MSG("AIAction160: config error: [%s] is not in config elements" % attributeType)
			return
		index = self.elements.index(attributeType)
		scriptID = self.scriptIDList[index]
		effectID = self.effectIDList[index]
		newEntity = entity.createEntityByScriptID(scriptID, Math.Vector3(self.position), self.direction, {"spawnPos":Math.Vector3( self.position ), "spawnDir": self.direction, "effectID": effectID})
		if newEntity:
			entity.setTemp("chartletType", str(newEntity.id))
			#newEntity.displayChartlet(effectID)

class AIAction161(AIActionBase.AIActionBase):
	"""
	销毁贴图（CST-3790）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.disappearType = int(section["param1"])		#1 逐渐消失, 2 扭成一团后消散
		
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity	
		"""
		if not entity.queryTemp("chartletType", None):
			KBEDebug.ERROR_MSG("AIAction161: Picture scroll[%s] has not chartlet" % entity.scriptID)
			return
		id = int(entity.queryTemp("chartletType"))
			
		newEntity = KBEngine.entities.get(id, None)
		if newEntity:
			entity.removeTemp("chartletType")
			newEntity.disappearChartlet(self.disappearType)
	
class AIAction162(AIActionBase.AIActionBase):
	"""
	将一定范围内离自己最近的指定entity作为AI目标 没有状态限制
	如果不填参数scriptID,则不进行此参数的判断，只进行类型的判断
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []


	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.entityType = section[ "param2" ]
		if section["param3"].strip()!="":
			self.scriptIDs = section["param3"].strip().split("|")
		


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		eid = 0
		distance = 10000.0
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs, [], entity.position)
		if len(self.scriptIDs):
			entities = [e for e in entities if e.scriptID in self.scriptIDs]
		for e in entities:													# 选择最近目标的ID
			dis = entity.position.flatDistTo(e.position)
			if distance > dis:
				eid = e.id
				distance = dis
		e = KBEngine.entities.get(eid,None)
		entity.monsterAISetTarget( eid )

class AIAction163(AIActionBase.AIActionBase):
	"""
	entity关联移动平台（作用：entity在平台上移动）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptID = []
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.scriptID = [section[ "param1" ],]
		param2 = section["param2"].split("|")
		self.radius = float(param2[0])
		if len(param2)>1:
			self.height = float(param2[1])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entitys = entity.entitiesInRangeExtForAI(self.radius, self.height, "MovingPlatform", self.scriptID )
		if len(entitys) > 0:
			entity.parent = entitys[0]
			entity.spawnPos = Math.Vector3( entitys[0].positionWorldToLocal( entity.spawnPos ))
			


class AIAction164(AIActionBase.AIActionBase):
	"""
	设置血量百分比
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.hpPercent = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.hpPercent = float(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		hp = int(entity.HP_Max*self.hpPercent/100 )
		entity.setHP(hp)
		


class AIAction165(AIActionBase.AIActionBase):
	"""
	在指定坐标召唤一个朝向为面向/背向召唤者的entity。
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = None
		self.faceTo = 1    #1 :面向，-1:背向
		self.scriptID = None
		

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		
		position = Functions.vector3TypeConvert( section["param1"] )
		if position:
			self.position = KBEMath.Unreal2KBEnginePosition( position )
		if section["param2"].strip():
			self.faceTo = bool(section["param2"].strip())
		
		self.scriptID = section["param3"].strip()

	def do(self, ai, entity, triggerEntity):

		position = self.position
		p= (entity.position - position)*self.faceTo
		direction = (0.0,0.0,csarithmetic.getYawByVector3( p ))

		param = {}
		param.update( {"spawnPos":tuple(Math.Vector3(position))} )
		param.update( {"spawnDir":tuple(Math.Vector3(0.0, 0.0, direction[2]))} )

		newEntity = entity.createMonster( self.scriptID, position, direction, param )
		if not newEntity:
			KBEDebug.ERROR_MSG("createMonster failed!")

class AIAction166(AIActionBase.AIActionBase):
	"""
	主动回到气盈状态
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)	

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.gangQi_changeState( csdefine.GANG_QI_STATE_QI_YING )
		entity.gangQiValue = entity.gangQiValue_Max

class AIAction167(AIActionBase.AIActionBase):
	"""
	随机移动脚本怪随机移动
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"].strip():
			self.moveSpeed = float(section["param1"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		entity.startRandomWalkFromList(moveSpeed, isUpdateSpeed)
		
class AIAction168(AIActionBase.AIActionBase):
	"""
	CST-3855
	关闭/开启预警范围的光效显示
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.open = 0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"]:
			self.open = int(section["param1"])
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		if self.open:
			entity.openInitiativeTrapEffect()
		else:
			entity.closeInitiativeTrapEffect()

class AIAction169(AIActionBase.AIActionBase):
	"""
	以某个坐标为中心(如果没有指定则表示以自身为中心）,在一定时间、
	一定范围内，随机召唤数个entity。 entity是一个一个刷的   CST-4407
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.centerPos = None		#param1 中心点坐标	
		self.direction = None 		#param2 朝向   不填默认为怪物朝向
		self.theta = 360 			#param3 角度   不填默认为圆
		self.maxRadius = 0.0 		#param4	指定最大半径
		self.minRadius = 0.0 		#param4	指定最小半径
		self.totalTime = 0.0 		#param5 总时间
		self.number = 0 			#param5	entity的数量
		self.scriptID = ""			#param5	entity的scriptID

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )	
		#param1
		if not section["param1"].strip():
			self.centerPos = None
			position = None
		else:
			position = Functions.vector3TypeConvert( section["param1"] )
			if position is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
			else:
				self.centerPos = KBEMath.Unreal2KBEnginePosition( position )
		#param2
		if not section["param2"].strip():
			self.direction = None
		else:
			direction = Functions.vector3TypeConvert( section["param2"] )
			if position is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param2(%s)" %( self.getAIID(), section["param2"] ) )
			else:
				self.direction = KBEMath.Unreal2KBEngineDirection( direction )
		#param3
		if  section["param3"].strip():
			self.theta = int(section["param3"].strip())

		#param4
		radiusList =  section[ "param4" ].split("|")
		self.maxRadius = float(radiusList[0])
		if len(radiusList)>1:
			self.minRadius = float(radiusList[1])

		#param5
		totalTime, number, scriptID = section["param5"].strip().split("|")
		self.totalTime = float(totalTime)
		self.number = int( number )
		self.scriptID = scriptID

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""

		def getRandPosInCircle( centerPos, direction, theta, maxRadius, minRadius, entity ):
			"""
			在圆(扇形)内获得随机点坐标
			"""
			if not centerPos:
				centerPos = entity.position
			if not direction:
				direction = entity.direction

			radius = random.uniform( self.minRadius, self.maxRadius )
			radian1 = direction.z
			_theta = random.uniform(-theta/2, theta/2)
			radian2 = math.radians(_theta)
			radian3 = radian1 + radian2
			srcPos= Math.Vector3( centerPos + Math.Vector3( math.sin(radian3)*radius , 0,  math.cos(radian3)*radius ))
			return srcPos

		direction = self.direction if self.direction else entity.direction

		delayTime = 0.0
		avgTime = self.totalTime/self.number
		targetDirection = entity.direction
		for i in range(self.number):
			delayTime += avgTime
			pos = getRandPosInCircle(self.centerPos, direction, self.theta, self.maxRadius, self.minRadius, entity )
			entity.addTimerCallBack(delayTime, "createEntityByScriptID",(self.scriptID, pos, targetDirection, {"spawnPos":pos ,"spawnDir":targetDirection}))

class AIAction170(AIActionBase.AIActionBase):
	"""
	将怪物自己设置为AI目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.monsterAISetTarget( entity.id )
		
class AIAction171(AIActionBase.AIActionBase):
	"""
	重置灵脉战场Boss
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.resetBoss()

class AIAction172(AIActionBase.AIActionBase):
	"""
	自身有特定buff时则移除该buff, 没有则添加buff
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		isHasBuff = True
		for buffID in self.buffIDs:
			if not len(entity.findBuffsByBuffID( buffID )):
				isHasBuff = False		
		
		if isHasBuff:
			for buffID in self.buffIDs:
				entity.removeBuffByID(buffID)
		else:
			for buffID in self.buffIDs:
				entity.addBuff( entity, buffID )

class AIAction173(AIActionBase.AIActionBase):
	"""
	CST-4246 程序功能需求（20级）——帮会副本【九字真言】
	给玩家加上某个buff[皆真言，阵真言, 兵真言]
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity : return
		buffList = spaceEntity.getTemp("BOSSBUFF", [])
		if len(buffList):
			buffID = random.choice(buffList)
			spaceEntity.getScript().onRoleAddBuff(buffID)
		
class AIAction174(AIActionBase.AIActionBase):
	"""
	CST-4246 九字真言
	在指定位置召唤指定数量拥有自身最大血量一定百分比的怪物
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptID = ""
		self.position = None
		self.hpPercent = 100		#血量百分比
		self.amount = 0				#召唤几个怪物
		
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		
		if section["param1"].strip():
			self.scriptID = section["param1"]
		if section["param2"].strip():
			self.position = Functions.vector3TypeConvert( section["param2"] )
		if section["param3"].strip():
			hpPercent = int(section["param3"])
			self.hpPercent = hpPercent if hpPercent > 0 and hpPercent <= 100 else 100
		if section["param4"].strip():
			self.amount = int(section["param4"])
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity
		"""
		direction = entity.direction
		hp = entity.HP / 100 * self.hpPercent
		for i in range(self.amount):
			newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(self.position), direction, {"spawnPos":Math.Vector3( self.position ),"spawnDir": direction})
			newEntity.setHP(hp)

class AIAction175(AIActionBase.AIActionBase):
	"""
	释放技能或者远离
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.oddList = []		#释放技能的概率:远离的概率:游走的概率
		self.spellSkillIDs = []
		self.skillLastCount = 5.0
		self.moveSpeed = 0.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if len(section["param1"].strip()):
			self.oddList = section["param1"].strip().split("|")
		self.moveSpeed = float(section["param2"])
		if len( self.oddList ) > 0 and len( self.oddList ) < 2:
			self.oddList.append( str( 1 - float( self.oddList[0] ) ) )
		if len(section["param3"].strip()):
			skillList =[ int( skillID ) for skillID in section["param3"].strip().split("|") ]
			result = True
			for skillID in skillList:
				if not self.checkSkillIsExit( skillID ):
					result = False
					break
			if result:
				self.spellSkillIDs = skillList
			
		if len(section["param4"].strip()):
			self.skillLastCount = float(section["param4"].strip())
		

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			return
			
		targetPosition = Math.Vector3( targetEntity.position )
		if not len(self.spellSkillIDs):
			KBEDebug.ERROR_MSG("skillIDs config error!")
			return
				
		skillIDs = list( self.spellSkillIDs )
		if entity.lastRandomSkillID in skillIDs:
			skillIDs.remove( entity.lastRandomSkillID )
		if len(skillIDs) <= 0:
			return
		skillID = random.choice( skillIDs )
		if entity.monsterAISkillLastTime > 0 and (Functions.getTime() - entity.monsterAISkillLastTime)/csconst.TIME_ENLARGE_MULTIPLE < self.skillLastCount:
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [skillID, entity.getTargetID(), False ] )
			return
		randOdd = random.random()
		if randOdd < float( self.oddList[0] ):
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [skillID, entity.getTargetID(), False ] )
			entity.monsterAISkillLastTime = Functions.getTime()
		elif randOdd < float( self.oddList[0] ) + float( self.oddList[1] ) and randOdd >= float( self.oddList[0] ):
			entity.fightDisperseMove( targetEntity, csdefine.MOVING_FIGHT_DISPERSE_STYLE_AWAY, self.moveSpeed )
			entity.monsterAISkillLastTime = 0
		else:
			entity.fightDisperseMove( targetEntity, csdefine.MOVING_FIGHT_DISPERSE_STYLE_AWAY, self.moveSpeed )
		
class AIAction176(AIActionBase.AIActionBase):
	"""
	靠近或者游走
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.moveSpeed = float(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			return
		entity.onFaceToPlayer(True)
		entity.fightDisperseMove( targetEntity, csdefine.MOVING_FIGHT_DISPERSE_STYLE_WANDER, self.moveSpeed )

class AIAction177(AIActionBase.AIActionBase):
	"""
	跟随当前目标到一定范围内
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.moveSpeed = float( section["param1"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			KBEDebug.ERROR_MSG("targetEntity is not exist")
			return

		entity.fightDisperseMove( targetEntity, csdefine.MOVING_FIGHT_DISPERSE_STYLE_CHASE, self.moveSpeed )

class AIAction178(AIActionBase.AIActionBase):
	"""
	设置怪物的朝向
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		entity.allClients.CLIENT_StopSimulationCircle()

class AIAction179(AIActionBase.AIActionBase):
	"""
	创建法阵(真言对应的虚影)
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

		if section["param1"].strip():
			self.scriptID = section["param1"]
		if section["param2"].strip():
			self.position = Functions.vector3TypeConvert( section["param2"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		if entity is None:
			return
		
		entity.createSpellBox(self.scriptID, self.position, (0.0, 0.0, 0.0), {"tempMapping" : {"entityID" : entity.id}})
		
class AIAction180(AIActionBase.AIActionBase):
	"""
	真言开始腐化
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		pass

class AIAction181(AIActionBase.AIActionBase):
	"""
	激活捕鱼点(CST-4263)
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.results = []
		self.rewardID = ""
		self.monsterDict = {}
		self.bossID = ""
		self.radius = 5.0
		self.sign = ''

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"].strip():
			self.results = section["param1"].strip().split("|")
		if section["param2"].strip():
			self.rewardID = int(section["param2"].strip())
		if section["param3"].strip():
			monsterIDStr = section["param3"].strip().split("|")
			for _str in monsterIDStr:
				key ,value = _str.split(":")
				param = {key:int(value)}
				self.monsterDict.update(param)
		if section["param4"].strip():
			self.bossID = section["param4"].strip()
		self.sign = section["param5"]


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not self.results:
			return

		if self.sign in entity.signs:
			self.results = ["4"]
			
		def getRandPosInCircle( centerPos, radius, num, entity ):
			"""
			在圆内获得随机点坐标
			"""
			posList = []
			while num:
				x = centerPos[2]+random.uniform(-1,1)*radius
				y = centerPos[0]+random.uniform(-1,1)*radius
				posList.append(Math.Vector3( y, entity.position[1], x ))
				num-=1
			return posList


		def funcDoNothing():
			"""
			什么也不做
			"""
			triggerEntity.statusMessage(csstatus.ZSYG_GET_NOTHING)

		def funcReward():
			"""
			获取内丹
			"""
			triggerEntity.addItemByID(self.rewardID)

		def funcCreateMonsters():
			"""
			刷小怪
			"""
			spaceEntity = entity.getCurrentSpace()
			if not spaceEntity:
				return
			for monsterID, num in self.monsterDict.items():
				for i in range(num):
					pos = entity.position
					x = pos[2]+random.uniform(-1,1)*self.radius
					y = pos[0]+random.uniform(-1,1)*self.radius
					_pos = Math.Vector3( y, entity.position[1], x )
					_dire = (0.0,0.0,0.0)
					spaceEntity.createEntityByScriptID(monsterID, _pos, _dire,{ "spawnPos":_pos ,"spawnDir":_dire})
			entity.destroySelf()

		def funcCreateBoss():
			"""
			刷Boss
			"""
			_pos = Math.Vector3(entity.position)
			_dire = (0.0,0.0,0.0)
			spaceEntity = entity.getCurrentSpace()
			if not spaceEntity:
				return
			spaceEntity.createEntityByScriptID(self.bossID, _pos, _dire,{ "spawnPos":_pos ,"spawnDir":_dire})
			entity.destroySelf()


		doFunc = {"1":funcDoNothing, "2":funcReward, "3":funcCreateMonsters, "4":funcCreateBoss}
		result = None
		results = list(self.results)
		if "4" in results:
			bossEntity = entity.getCurrentSpace().getEntityRecord(self.bossID)
			if len(bossEntity):
				results.remove("4")
		result = random.choice(results)

		if result in doFunc.keys():
			doFunc[result]()
		else:
			KBEDebug.ERROR_MSG("key = %s is not valid!"%result)
		entity.destroySelf()	


class AIAction182(AIActionBase.AIActionBase):
	"""
	逃离或原地对目标释放技能（CST-4263）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.targetPos = (0.0, 0.0, 0.0)
		self.distance = 0.0
		self.moveSpeed = 0.0
		self.skillID = 0
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		position = Functions.vector3TypeConvert( section["param1"] )
		if position is None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
		else:
			self.targetPos = KBEMath.Unreal2KBEnginePosition( position )
		self.distance = float(section["param2"])
		self.moveSpeed = float(section["param3"])
		tskillID = int(section["param4"])
		if self.checkSkillIsExit( tskillID ):
			self.skillID = tskillID

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		target = KBEngine.entities.get(entity.getTargetID(), None)
		if not target:
			return
		
		if self.skillID == 0:
			return
			
		if entity.position.flatDistTo(target.position) > self.distance:
			behType = csdefine.BEHAVIOUR_TYPE_MOVING
			if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
				moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
			else:
				moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
			
			(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
			
			moveArgs = [ Math.Vector3(self.targetPos) ]
			entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )
		else:
			self.behControlReset(csdefine.BEHAVIOUR_TYPE_MOVING)
			behType = csdefine.BEHAVIOUR_TYPE_SPELL
			entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.skillID, entity.getTargetID(),False])


class AIAction183(AIActionBase.AIActionBase):
	"""
	头顶冒泡（说话气泡)
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.voice = ""
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.voice = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		entity.allClients.CLIENT_onPlaySpeechBubbles( self.voice )


class AIAction184(AIActionBase.AIActionBase):
	"""
	模型持续改变
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.extraScale = 0.0
		self.tickTime = 0.5
		self.maxScale = 0.0
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.extraScale = float(section["param1"])
		self.tickTime = float(section["param2"])
		self.maxScale = float(section["param3"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		entity.setMaxModelScale(self.maxScale)
		entity.keepChangeModelScaleTimerID =  entity.addTimerRepeat(self.tickTime, "keepChangeModelScale", (self.extraScale,))


class AIAction185(AIActionBase.AIActionBase):
	"""
	一定范围内的玩家震屏
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0.0 	   #半径
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.intensity = 0.0   #震动强度
		self.rate = 0.0        #震动增量
		self.time = 0.0 	   #震动时间
		self.priority = 0      #优先级
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.intensity = float(section["param2"])
		self.rate = float(section["param3"])
		self.time = float(section["param4"])
		if section["param5"]:
			self.priority = int(section["param5"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, "Role", [], [], entity.position)

		for player in entities:
			player.client.RoleCameraShake(self.intensity, self.rate, self.time, self.priority)
			
class AIAction186(AIActionBase.AIActionBase):
	"""
	CST-4246 九字真言
	给拥有指定buff的monster随机选一个发送指令
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptIDs = []
		self.buffID = 0
		self.commandID = ""
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.scriptIDs = section["param1"].split('|')
		self.buffID = int(section["param2"])
		self.commandID = section["param3"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		
		temp = []
		entities = []
		for scriptID in self.scriptIDs:
			entities.extend(spaceEntity.getEntityRecord(scriptID))

		for id in entities:
			e = KBEngine.entities.get(id)
			if e and e.findBuffsByBuffID(self.buffID):
				temp.append(e)
		
		if len(temp):
			e = random.choice(temp)
			e.monsterAISendCommand(e.id, self.commandID)
		

class AIAction187(AIActionBase.AIActionBase):
	"""
	CST-4246 九字真言
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		pass
		
class AIAction188(AIActionBase.AIActionBase):
	"""
	CST-4246 九字真言
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""	
		pass

class AIAction189(AIActionBase.AIActionBase):
	"""
	显示怪物血条界面,根据所在副本显示不同界面 CST-5157
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.isOpen = bool(int(section["param1"]))   #开关 0：关闭 1打开

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		if not entity:
			return
		if triggerEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		if not self.isOpen:
			triggerEntity.client.ShowCircleHPPercentBar( 0, 0 )
			return
		percent = int(math.floor(entity.HP/entity.HP_Max*100))
		triggerEntity.client.ShowCircleHPPercentBar( self.isOpen, percent )

class AIAction190(AIActionBase.AIActionBase):
	"""
	一定范围内的玩家震屏，显示怪物血条界面 CST-5157
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.isOpen = bool(int(section["param1"]))   #开关 0：关闭 1打开
		self.radius = float(section["param2"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		entities = entity.entitiesInRangeExtCircle( self.radius, "Role", entity.position )
		percent = int(math.floor(entity.HP/entity.HP_Max*100))
		for player in entities:
			player.client.ShowCircleHPPercentBar( self.isOpen, percent )


class AIAction191(AIActionBase.AIActionBase):
	"""
	通过效果脚本名移除目标身上buff
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.effectName = section["param1"]		

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		AITargetEntity = entity.monsterAIGetTargetEntity()
		if not AITargetEntity:
			return
		
		AITargetEntity.removeBuffByEffect( self.effectName )

class AIAction192( AIActionBase.AIActionBase ):
	"""
	向某个方向移动（前：1，后：2，左：3，右：4）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._velocity = 0.0						# 移速
		self._dire = 0								# 方向
		self._distance = 0.0						# 距离
		self._bFaceMove = 1							# 移动时，朝向是否为移动方向

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._velocity = section["param1"] and float( section["param1"]) or 0.0
		self._dire = section["param2"] and int( section["param2"]) or 0
		self._distance = section["param3"] and float( section["param3"]) or 0.0
		self._bFaceMove = section["param4"] and int( section["param4"]) or 1

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self._velocity:
			speed = self._velocity
			isUpdateSpeed = False
		else:
			speed = entity.getSpeed()
			isUpdateSpeed = True
			
		if self._dire == 1:
			yaw = entity.getYaw()
		elif self._dire == 2:
			yaw = entity.getYaw() + math.pi
		elif self._dire == 3:
			yaw = entity.getYaw()- math.pi / 2
		elif self._dire == 4:
			yaw = entity.getYaw() + math.pi / 2
			
		dstPos = Math.Vector3( entity.position.x + self._distance * math.sin(yaw), entity.position.y, entity.position.z + self._distance * math.cos(yaw) )
		#加行为
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
		moveArgs = [ Math.Vector3(dstPos), 0.0, self._bFaceMove ]
		entity.behAdd( behType, [ moveScriptID, speed, isUpdateSpeed,  moveArgs ] )

class AIAction193(AIActionBase.AIActionBase):
	"""
	刷新场景物件条件
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )		

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		AITargetEntity = entity.monsterAIGetTargetEntity()
		if not AITargetEntity:
			return
		
		entityList = AITargetEntity.entitiesInView()
		for entity in entityList:
			if entity.getEntityFlag() == csdefine.ENTITY_FLAG_SPELL:
				entity.requestRefreshCondition( entity, AITargetEntity )

class AIAction194( AIActionBase.AIActionBase ):
	"""
	英雄王座小兵  呼叫同一波小兵
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		#如果自身处于呼叫状态中，则不能呼叫别人
		if entity.callSign:
			KBEDebug.DEBUG_MSG("entity id = %d is called,can't call others!"%entity.id)
			return
		else:
			entity.callSign = True

		spaceEntity = entity.getCurrentSpace()
		if spaceEntity:
			es = spaceEntity.getEntityMailBoxByPatrolListAndNumber( entity.way, entity.number )
			for e in es:
				e.onFightCall( entity.getTargetID())

		
class AIAction195(AIActionBase.AIActionBase):
	"""
	AI目标给自身增加Buff
	
	param1：BuffID，支持多个，以竖号分隔，表示且；


	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.buffIDs =  [int(buffID) for buffID in section["param1"].strip().split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		AITargetEntity = entity.monsterAIGetTargetEntity()
		if not AITargetEntity:
			return
		for buffID in self.buffIDs:
			AITargetEntity.addBuff( AITargetEntity, buffID )

class AIAction196(AIActionBase.AIActionBase):
	"""
	专属怪以某个坐标为中心(如果没有指定则表示以自身为中心），在一定范围内(圆内或者圆上)随机召唤数个拥有创建者entity。
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.isJudge = []
		self.centerPos = None	#param1 中心点坐标	
		self.radius = 0.0 		#param2	指定半径
		self.isAtTheCircle = False #param3 是否在圆上
		self.isHasFlag = False  #param3是否是浮空召唤
		self.number = 0 		#param3	entity的数量
		self.scriptID = ""		#param4	entity的scriptID

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )	
		if not section["param1"].strip():
			self.centerPos = None
		else:
			position = Functions.vector3TypeConvert( section["param1"] )
			if position is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
			else:
				self.centerPos = KBEMath.Unreal2KBEnginePosition( position )
		
		self.radius = float(section[ "param2" ])

		if len(section["param3"]):
			self.isJudge = [int(x) for x in section["param3"].split("|")]
			self.isAtTheCircle = bool(int(self.isJudge[0]))
			if len(self.isJudge) > 1:
				self.isHasFlag = bool(int(self.isJudge[1]))

		self.number = int( section[ "param4" ] )
		self.scriptID = section[ "param5" ]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""

		def getRandPosInCircle( centerPos, radius, num, entity ):
			"""
			在圆内获得随机点坐标
			"""
			posList = []
			while num:
				x = centerPos[2]+random.uniform(-1,1)*radius
				y = centerPos[0]+random.uniform(-1,1)*radius
				posList.append(Math.Vector3( y, entity.position[1], x ))
				num-=1
			return posList

		def getRandPosAtTheCircle( centerPos, radius, num, entity ):
			"""
			在圆边缘上获得随机点坐标
			"""
			PIE = 3.1415926
			radian = PIE*2/num
			posList = []
			while num:
				x = centerPos[2]+radius*math.cos(radian*num)
				y = centerPos[0]+radius*math.sin(radian*num)
				posList.append(Math.Vector3( y, entity.position[1], x ))
				num-=1
			return posList

		posList = []
		if not self.centerPos:
			centerPos = Math.Vector3( entity.position )
		else:
			centerPos = Math.Vector3( self.centerPos )
		if self.isAtTheCircle:
			posList = getRandPosAtTheCircle( centerPos, self.radius, self.number, entity )
		else:
			posList = getRandPosInCircle( centerPos, self.radius, self.number, entity )
		
		targetDirection = Math.Vector3(0.0, 0.0, entity.direction.z)
		for targetPosition in posList:
			tarPosition = KBEngine.collideVertical( entity.spaceID, entity.layer, targetPosition, 10, - 10 )
			if self.isHasFlag:
				newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(targetPosition), targetDirection,{ "spawnPos":Math.Vector3( targetPosition ) ,"spawnDir":Math.Vector3( targetDirection ),"creatorDBID":entity.creatorDBID})
			elif tarPosition:
				newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(tarPosition[0]), targetDirection,{ "spawnPos":Math.Vector3( tarPosition[0] ) ,"spawnDir":Math.Vector3( targetDirection ),"creatorDBID":entity.creatorDBID})

class AIAction197(AIActionBase.AIActionBase):
	"""
	金树种子:计算收获金树的奖励  CST-5772
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )	
		self.StageList  = [int(i) for i in section["param2"].split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		def calcRewards( n,  percent):
			k = 0
			v = 0
			while k < n and k<len(self.StageList):
				v += self.StageList[k]*25
				k += 1
			v += self.StageList[k] * (v%25)
			return v
		percent = int((entity.HP * 1.0 / entity.HP_Max ) * 100)
		rewards = calcRewards(int(percent/25), percent)
		triggerEntity.addMoney(rewards, csdefine.EXP_ADD_REASON_SPACE_SENTLEMENT)

class AIAction198(AIActionBase.AIActionBase):
	"""
	魔像水晶：执行点击逻辑
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.delaySecond = Const.NPC_DESTORY_SELF

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.successID = section["param1"]
		self.failID = section["param2"]
		self.delaySecond = float(section["param3"])
			
				
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		monsterIDs = triggerEntity.queryTemp( "ClickMonsterIDs_MXSJ", [] )	#用列表记录，放置怪物再点击作判断后，还被点击了
		if not monsterIDs:
			triggerEntity.setTemp( "ClickMonsterIDs_MXSJ", [entity.id] )
			return
		else:
			monsterID = monsterIDs[-1]
			if monsterID == entity.id:return			# 点击相同的怪物不处理
			monsterIDs.append(entity.id)
			triggerEntity.setTemp( "ClickMonsterIDs_MXSJ", monsterIDs )
			
			if len(monsterIDs) % 2 == 0:				# 偶数才执行判断
				monster = KBEngine.entities.get( monsterID )
				spaceEntity = entity.getCurrentSpace()
				result = 0
				if monster and spaceEntity:
					if monster.modelNumber == entity.modelNumber:
						spaceEntity.getScript().onConditionChange( spaceEntity, "AI", entity.scriptID, self.successID, "" )
						entity.delayDestroy(self.delaySecond)
						monster.delayDestroy(self.delaySecond)
						entity.monsterAISendCommand(entity.id, self.successID)
						entity.monsterAISendCommand(monster.id, self.successID)
						result = 1
					else:
						spaceEntity.getScript().onConditionChange( spaceEntity, "AI", entity.scriptID, self.failID, "" )
						entity.monsterAISendCommand(entity.id, self.failID)
						entity.monsterAISendCommand(monster.id, self.failID)
						
						idList = list( spaceEntity.getEntityRecord( entity.scriptID ) )
						for id in idList:
							ent = KBEngine.entities.get( id )
							if not ent:
								continue
							if ent.id == entity.id:
								continue
							ent.delayDestroy(self.delaySecond)
						idList = list( spaceEntity.getEntityRecord( monster.scriptID ) )
						for id in idList:
							ent = KBEngine.entities.get( id )
							if not ent:
								continue
							if ent.id == monster.id:
								continue
							ent.delayDestroy(self.delaySecond)
				if triggerEntity.isEntityFlag(csdefine.ENTITY_FLAG_ROLE):
					triggerEntity.client.CLIENT_OnMatchMXSJResult( result )

class AIAction199(AIActionBase.AIActionBase):
	"""
	阴兵特殊追击
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.isNear = 1 			#是否靠近
		self.radius = 10.0 			#自身到目标的距离为圆的半径 在圆上随机生成一个可移动点
		self.actionID = "" 			#追击动作
		self.moveTime = 0.0 		#移动时间
		self.posList = [] 			#可移动区域

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.isNear = bool(int(section["param1"]))
		self.radius = float(section["param2"])
		self.actionID = section["param3"]
		self.moveTime = float(section["param4"])
		if section["param5"]:
			posList1 = [Functions.vector3TypeConvert(pos) for pos in section["param5"].split("|")]
			posList2 = [KBEMath.Unreal2KBEnginePosition(pos) for pos in posList1]
			self.posList = [Math.Vector3(pos) for pos in posList2]
				
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		aiTargetEntity = KBEngine.entities.get( entity.getTargetID(), None )
		if not aiTargetEntity:
			return
		targetPos = aiTargetEntity.position
		_radius = self.radius
		if self.isNear:
			#_radius = abs(entity.position.flatDistTo(targetPos) - self.radius)
			entity.monsterAppearLineToPoint_chase(targetPos, self.posList, self.actionID, _radius, self.moveTime)
		else:
			entity.monsterAppearLineToPoint_retreat(targetPos, self.posList, self.actionID, _radius, self.moveTime)

class AIAction200(AIActionBase.AIActionBase):
	"""
	将一定范围内的所有玩家闪现到当前地图的某个坐标并加上定身BUFF
	Param1：半径，单位米
	Param2: buffID
	Param3：position，以空格分隔
	Param4：direction，以空格分隔

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = None
		self.direction = None
		self.buffID = 0
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])

		self.buffID = int(section["param2"])

		position = Functions.vector3TypeConvert( section["param3"] )
		if not position:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param3(%s)" %( self.getAIID(), section["param3"] ) )
		else:
			self.position = KBEMath.Unreal2KBEnginePosition( position )

		direction = Functions.vector3TypeConvert( section["param4"] )
		if direction==None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param4(%s)" %( self.getAIID(), section["param4"] ) )
		else:
			self.direction = KBEMath.Unreal2KBEngineDirection( direction )


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""		
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, "Role" )
		if self.position == None or self.direction == None :
			return	
		for e in entities:
			e.addBuff( e, self.buffID)
			e.changeDirection(self.direction, csdefine.REASON_CHANGE_DIR_VOLUNTARY)
			e.allClients.TeleportToDstPosition( KBEMath.KBEngine2UnrealPosition(self.position))

class AIAction201(AIActionBase.AIActionBase):
	"""
	AI目标玩家显示界面并播放语音（多个语音中随机播放其中一条）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.voiceIDList = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.voiceIDList = section["param1"].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		soundID = random.choice( self.voiceIDList )
		targetEntity = KBEngine.entities.get(entity.monsterAIGetTarget(),None)
		if targetEntity and targetEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and targetEntity.getState() != csdefine.ENTITY_STATE_PEAD \
		and targetEntity.getState() != csdefine.ENTITY_STATE_DEAD and not targetEntity.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):
			entity.monsterAIShowMessagePlaySound( targetEntity, soundID )

class AIAction202(AIActionBase.AIActionBase):
	"""
	以某个坐标并且距离自身多高为中心(如果没有指定则表示以自身为中心），在一定范围内(圆内或者圆上)随机召唤数个entity。 位置随机，entity类型可以是monster，npc,陷阱

	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.isJudge = []
		self.centerPos = None		#param1 中心点坐标	
		self.radius = 0.0 			#param2	指定半径
		self.isAtTheCircle = False  #param3 是否在圆上
		self.isHasFlag = False  	#param3 是否是浮空召唤
		self.highly = 0.0			#param3 高度
		self.number = 0 			#param4	entity的数量
		self.scriptID = ""			#param5	entity的scriptID

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )	
		if not section["param1"].strip():
			self.centerPos = None
		else:
			position = Functions.vector3TypeConvert( section["param1"] )
			if position is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
			else:
				self.centerPos = KBEMath.Unreal2KBEnginePosition( position )
		
		self.radius = float(section[ "param2" ])

		if len(section["param3"]):
			self.isJudge = [int(x) for x in section["param3"].split("|")]
			self.isAtTheCircle = bool(self.isJudge[0])
			if len(self.isJudge) > 1:
				self.isHasFlag = bool(self.isJudge[1])
			if len(self.isJudge) > 2:
				self.highly = float(self.isJudge[2])

		self.number = int( section[ "param4" ] )

		self.scriptID = section[ "param5" ]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""

		def getRandPosInCircle( centerPos, radius, num, entity ):
			"""
			在圆内获得随机点坐标
			"""
			posList = []
			while num:
				x = centerPos[2]+random.uniform(-1,1)*radius
				y = centerPos[0]+random.uniform(-1,1)*radius
				posList.append(Math.Vector3( y, entity.position[1]+ self.highly, x ))
				num-=1
			return posList

		def getRandPosAtTheCircle( centerPos, radius, num, entity ):
			"""
			在圆边缘上获得随机点坐标
			"""
			PIE = 3.1415926
			radian = PIE*2/num
			posList = []
			while num:
				x = centerPos[2]+radius*math.cos(radian*num)
				y = centerPos[0]+radius*math.sin(radian*num)
				posList.append(Math.Vector3( y, entity.position[1]+ self.highly, x ))
				num-=1
			return posList

		posList = []
		if not self.centerPos:
			centerPos = Math.Vector3( entity.position )
		else:
			centerPos = Math.Vector3( self.centerPos )
		if self.isAtTheCircle:
			posList = getRandPosAtTheCircle( centerPos, self.radius, self.number, entity )
		else:
			posList = getRandPosInCircle( centerPos, self.radius, self.number, entity )

		targetDirection = Math.Vector3( entity.direction )
		for targetPosition in posList:
			tarPosition = KBEngine.collideVertical( entity.spaceID, entity.layer, targetPosition, 10, - 10 )
			if self.isHasFlag:
				newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(targetPosition), targetDirection,{ "spawnPos":Math.Vector3( targetPosition ) ,"spawnDir":Math.Vector3( targetDirection )})
			elif tarPosition:
				newEntity = entity.createEntityByScriptID(self.scriptID, Math.Vector3(tarPosition[0]), targetDirection,{ "spawnPos":Math.Vector3( tarPosition[0] ) ,"spawnDir":Math.Vector3( targetDirection )})



class AIAction203(AIActionBase.AIActionBase):
	
	#修改怪物的主动攻击范围
	
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.attackTrapShape = 1		#1：圆形2：方形
		self.attackRange = ""			#大小:单位 米

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.attackTrapShape = int(section["param1"])
		self.attackRange = section["param2"]
	def do(self, ai, entity, triggerEntity):
		
		#vitural method
		#@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		#@type	ai		:	AIInstanceBase
		#@param	entity	: 	执行此AICondition的entity
		#@type	entity	:	entity
		
		entity.monsterAICancelAttackTrap()	#取消之前的主动攻击陷阱
		entity.attackRange = float(self.attackRange)
		entity.attackTrapShape = self.attackTrapShape
		entity.monsterAIAddAttackTrap()

class AIAction204(AIActionBase.AIActionBase):
	"""
	CST-6262 蟠龙秘境 随机某范围选择玩家移动过去
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0.0
		self.centerPos = None

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.radius = float( section["param1"] )
		if section["param2"]:
			position = Functions.vector3TypeConvert( section["param1"] )
			if position is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param2"] ))
			else:
				self.centerPos = KBEMath.Unreal2KBEnginePosition( position )

	def do(self, ai, entity, triggerEntity):
		
		#vitural method
		#@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		#@type	ai		:	AIInstanceBase
		#@param	entity	: 	执行此AICondition的entity
		#@type	entity	:	entity
		if self.centerPos == None:
			pos = entity.position
		else:
			pos = self.centerPos
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		roleList = []
		for role in spaceEntity._spaceRoles:
			if role.position.flatDistTo(pos) <= self.radius:
				roleList.append( role )
		if not len(roleList):
			return
		role = random.choice( roleList )
		dstPos = Math.Vector3( role.position )
		entity.setTemp( "dstPos",dstPos )
		entity.moveToPosition( dstPos )

class AIAction205(AIActionBase.AIActionBase):
	"""
	triggerEntity 对该怪释放技能
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.skillID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.skillID = int(section["param1"])

	def do(self, ai, entity, triggerEntity):
		
		#vitural method
		#@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		#@type	ai		:	AIInstanceBase
		#@param	entity	: 	执行此AICondition的entity
		#@type	entity	:	entity
		if triggerEntity :
			if not triggerEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				triggerEntity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [self.skillID, entity, False])
			else:
				triggerEntity.useSkillToEntity(self.skillID, entity.id)


class AIAction206(AIActionBase.AIActionBase):
	"""
	防重叠追击
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.chaseDistance = 2.0
		self.chaseAngle = 30

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.chaseDistance = float(section["param1"])
		if section["param2"]:
			self.chaseAngle = float(section["param2"])
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			KBEDebug.ERROR_MSG("targetEntity is not exist")
			return
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		entity.circleChaseDistance = self.chaseDistance
		entity.circleChaseAngle = self.chaseAngle
		#entity.stopMoving(csdefine.MOVE_TYPE_STOP)
		moveArgs = (targetEntity.id, entity.circleChaseDistance)
		entity.behAdd( behType, [ csdefine.MOVE_TYPE_CHASE_CLIENT, entity.getSpeed(), True, moveArgs ] )

class AIAction207(AIActionBase.AIActionBase):
	"""
	停止移动
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.stopMovingForType(csdefine.SYSTEM_MOVE)

class AIAction208(AIActionBase.AIActionBase):
	"""
	在该怪物出生点位置创建一个怪物
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._scriptID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._scriptID = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.createEntityByScriptID( self._scriptID, Math.Vector3(entity.spawnPos), Math.Vector3(0.0, 0.0, entity.spawnDir.z), {"spawnPos":Math.Vector3( entity.spawnPos ),"spawnDir": Math.Vector3(entity.spawnDir)})

class AIAction209(AIActionBase.AIActionBase):
	"""
	在一个小圆外另一个大圆内的环形范围以一定速度随机移动
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._minRadius = 0
		self._maxRadius = 0
		self._position = Math.Vector3(0.0, 0.0, 0.0)
		self.moveSpeed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self._minRadius = float(section["param1"])
		self._maxRadius = float(section["param2"])
		position = Functions.vector3TypeConvert( section["param3"] )
		if position is None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param3(%s)" %( self.getAIID(), section["param2"] ) )
		else:
			self._position = KBEMath.Unreal2KBEnginePosition( position )
		if section["param4"].strip():
			self.moveSpeed = float(section["param4"].strip())

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		pos = csarithmetic.getPositionByByLinks( self._position, self._minRadius, self._maxRadius )
		#加行为
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
			
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		moveArgs = [ Math.Vector3(pos) ]
		entity.behAdd( behType, [ moveScriptID, moveSpeed, isUpdateSpeed, moveArgs ] )

class AIAction210(AIActionBase.AIActionBase):
	"""
	让战斗列表内的玩家完成任务目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.questID = 0
		self.questTargetID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.questID = int(section["param1"])
		self.questTargetID = int(section["param2"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.enemyList:			
			for enemyID in entity.enemyList.keys():
				targetEntity = KBEngine.entities.get( enemyID, None )
				if targetEntity:
					targetEntity.questTaskIncreaseState( self.questID, self.questTargetID )

class AIAction211(AIActionBase.AIActionBase):
	"""
	妖卫追击
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.chase()


class AIAction212(AIActionBase.AIActionBase):
	"""
	妖卫最近点巡逻
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.route = -1
		self.pointIndex = 0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"]:
			self.route = int(section["param1"])
		if section["param2"]:
			self.pointIndex = int(section["param2"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		route = self.route if self.route!= -1 else entity.patrolRoute
		pointIndex = 0
		patrolRouteInfo = entity.getCurrentSpacePatrolnfo( route )

		if 0 != self.pointIndex:
			spaceEntity = entity.getCurrentSpace()
			if not spaceEntity:
				return
			routeData = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute(spaceEntity.scriptID, route)
			if routeData:
				routePoints = PatrolRouteLoader.g_patrolRouteLoader.getRoutePoints(routeData)
				if self.pointIndex in routePoints:
					pointIndex = self.pointIndex
				else:
					KBEDebug.ERROR_MSG("routPoint = %d not in route = %d"%(self.pointIndex, route))
					return
		else:
			nearestPoint = PatrolRouteLoader.g_patrolRouteLoader.getNearestRoutePoint(entity.getCurrentSpaceScriptID(), route,Math.Vector3(entity.position))
			if nearestPoint:
				pointIndex = nearestPoint
			else:
				KBEDebug.ERROR_MSG("AIActions212 can't find nearestPoint!")
				return
		entity.patrolRoute = route
		entity.patrol(patrolRouteInfo, pointIndex)

class AIAction213(AIActionBase.AIActionBase):
	"""
	怪物反向巡逻
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.route = -1			# 巡逻路线ID
		self.moveSpeed = 0.0	# 速度
		self.accVelocity = 0.0	# 加速度

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"].strip():
			self.route = int(section["param1"].strip())
		if section["param2"].strip():
			self.moveSpeed = float(section["param2"].strip())
		if section["param3"]:	#加速度
			self.accVelocity = float(section["param3"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""
		if self.route == -1:
			KBEDebug.ERROR_MSG("AIActions213 can't find route!")
			return
		targetEntity = KBEngine.entities.get( entity.monsterAIGetTarget(), None )
		if not targetEntity:
			KBEDebug.ERROR_MSG("targetEntity is not exist")
			return

		pointIndex = 0 # 最近点索引
		patrolRouteInfo = entity.getCurrentSpacePatrolnfo( self.route )
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed > 0 else (entity.getSpeed(), True)
		nearestPoint = PatrolRouteLoader.g_patrolRouteLoader.getNearestRoutePoint( entity.getCurrentSpaceScriptID(), self.route, Math.Vector3(entity.position) )
		if nearestPoint:
			pointIndex = nearestPoint
		else:
			KBEDebug.ERROR_MSG("AIActions213 can't find nearestPoint!")
			return

		entity.patrolRoute = self.route
		nodeInfo = patrolRouteInfo.get( pointIndex + 1 ) # 取出当前点的下一个巡逻点信息
		nodePosition = Math.Vector3( nodeInfo[ "position" ] )	# 取出坐标点
		if nodePosition.flatDistTo(targetEntity.position) > nodePosition.flatDistTo( entity.position ):
			entity.startPatrol( moveSpeed, isUpdateSpeed, ( patrolRouteInfo, pointIndex + 1, csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION, self.accVelocity ) )
		else:
			if pointIndex == 1: # 如果最近点是第一点，取末位的点:
				entity.startReversePatrol( moveSpeed, isUpdateSpeed, ( patrolRouteInfo,  max(patrolRouteInfo.keys()), csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION, self.accVelocity ) )
			else:
				entity.startReversePatrol( moveSpeed, isUpdateSpeed, ( patrolRouteInfo, pointIndex - 1, csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION, self.accVelocity ) )	

class AIAction214(AIActionBase.AIActionBase):
	"""
	小地图显示怪物位置的点变成闪烁的点
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.isTwink = int(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.allClients.ShowMonsterLocationTwinkle( self.isTwink )

class AIAction215(AIActionBase.AIActionBase):
	"""
	开启透视 放在进入主动反应陷阱事件中
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.maxDis = 50.0
		self.minDis = 0.0
		self.maxheight = 30.0


	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"]:
			self.maxDis = float(section["param1"])
		if section["param2"]:
			self.minDis = float(section["param2"])
		if section["param3"]:
			self.maxheight = float(section["param3"])


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if triggerEntity.getEntityFlag()!=csdefine.ENTITY_FLAG_ROLE:
			return
		triggerEntity.client.CLIENT_AddPerspectiveTarget(entity.id, self.maxDis, self.minDis, self.maxheight)


class AIAction216(AIActionBase.AIActionBase):
	"""
	关闭透视 放在离开主动反应陷阱事件中
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.maxDis = 50.0
		self.minDis = 0.0
		self.maxheight = 30.0


	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"]:
			self.maxDis = float(section["param1"])
		if section["param2"]:
			self.minDis = float(section["param2"])
		if section["param3"]:
			self.maxheight = float(section["param3"])


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if triggerEntity.getEntityFlag()!=csdefine.ENTITY_FLAG_ROLE:
			return
		triggerEntity.client.CLIENT_RemovePerspectiveTarget(entity.id, self.maxDis, self.minDis, self.maxheight)

class AIAction217(AIActionBase.AIActionBase):
	"""
	CST-7419 金树种子 通知界面显示成长度
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.value = 0.0	# 成长度值

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.value = int(section["param1"].strip())	# 成长度值

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity:
			for role in spaceEntity._spaceRoles:
				if role.getClient():
					role.client.ShowJSZZGrowthDegree(self.value)


class AIAction218(AIActionBase.AIActionBase):
	"""
	CST-7682 程序需求——根据战斗关系显示血条和关闭
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )


	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not triggerEntity:
			return
		if not triggerEntity.getEntityFlag()== csdefine.ENTITY_FLAG_ROLE:
			return
		if triggerEntity.id in entity.enemyList:
			#玩家敌对列表中，开启血条显示
			triggerEntity.client.CLIENT_ShowHPPercentAboveQuestBar(entity.id)
		else:
			triggerEntity.client.CLIENT_CloseHPPercentAboveQuestBar()

class AIAction219(AIActionBase.AIActionBase):
	"""
	移动到某个坐标 忽略导航
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.movePosition = None

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		position = Functions.vector3TypeConvert( section["param1"] )
		if position is None:
			KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
		else:
			self.movePosition = KBEMath.Unreal2KBEnginePosition( position )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.moveToPosition( Math.Vector3( self.movePosition ) )

class AIAction220(AIActionBase.AIActionBase):
	"""
	朝向顺时针旋转N°
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.angle = Math.Vector3(0, 0, 0)	#旋转角度
		
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"].strip():
			self.angle = float(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AIAction的entity
		@type	entity	:	entity
		"""
		direction = Math.Vector3(entity.direction)
		direction = list(KBEMath.KBEngine2UnrealDirection(direction))
		direction[2] = (direction[2] + self.angle) % 360
		direction = KBEMath.Unreal2KBEngineDirection(direction)
		entity.changeDirection(direction, csdefine.REASON_CHANGE_DIR_VOLUNTARY)
	
class AIAction221(AIActionBase.AIActionBase):
	"""
	从当前位置跳到AI目标位置
	param1: 动作ID 必填
	param2: 动作播放时间 必填
	param3: 新加参数，是否改变朝向，0：不改变，1：改变，不填：默认0
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.actionID = None
		self.playTime = None
		self.changeFlag = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.actionID = section["param1"].strip()
		self.playTime = float(section["param2"])
		if section["param3"].strip():
			self.changeFlag = int(section["param3"])

	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = entity.monsterAIGetTargetEntity()
		if not targetEntity:
			KBEDebug.ERROR_MSG("entity.id = %s: monsterAITarget is None!"%entity.id)
			return		
		targetPosition = Math.Vector3( targetEntity.position )
		
		isChangeDir = False
		if self.changeFlag == 1:
			isChangeDir = True
			
		playTime = self.playTime
		actionID = self.actionID

		entity.monsterShowEx( actionID, playTime, targetPosition, isChangeDir)

class AIAction222(AIActionBase.AIActionBase):
	"""
	CST-7929 废弃！！！
	触发对话选择界面(AI目标必须是玩家)
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.optionID = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.optionID = section["param1"]
	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = entity.monsterAIGetTargetEntity()
		if not targetEntity:
			KBEDebug.ERROR_MSG("entity.id = %s: monsterAITarget is None!"%entity.id)
			return
		optionKeys = g_optionTalkLoader.getOptionTalkDes( self.optionID )	# 获取对话选择界面的key和选项描述
		defaultOptions = g_optionTalkLoader.getDefaultOptions()		# 获取默认选项
		countDown = g_optionTalkLoader.getCountDown()		# 获取倒计时时间
		targetEntity.client.onShowDefaultOption( self.optionID, defaultOptions, float(countDown) )
		for optionKey, optionDes in optionKeys.items():
			targetEntity.client.onShowOptionTalkDes( self.optionID, optionKey, optionDes )

class AIAction223(AIActionBase.AIActionBase):
	"""
	五行怪物分身进入画卷
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]
		self.attributeType = ""
		
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.entityType = section[ "param2" ]
		self.attributeType = section["param3"]
		if section["param4"].strip()!="":
			self.scriptIDs = section["param4"].strip().split("|")
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		eid = 0
		distance = 10000.0
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs,self.removeStates )
		for e in entities:													# 选择最近目标的ID
			dis = entity.position.flatDistTo(e.position)
			if distance > dis:
				eid = e.id
				distance = dis
		e = KBEngine.entities.get( eid,None )
		attributeType = 0
		if e:
			if self.attributeType == "jin":
				attributeType = 0
			elif self.attributeType == "mu":
				attributeType = 1
			elif self.attributeType == "shui":
				attributeType = 2
			elif self.attributeType == "huo":
				attributeType = 3
			elif self.attributeType == "tu":
				attributeType = 4
			e.allClients.CLIENT_OnMonsterCopyEnterPicture( attributeType )
		
class AIAction224(AIActionBase.AIActionBase):
	"""
	设置AI目标头顶，脚下光圈，血条的显示颜色 0:不改变颜色，1:绿色，2:红色
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.colorstr = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.colorstr = int(section["param1"])
	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = entity.monsterAIGetTargetEntity()
		if not targetEntity:
			KBEDebug.ERROR_MSG("entity.id = %s: monsterAITarget is None!"%entity.id)
			return
		targetEntity.setAppearanceColor(self.colorstr)


class AIAction225(AIActionBase.AIActionBase):
	"""
	重置AI目标头顶，脚下光圈，血条的显示颜色
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
	
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = entity.monsterAIGetTargetEntity()
		if not targetEntity:
			KBEDebug.ERROR_MSG("entity.id = %s: monsterAITarget is None!"%entity.id)
			return
		targetEntity.resetApperanceColor(self.colorstr)	

class AIAction226(AIActionBase.AIActionBase):
	"""
	CST-8725 冰火灵脉副本 创建降服的狼王
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		spaceEntity.getScript().createCallWolfMonster( spaceEntity, entity.position, Math.Vector3(0.0, 0.0, entity.direction.z) )
		entity.delayDestroy(0.5)

class AIAction227(AIActionBase.AIActionBase):
	"""
	上古密阵有概率刷出NPC队伍
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.probability = 0
		self.scriptID = ""
		self.position = None
		self.direction = None
		self.key = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.probability = int(section["param1"])
		self.scriptID = section["param2"].split("|")
		
		if section["param3"].strip() != "":
			position = Functions.vector3TypeConvert( section["param3"] )
			if position is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param3(%s)" %( self.getAIID(), section["param3"] ) )
			else:
				self.position = KBEMath.Unreal2KBEnginePosition( position )
			
		if section["param4"].strip() != "":
			direction = Functions.vector3TypeConvert( section["param4"] )
			if direction is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param4(%s)" %( self.getAIID(), section["param4"] ) )
			else:
				self.direction = KBEMath.Unreal2KBEngineDirection( direction )
		self.key = section["param5"]	#string类型

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		if random.randint( 0, 100 ) <= self.probability:
			for i in range( len(spaceEntity.manMemberData) ):
				newEntity = entity.createEntityByScriptID(self.scriptID[i], self.position, self.direction ,{ "spawnPos":self.position,"spawnDir":self.direction})
				newEntity.robotName = spaceEntity.manMemberData[i]["name"]
				newEntity.robotLevel = spaceEntity.manMemberData[i]["level"]
				newEntity.robotCamp = spaceEntity.manMemberData[i]["camp"]
				newEntity.occupation = spaceEntity.manMemberData[i]["profession"]
				if newEntity.occupation == csdefine.CLASS_FIGHTER:
					newEntity.setModelNumber( spaceEntity.getScript().modelNumberList[0] )
				elif newEntity.occupation == csdefine.CLASS_SWORDMAN:
					newEntity.setModelNumber( spaceEntity.getScript().modelNumberList[1] )
				elif newEntity.occupation == csdefine.CLASS_ARCHER:
					newEntity.setModelNumber( spaceEntity.getScript().modelNumberList[2] )
				else:
					newEntity.setModelNumber( spaceEntity.getScript().modelNumberList[3] )
		else:
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, self.key, "")


class AIAction228(AIActionBase.AIActionBase):
	"""
	副本中找距离最近的玩家
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.speed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.speed = float(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		dists = []
		tempDists = []
		for role in spaceEntity._spaceRoles:
			dist = entity.position.flatDistTo(role.position)
			dists.append(dist)
			tempDists.append(dist)
		if len(tempDists) and len(dists):
			dists.sort()
			index = tempDists.index( dists[0] )
			entity.gotoPosition(spaceEntity._spaceRoles[index].position, 1.0, True, 0, self.speed)

class AIAction229(AIActionBase.AIActionBase):
	"""
	副本中找血量最低的玩家
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.speed = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.speed = float(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		hps = []
		tempHPs = []
		for role in spaceEntity._spaceRoles:
			hps.append( role.HP )
			tempHPs.append(role.HP)
		if len(tempHPs) and len( hps ):
			hps.sort()
			index = tempHPs.index( hps[0] )
			entity.gotoPosition(spaceEntity._spaceRoles[index].position,1.0, True, 0, self.speed )

class AIAction230(AIActionBase.AIActionBase):
	"""
	CST-8726 勇闯夺命岛 小BOSS指引寻找大Boss
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.newAIState = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.newAIState = int(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		bossScriptID = entity.queryTemp("searchBossID")
		if not bossScriptID:
			entity.monsterAIChangeSubState(self.newAIState)
			return

		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			entity.monsterAIChangeSubState(self.newAIState)
			return

		bossEntitys = spaceEntity.getEntityMailBoxRecord( bossScriptID )
		if not len( bossEntitys ):
			entity.monsterAIChangeSubState(self.newAIState)
			return
		entity.gotoPosition(bossEntitys[0].position)

class AIAction231(AIActionBase.AIActionBase):
	"""
	副本中怪物逃跑 根据怪物视野范围内玩家  在MonsterEscapePointCfg.py 取逃跑点 JIRA CST-8973
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.searchRadius = 0.0
		self.searchAngle = 0.0
		self.searchTimes = 0
		self.escapePointNums = [] #如果搜索的逃跑点中有特殊点，该值无用

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.searchRadius = float(section["param1"])
		self.searchAngle = float( section["param2"] )
		self.searchTimes = int( section["param3"] )
		self.escapePointNums = [int(i) for i in section["param4"].split("|") ] #[最小值,最大值]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		roleViews = []
		for role in spaceEntity._spaceRoles:
			if entity.monsterAICheckInViewRange( role.id ):
				roleViews.append(role)
		if not len( roleViews ):
			return

		escapePointNum = random.randint( self.escapePointNums[0], self.escapePointNums[1] )
		escapePoints = g_MonsterEscapePoint.getMonsterEscapePoints( entity, roleViews, self.searchRadius,self.searchAngle,self.searchTimes,escapePointNum )
		entity.setTemp("escapePoints",escapePoints)

class AIAction232(AIActionBase.AIActionBase):
	"""
	副本中怪物逃跑  逃跑到下一个点  在MonsterEscapePointCfg.py 取逃跑点 JIRA CST-8973
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		escapePoints = entity.queryTemp( "escapePoints" )
		if not escapePoints:
			return

		entity.gotoPosition( escapePoints[0],0.0,True,0, entity.getSpeed() )


class AIAction233(AIActionBase.AIActionBase):
	"""
	设置是否开启跳跃
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.canJumpMove = False

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.canJumpMove = bool( section["param1"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.canJumpMove = self.canJumpMove

class AIAction234(AIActionBase.AIActionBase):
	"""
	根据触发者职业(战士、剑客、链刃、法师)添加buff
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = {}

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			buffList = [int(buffID) for buffID in section["param1"].strip().split("|")]
			if len(buffList) >= 4:
				professions = [csdefine.CLASS_FIGHTER, csdefine.CLASS_SWORDMAN, csdefine.CLASS_ARCHER, csdefine.CLASS_MAGE]
				self.buffIDs = dict(zip(professions, buffList ))

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.buffIDs:
			triggerEntity.addBuff( entity, self.buffIDs[triggerEntity.profession] )
		
class AIAction235(AIActionBase.AIActionBase):
	"""
	移除触发者buff
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buffIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.buffIDs = [int(buffID) for buffID in section["param1"].strip().split("|")]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		for id in self.buffIDs:
			triggerEntity.removeBuffByID( id )

class AIAction236(AIActionBase.AIActionBase):
	"""
	选择优先级的高的entity作为攻击目标 (伤害高的玩家->玩家->伤害高的怪物 隐身单位除外)
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		damageDataIDs = sorted(entity.damageList,key=lambda x:entity.damageList[x], reverse = True)
		for id in damageDataIDs:
			damageEntity = KBEngine.entities.get(id,None)
			if not damageEntity:
				continue
			if damageEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and not damageEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
				if id == entity.getTargetID():
					return
				if entity.monsterAIIsCanAttackUseID(id):
					entity.setTargetID(id)
					return

		for id in entity.enemyList.keys():
			enemyEntity = KBEngine.entities.get( id,None )
			if not enemyEntity:
				continue
			if enemyEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				if id == entity.getTargetID():
					return
				if entity.monsterAIIsCanAttackUseID(id):
					entity.setTargetID(id)
					return
		for id in damageDataIDs:
			damageEntity = KBEngine.entities.get(id,None)
			if damageEntity and damageEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
				continue
			if id == entity.getTargetID():
				return
		
			if entity.monsterAIIsCanAttackUseID(id):
				entity.setTargetID(id)
				return

class AIAction237(AIActionBase.AIActionBase):
	"""
	焚火金牛副本中所有玩家播放系统提示
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._noticeID = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._noticeID = int(section["param1"])

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			role.statusMessage( self._noticeID, "" )

class AIAction238(AIActionBase.AIActionBase):
	"""
	焚火金牛怪 继续前进
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.moveStart( csdefine.MOVE_TYPE_MOVE_POINT, entity.getSpeed(), True, ( entity.destPosition, 0.0, True, 0 ) )

class AIAction239(AIActionBase.AIActionBase):
	"""
	焚火金牛怪 回到中心位置
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if entity.getPatrolSpeed(entity.getSpeed()) < entity.getMaxSpeed():
			entity.accelerateSpeed( entity.getAccSpeed() )
		entity.moveStart( csdefine.MOVE_TYPE_MOVE_POINT, entity.getPatrolSpeed(entity.getSpeed()), True, ( entity.getCenterPos(), 0.0, True, 0 ) )

class AIAction240( AIActionBase.AIActionBase ):
	"""
	跟随归属玩家到一定范围内
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0.0
		self.moveDist = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.radius = float( section["param1"] )
		self.moveDist = float( section["param2"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not hasattr( entity, 'owner' ):
			return
		if not entity.owner:
			return
		master = KBEngine.entities.get( entity.owner.id, None )
		if not master:
			return
		randomPos = Math.Vector3( master.position )
		posList = master.getRandomPoints( master.position, self.radius, 1, master.layer,0xFFFF )
		if len( posList ):
			randomPos = posList[0]
		behType = csdefine.BEHAVIOUR_TYPE_MOVING
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
		moveArgs = [ randomPos, self.moveDist ]
		entity.behAdd( behType, [ moveScriptID, entity.getSpeed(), True, moveArgs ] )


class AIAction241(AIActionBase.AIActionBase):
	"""
	CST-9348 焚火金牛 显示金牛额外血条和血条信息
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.describe = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.describe = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.ShowFHJNSpecialWidget( entity.HP_Max, entity.HP, self.describe )

class AIAction242(AIActionBase.AIActionBase):
	"""
	CST-9348 焚火金牛 移除金牛额外血条和血条信息
	"""
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.HideFHJNSpecialWidget()

class AIAction243(AIActionBase.AIActionBase):
	"""
	CST-9348 焚火金牛 更新金牛额外血条
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.notifyID = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.notifyID = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		if entity.HP == 0:
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, self.notifyID, "")
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.UpdateFHJNSpecialWidget( entity.HP_Max, entity.HP )

class AIAction244(AIActionBase.AIActionBase):
	"""
	怪物找并移动SpellBoxPickItem
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.range = 0.0
		self.scriptIDs = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.range = float( section["param1"] )
		if section["param2"]:
			self.scriptIDs = section["param2"].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entities = entity.entitiesInRangeExtForAI( self.range, csconst.AI_ENTITIES_IN_RANGE_HEIGHT, "SpellBoxPickItem", self.scriptIDs )
		if len(entities):
			et = sorted( entities, key = lambda e:e.position.flatDistTo( entity.position ))
			entity.setTemp("OpenSpellBoxID",et[0].id)
			entity.gotoPosition( et[0].position )
		else:
			entity.removeTemp("OpenSpellBoxID")

class AIAction245(AIActionBase.AIActionBase):
	"""
	副本勇闯绝命岛  取要寻找的Boss
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptIDS = []
		self.notifyID = ""
		self.range = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.scriptIDS = section["param1"].split("|") #Boss的scriptID
		self.notifyID = section["param2"] # 该通知ID 用来通知已经找到的Boss 去找另一个Boss
		if section["param3"]:
			self.range = float( section["param3"] ) # 通知其他Boss的范围

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		bossScriptID = entity.queryTemp("FindBossScriptID")
		if bossScriptID:
			return

		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		recordScriptIDs = spaceEntity.getRecordFindBossScriptIDs()
		findScriptIDs = []
		for scriptID in self.scriptIDS:
			if scriptID in recordScriptIDs or entity.scriptID == scriptID:
				continue
			findScriptIDs.append( scriptID )

		if not len( findScriptIDs ):
			return
		bossEntitys = []
		for scriptID in findScriptIDs:
			tempBoss = [bossEntity for bossEntity in spaceEntity.getEntityMailBoxRecord( scriptID ) if bossEntity.getState() != csdefine.ENTITY_STATE_DEAD]
			bossEntitys.extend( tempBoss )

		result = sorted( bossEntitys, key=lambda e:e.position.flatDistTo( entity.position ) )
		entity.setTemp("FindBossScriptID", result[0].scriptID )
		for scriptID in recordScriptIDs:
			if entity.scriptID == scriptID:
				continue
			entities = spaceEntity.getEntityMailBoxRecord( scriptID )
			if not len( entities ):
				continue
			if entities[0].position.flatDistTo( entity.position ) > self.range:
				continue
			entities[0].setTemp( "FindBossScriptID", result[0].scriptID )
			entity.monsterAISendCommand( entities[0].id, self.notifyID)

		spaceEntity.addRecordFindBossScriptIDs( entity.scriptID )
		spaceEntity.addRecordFindBossScriptIDs( result[0].scriptID )

class AIAction246(AIActionBase.AIActionBase):
	"""
	副本勇闯绝命岛  寻找Boss
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.newAIState = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.newAIState = int( section["param1"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		scriptID = entity.queryTemp("FindBossScriptID")
		if not scriptID:
			entity.monsterAIChangeSubState(self.newAIState)
			return
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			entity.monsterAIChangeSubState(self.newAIState)
			return
		findEntitys = spaceEntity.getEntityMailBoxRecord( scriptID )
		if not len( findEntitys ):
			entity.monsterAIChangeSubState(self.newAIState)
			return
		entity.gotoPosition( findEntitys[0].position,0.0,True,0,entity.getSpeed() )

class AIAction247(AIActionBase.AIActionBase):
	"""
	记录怪的当前血量值
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.recordKey = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.recordKey = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.setTemp( self.recordKey,entity.HP)

class AIAction248(AIActionBase.AIActionBase):
	"""
	CST-9506 程序功能需求（22级）——副本勇闯绝命岛BOSS快速折线逃跑表现功能需求
	背离攻击目标方向 夹角为angle 随机一个方向远离 radius米 移动时常为movetime 动作为actionID
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.movetime = 0.5 #移动时间
		self.radius = 15 	#移动最大距离
		self.angle = 90    #角度范围
		self.actionID = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.moveTime = float(section["param1"])
		self.radius = float(section["param2"])
		self.angle = float(section["param3"])
		self.actionID = section["param4"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetID = entity.getTargetID()
		target = KBEngine.entities.get(targetID, None)
		if target:
			yawBase = csarithmetic.getYawByVector3(entity.position - target.position)
			entity.move_CST_9506(yawBase, self.angle, self.moveTime, self.radius, self.actionID)

class AIAction249(AIActionBase.AIActionBase):
	"""
	怪物开启SpellBoxPickItem
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.timeTag = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.timeTag = section["param1"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if self.timeTag in entity.monsterAITimeTag:
			del entity.monsterAITimeTag[self.timeTag]
		entity.monsterAITimeTag[self.timeTag] = 0.0
		entity.monsterAITimeTag[self.timeTag] = time.time()
		spellBoxID = entity.queryTemp("OpenSpellBoxID")
		if spellBoxID == None:
			return
		spellBoxEntity = KBEngine.entities.get( spellBoxID )
		if not spellBoxEntity:
			return
		skillID = spellBoxEntity.getScript().getGossipSkillID()
		entity.useSkillToEntity( skillID, spellBoxEntity.id )
		entity.removeTemp("OpenSpellBoxID")
		#entity.addTimerCallBack(2.0,"removeTemp", ("OpenSpellBoxID",))

class AIAction250(AIActionBase.AIActionBase):
	"""
	CST-6351 怪物开始扔火把
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.effectID = None
		self.radius = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.effectID = section["param1"]
		self.radius = int(section["param2"])
	def do(self, ai, entity, triggerEntity):
		entity.allClients.startThorwtorch( self.effectID, self.radius)

class AIAction251(AIActionBase.AIActionBase):
	"""
	移动到一定范围内能通过导航移动到一定距离的最近的entity位置
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.radius = 0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.entityType = ""
		self.scriptIDs = []
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]
		self.distance = 1.0
	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		param1 = section["param1"].split("|")
		self.radius = float(param1[0])
		if len(param1)>1:
			self.height = float(param1[1])
		self.entityType = section[ "param2" ]
		if section["param3"].strip()!="":
			self.scriptIDs = section["param3"].strip().split("|")
		if section["param4"].strip()!="":
			self.removeStates = [int(state) for state in section["param4"].strip().split("|")]
		if section[ "param5" ]:
			self.distance = float( section[ "param5" ])


	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		eidPos = []
		sortPos = []
		entities = entity.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs,self.removeStates  )
		for e in entities:													# 选择最近目标的ID
			if e.hasEffectState( csdefine.EFFECT_STATE_HIDE ):continue		# 隐身单位不能选择
			dis = entity.position.flatDistTo(e.position)
			eidPos.append( {e.id:dis} )

		sortPos = sorted(eidPos,key = lambda d:list(d.values())[0])
		for d in sortPos:
			id = list(d.keys())[0]
			e = KBEngine.entities.get( id,None )
			if e and e.getState() != csdefine.ENTITY_STATE_DEAD:
				pos = KBEngine.raycast( entity.spaceID, entity.layer, entity.position, e.position )[0]
				if e.position.flatDistTo( pos ) < self.distance:
					entity.gotoPosition( pos )
					return
class AIAction252(AIActionBase.AIActionBase):
	"""
	操作火炮（AI目标）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def do(self, ai, entity, triggerEntity):
		target = entity.monsterAIGetTargetEntity()
		if target:
			target.beginOperationBattery( entity.id )
			
class AIAction253(AIActionBase.AIActionBase):
	"""
	取消火炮操作
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def do(self, ai, entity, triggerEntity):
		target = entity.monsterAIGetTargetEntity()
		if target:
			target.cancelOperationBattery( entity.id )

class AIAction254(AIActionBase.AIActionBase):
	"""
	火炮执行开炮行为
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.skillID = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.skillID = [int(i) for i in section["param1"].split("|")]

	def do(self, ai, entity, triggerEntity):
		targetID = entity.monsterAIGetTarget()
		if targetID:
			entity.npcProjectBattery( random.choice(self.skillID), targetID )
		else:
			KBEDebug.ERROR_MSG(" entity(id:%d) Cannot find monsterAIGetTarget, in AIAction254!"%entity.id)

class AIAction255(AIActionBase.AIActionBase):
	"""
	AI目标(必须是玩家)放弃某任务
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.questID = int(section["param1"])

	def do(self, ai, entity, triggerEntity):
		target = entity.monsterAIGetTargetEntity()
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			target.abandonQuest( self.questID)

class AIAction256(AIActionBase.AIActionBase):
	"""
	原兽进入虚弱状态
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._destroyTime = int(section["param1"]) #销毁时间

	def do(self, ai, entity, triggerEntity):
		entity.weakState = 1
		entity.destroyTimeID = entity.addTimerCallBack( self._destroyTime, "destroySelf", () )

class AIAction257(AIActionBase.AIActionBase):
	"""
	怪物死亡在怪物的位置上根据权重随机概率刷新出原兽
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._scriptIDList = []
		self._probabilityList = []
		self._indexList = []
		self._destroyTime = 0
		self.effectID = None
		self.bossList = []

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._scriptIDList = section["param1"].split("|") #凡兽的scriptID|灵兽的scriptID|圣兽的scriptID
		self._probabilityList = [float(i) for i in section["param2"].split("|")] #凡兽的刷新概率|灵兽的刷新概率|圣兽的刷新概率
		num = 0.0
		for j in self._probabilityList:
			num += j
		if num < 100:
			self._probabilityList.append( 100- num ) 
		for i in range( len( self._probabilityList ) ):
			self._indexList.append(i)
		if section["param3"]:
			self._destroyTime = int(section["param3"]) #销毁时间
		self.effectID = section["param4"]
		
		if section["param5"]:
			lst = section["param5"].split("|")#BOSS的scriptID:高出玩家的等级|BOSS的scriptID:高出玩家的等级|BOSS的scriptID:高出玩家的等级……
			for l in lst:
				ll = l.split(":")
				self.bossList.append((int(ll[0]), int(ll[1])))
			
	def do(self, ai, entity, triggerEntity):
		def getForWeight( indexList, probabilityList ):
			"""计算随机概率"""
			number = 0
			x = random.uniform( 0, 10000 )
			for index, probability in enumerate( probabilityList ):
				if number < x <= probability + number:
					return index
				else:
					number = probability
			return -1
		index = getForWeight( self._indexList, self._probabilityList )
		for index1, scriptID in enumerate( self._scriptIDList ):
			if index == index1:
				newEntity = entity.createEntityByScriptID( scriptID, entity.position, entity.direction, { "spawnPos": entity.position } )
				newEntity.ownerIDList = entity.getOwnerIDList()
				newEntity.allClients.CLIENT_OnPlayParticles( newEntity.id, self.effectID, "", 1.0, Math.Vector3(0,0,0) )
				newEntity.destroyTimeID = newEntity.addTimerCallBack( self._destroyTime, "destroySelf", () )
				
				if triggerEntity:
					#配置在最后的才是圣兽
					if index == len(self._scriptIDList) - 1:
						spaceEntity = entity.getCurrentSpace()
						if spaceEntity:	#广播一条消息
							spaceEntity.globalWord(csstatus.ITEM_ADD_BY_LUNHUIMIJING, "{}|{}".format(triggerEntity.getName(), newEntity.getName()))
							#if triggerEntity.getClient():
							#	triggerEntity.client.CLIENT_PlaySound(Const.SHENGJIE_ITEM_GET_SOUND)
							#	triggerEntity.client.CLIENT_PlayEffect(Const.SHENGJIE_ITEM_GET_EFFECTID)
								
					if index < len(self.bossList):
						bossID, level = self.bossList[index]
						if bossID == "0": continue
						entityLevel = level + triggerEntity.level
						newEntity =  entity.createEntityByScriptID( bossID, entity.position, entity.direction, { "level" : entityLevel} )
						newEntity.setBootyOwnerForNeverChange(triggerEntity) #设置怪物所有权
				

class AIAction258(AIActionBase.AIActionBase):
	"""
	云梯(MonsterExtAerialLadder)跟随玩家
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.distance = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.distance = float( section["param1"] )

	def do(self, ai, entity, triggerEntity):
		followerID = entity.getFollowerID()
		followerEntity = KBEngine.entities.get( followerID,None )
		if not followerEntity:
			entity.destroySelf()
			return

		entity.gotoPosition(followerEntity.position,self.distance)

class AIAction259(AIActionBase.AIActionBase):
	"""
	改变云梯(MonsterExtAerialLadder) （0:跟随 1:搭建 2:搭建完成）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.ladderState = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.ladderState = int( section["param1"] )

	def do(self, ai, entity, triggerEntity):
		entity.changeAerialLadderState( self.ladderState )


# class AIAction260(AIActionBase.AIActionBase):
# 	"""
# 	cst-10221
# 	阵型跟随移动
# 	"""
# 	def __init__( self, aiID ):
# 		AIActionBase.AIActionBase.__init__( self, aiID )

# 	def initData(self, section):
# 		AIActionBase.AIActionBase.initData(self, section)
# 		self.startDist = float(section["param1"])
# 		self.spacing = float(section["param2"])
# 		self.columnMax = int(section["param3"])
# 		self.isCmdMove = bool(section["param4"])
		
# 	def do(self, ai, entity, triggerEntity):
# 		entity.moveToFollowTargetPos(self.startDist, self.spacing, self.columnMax, self.isCmdMove)


# class AIAction261(AIActionBase.AIActionBase):
# 	"""
# 	cst-10221
# 	阵型矩形列阵移动
# 	"""
# 	def __init__( self, aiID ):
# 		AIActionBase.AIActionBase.__init__( self, aiID )

# 	def initData(self, section):
# 		AIActionBase.AIActionBase.initData(self, section)
# 		self.startDist = float(section["param1"])
# 		self.spacing = float(section["param2"])
# 		self.columnMax = int(section["param3"])
# 		self.isCmdMove = bool(section["param4"])

# 	def do(self, ai, entity, triggerEntity):
# 		entity.moveToRectFormationTargetPos(self.startDist, self.spacing, self.columnMax, self.isCmdMove)	


# class AIAction262(AIActionBase.AIActionBase):
# 	"""
# 	cst-10221
# 	阵型圆形列阵移动
# 	"""
# 	def __init__( self, aiID ):
# 		AIActionBase.AIActionBase.__init__( self, aiID )

# 	def initData(self, section):
# 		AIActionBase.AIActionBase.initData(self, section)
# 		self.startDist = float(section["param1"])
# 		self.spacing = float(section["param2"])
# 		self.columnMax = int(section["param3"])
# 		self.isCmdMove = bool(section["param4"])

# 	def do(self, ai, entity, triggerEntity):
# 		entity.moveToCircleFormationTargetPos(self.startDist, self.spacing, self.columnMax, self.isCmdMove)	


class AIAction263(AIActionBase.AIActionBase):
	"""
	cst-10221
	指挥士兵：跟随
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.startDist = float(section["param1"])
		self.spacing = float(section["param2"])
		self.columnMax = int(section["param3"])
		self.moveSpeed = float(section["param4"])
		
	def do(self, ai, entity, triggerEntity):
		entity.sendCmdFollow(self.startDist, self.spacing, self.columnMax, self.moveSpeed)	

class AIAction264(AIActionBase.AIActionBase):
	"""
	cst-10221
	指挥士兵列阵：矩形
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.startDist = float(section["param1"])
		self.spacing = float(section["param2"])
		self.columnMax = int(section["param3"])
		self.moveSpeed = float(section["param4"])

	def do(self, ai, entity, triggerEntity):
		entity.sendCmdRectFormation(self.startDist, self.spacing, self.columnMax, self.moveSpeed)	


class AIAction265(AIActionBase.AIActionBase):
	"""
	cst-10221
	指挥士兵列阵：圆形
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.startDist = float(section["param1"])
		self.spacing = float(section["param2"])
		self.columnMax = int(section["param3"])
		self.moveSpeed = float(section["param4"])

	def do(self, ai, entity, triggerEntity):
		entity.sendCmdCircleFormation(self.startDist, self.spacing, self.columnMax, self.moveSpeed)	

class AIAction266(AIActionBase.AIActionBase):
	"""
	捕捉原兽
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.distance = 0.0
		self.effectID = None
		self.slotName = ""
		self.scale = -1.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.distance = float( section["param1"])
		self.effectID = section["param2"].strip()
		if len(section["param3"].strip()):
			self.slotName = section["param3"].strip()
		if len(section["param4"].strip()):
			self.scale = float( section["param4"].strip() )
			
	def do(self, ai, entity, triggerEntity):
		num = random.uniform( 0, 100 )
		if num <= entity.probability:
			if self.effectID:
				entity.allClients.CLIENT_OnPlayParticles( triggerEntity.id,self.effectID,self.slotName, self.scale, Math.Vector3(0,0,0) )
			triggerEntity.addItemByID( entity.getScript().itemPetEgg )
			triggerEntity.client.OnCatchOriginPetResult(1)
			entity.destroySelf()
		else:
			triggerEntity.client.OnCatchOriginPetResult(0)
			entity.startMoveBehindPos( triggerEntity, self.distance )

class AIAction267(AIActionBase.AIActionBase):
	"""
	NPC开炮，设置AI目标
	1、攻城器械
	2、敌对玩家
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.minAttackDist = 0.0			# 最近攻击距离
		self.maxAttackDist = 0.0			# 最远攻击距离
		self.offsetRadian = 0.0				# 左右各偏移弧度

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.minAttackDist = float( section["param1"])
		self.maxAttackDist = float( section["param2"])
		self.offsetRadian = float( section["param3"])
			
	def do(self, ai, entity, triggerEntity):
		def filterFunc(x):
			
			if x.isState(csdefine.ENTITY_STATE_DEAD) or x.isState(csdefine.ENTITY_STATE_PEAD):
				return False
			if x.queryRelation(entity) != csdefine.COMBAT_RELATION_ENEMY:
				return False
			dist = entity.position.distTo(x.position)
			if dist < self.minAttackDist or dist > self.maxAttackDist:
				return False
#			yaw = entity.getYaw()
#			yaw = yaw if yaw >= 0 else yaw + math.pi
#			dstYaw = csarithmetic.getYawByVector3(x.position - entity.position)
#			dstYaw = dstYaw if dstYaw >= 0 else dstYaw + math.pi
#			if dstYaw < yaw - self.offsetRadian or dstYaw > yaw + self.offsetRadian:
#				return False
			
			
			return csarithmetic.isInSector(x.position, entity.position, entity.initialDirection.z, self.maxAttackDist, self.offsetRadian * 2)
			
		space = entity.getCurrentSpace()
		if space.__class__.__name__ == "SpaceCopyAttackCityWar":
			machineList = []
			# 首先选择被操作的攻城器械
			for entityID in space.machineWarList:
				machine = KBEngine.entities.get(entityID)
				if machine and machine.queryRelation(entity)  == csdefine.COMBAT_RELATION_ENEMY:
					machineList.append( machine )
			machineList = list(filter(filterFunc, machineList))
			if machineList:
				result = sorted( machineList, key=lambda e:e.position.flatDistTo( entity.position ) )
				entity.monsterAISetTarget(result[0].id)
				return
		roleList = []
		# 选择玩家的士兵
		soldierList = []
		for player in space._spaceRoles:
			if entity.queryRelation(player) == csdefine.COMBAT_RELATION_ENEMY:
				roleList.append( player )
				for idList in player.controlledData.values():
					for entityID in idList:
						monsterEnt = KBEngine.entities.get( entityID )
						if monsterEnt:
							soldierList.append(monsterEnt)			# 每个玩家只取一个士兵
							break
		if soldierList:
			result = sorted( soldierList, key=lambda e:e.position.flatDistTo( entity.position ) )
			entity.monsterAISetTarget(result[0].id)
			return

		
		# 选择敌对玩家
		roleList = list(filter(filterFunc, roleList))
		if roleList:
			result = sorted( roleList, key=lambda e:e.position.flatDistTo( entity.position ) )
			entity.monsterAISetTarget(result[0].id)
			return

class AIAction268(AIActionBase.AIActionBase):
	"""
	cst-10221
	指挥士兵指令：攻击
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		
	def do(self, ai, entity, triggerEntity):
		entity.sendCmdAttack()


class AIAction269(AIActionBase.AIActionBase):
	"""
	cst-10221 士兵列阵 跟随移动到上一次队伍位置
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.isCmdMove = bool(section["param1"])
		
	def do(self, ai, entity, triggerEntity):
		entity.moveFollow(self.isCmdMove)


class AIAction270(AIActionBase.AIActionBase):
	"""
	cst-10221
	士兵列阵 矩形列阵移动到队伍位置
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.isCmdMove = bool(section["param1"])
		
	def do(self, ai, entity, triggerEntity):
		entity.moveRectFormation(self.isCmdMove)


class AIAction271(AIActionBase.AIActionBase):
	"""
	cst-10221
	士兵列阵 圆形列阵移动到队伍位置
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.isCmdMove = bool(section["param1"])
		
	def do(self, ai, entity, triggerEntity):
		entity.moveCircleFormation(self.isCmdMove)

class AIAction272(AIActionBase.AIActionBase):
	"""
	搜索已搭建好的云梯
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.range = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.range = float( section["param1"] )
		
	def do(self, ai, entity, triggerEntity):
		entitys = entity.entitiesInRangeExtCircle( self.range,"MonsterExtAerialLadder")
		searchEntitys = []
		for e in entitys:
			if e.getAerialLadderState() == csdefine.AERIAL_LADDER_STATE_BUILD_SUCCESS:
				searchEntitys.append( e )
		if not len( searchEntitys ):
			return
		distList = []
		for e in searchEntitys:
			dist = e.position.distTo( entity.position )
			distList.append( dist )
		minDist = min(distList)
		index = distList.index( minDist )
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity:
			return
		position = spaceEntity.getAerialLadderUpPosInfo(searchEntitys[index].getLadderPosIndex())
		entity.setTemp("dstPosInfo",( position,searchEntitys[index].id ))

class AIAction273(AIActionBase.AIActionBase):
	"""
	移动到已搭建好的云梯
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.newAIState = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.newAIState = int( section["param1"] )
		
	def do(self, ai, entity, triggerEntity):
		dstPos,entityID = entity.queryTemp("dstPosInfo")
		if dstPos == None:
			entity.monsterAIChangeSubState(self.newAIState)
			return
		entity.gotoPosition(dstPos)

class AIAction274(AIActionBase.AIActionBase):
	"""
	推已搭建好的云梯
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.actionID = ""
		self.newAIState = 0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.actionID = section["param1"]
		self.newAIState = int( section["param2"] )
		
	def do(self, ai, entity, triggerEntity):
		dstPos,entityID = entity.queryTemp("dstPosInfo")
		aerialEntity = KBEngine.entities.get( entityID, None )
		if not aerialEntity:
			entity.monsterAIChangeSubState(self.newAIState)
			return
		entity.allClients.CLIENT_OnPlayAction( self.actionID, -1.0 )
		aerialEntity.aerialLadderReadyToFall()
		entity.monsterAIChangeSubState(self.newAIState)
		entity.removeTemp("dstPosInfo")

class AIAction275(AIActionBase.AIActionBase):
	"""
	将领召唤小兵
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptID = "" #召唤小兵ScriptID
		self.amount = 0    # 召唤小兵的数量

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.scriptID = section["param1"]
		self.amount = int( section["param2"] )
		
	def do(self, ai, entity, triggerEntity):
		entity.createSoldiers( self.scriptID, self.amount )

class AIAction276(AIActionBase.AIActionBase):
	"""
	将领销毁所有跟随它的士兵
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		entity.destorySoldiers()


class AIAction277(AIActionBase.AIActionBase):
	"""
	改变自身初始动作
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.initActionId = section["params1"]

	def do(self, ai, entity, triggerEntity):
		entity.initActionId = self.initActionId

class AIAction278(AIActionBase.AIActionBase):
	"""
	查找最近的恢复点(兵营)
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity or spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_CHILD_TYPE_GCZ:
			return
		recordNotOccupyBarracks = spaceEntity.getAllNotOccupyBarracks()
		entityIDs = []
		dists = []
		for entityID, position in recordNotOccupyBarracks.items():
			entityIDs.append(entityID)
			dists.append( position.flatDistTo( entity.position ) )
		dist = min( dists )
		index = dists.index( dist )
		entity.setTemp("barracksID",entityIDs[index])

class AIAction279(AIActionBase.AIActionBase):
	"""
	将领走到最近恢复点
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity or spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_CHILD_TYPE_GCZ:
			return
		barracksID = entity.queryTemp( "barracksID" )
		if not barracksID:
			return
		position = spaceEntity.getRecordNotOccupyBarracks( barracksID )
		if position == None:
			return
		entity.gotoPosition( position )

class AIAction280(AIActionBase.AIActionBase):
	"""
	给一定范围内的 处于非战斗状态的将领并且距离最近 发送通知
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.scriptIDs = []
		self.commandID = ""
		self.radius = 0
		self.entityType = ""
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.radius = float(section["param1"])
		if section["param2"].strip()!="":
			self.scriptIDs = section["param2"].strip().split("|")
		self.commandID = section["param3"]
		if section["param4"].strip()!="":
			self.removeStates = [int(state) for state in section["param4"].strip().split("|")]
		self.entityType = section["param5"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entities = entity.entitiesInRangeExtForAI( self.radius, csconst.AI_ENTITIES_IN_RANGE_HEIGHT, self.entityType, self.scriptIDs, self.removeStates )
		if not len( entities ):
			return
		dists = []
		for e in entities:
			dist = e.position.flatDistTo( entity.position )
			dists.append( dist )
		minDist = min(dists)
		index = dists.index( minDist )
		entities[index].monsterAISendCommand(entities[index].id, self.commandID)

class AIAction281(AIActionBase.AIActionBase):
	"""
	虚空探宝  清除时间
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity:
			if spaceEntity.probeTimerID:
				spaceEntity.popTimer( spaceEntity.probeTimerID )
				spaceEntity.probeTimerID = 0
			if spaceEntity.extcavateTimerID:
				spaceEntity.popTimer( spaceEntity.extcavateTimerID )
				spaceEntity.extcavateTimerID = 0
		entity.allClients.CancelDisplyCurrentText()

class AIAction282(AIActionBase.AIActionBase):
	"""
	搜索一定距离内，离自身最近的敌人为攻击目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self.radius = float(section["param1"])

	def do(self, ai, entity, triggerEntity):
		entityTypes = [csdefine.ENTITY_FLAG_ROLE, csdefine.ENTITY_FLAG_MONSTER, csdefine.ENTITY_FLAG_VEHICLEPET]
		entities = entity.entitiesInRangeExtForAI(self.radius)
		entities = [e for e in entities if e.getEntityFlag() in entityTypes and  e.state!=csdefine.ENTITY_STATE_DEAD and entity.queryRelation(e) == csdefine.COMBAT_RELATION_ENEMY]

		minDis = self.radius
		targetID = 0
		for e in entities:
			testDist = e.position.flatDistTo(entity.position)
			if testDist<=minDis:
				targetID = e.id
				minDis =testDist
		entity.setTargetID(targetID)
		
		# ####
		# curTargetID = entity.getTargetID()
		# if not entity.monsterAIIsCanAttackUseID( curTargetID ):
		# 	curTargetID = 0
			
		# if curTargetID:
		# 	curTargetEntity = KBEngine.entities[ curTargetID ]
		# 	disToCurTarget = entity.position.flatDistTo( curTargetEntity.position ) + 0.3
		# 	damageDatas = sorted(entity.damageList,key=lambda x:entity.damageList[x], reverse = True)
		# 	for id in damageDatas:
		# 		maxDamEntity = KBEngine.entities.get( id )
		# 		if maxDamEntity and maxDamEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
		# 			continue
		# 		if id == entity.getTargetID():
		# 			return
			
		# 		if entity.monsterAIIsCanAttackUseID(id):
		# 			if entity.position.flatDistTo( maxDamEntity.position ) < disToCurTarget:
		# 				entity.setTargetID(id)
		# 				return
		
		# entityTypes = [csdefine.ENTITY_FLAG_ROLE, csdefine.ENTITY_FLAG_MONSTER, csdefine.ENTITY_FLAG_VEHICLEPET]
		# if curTargetID == 0:
		# 	ctrlEntity =entity.getCmder()
		# 	if ctrlEntity:
		# 		if  len( ctrlEntity.tempTargetList ) == 0:
		# 			entities = entity.entitiesInRangeExtForAI( self.radius )
		# 			ctrlEntity.tempTargetList  = [e for e in entities if e.getEntityFlag() in entityTypes and e.state!=csdefine.ENTITY_STATE_DEAD and ctrlEntity.queryRelation(e) == csdefine.COMBAT_RELATION_ENEMY ]
				
		# 		while True :
		# 			if len( ctrlEntity.tempTargetList ) == 0:
		# 				break
						
		# 			e = ctrlEntity.tempTargetList.pop()
		# 			if e.state!=csdefine.ENTITY_STATE_DEAD and ctrlEntity.queryRelation( e ) ==csdefine.COMBAT_RELATION_ENEMY:
		# 				entity.setTargetID(e.id)
		# 				return

class AIAction283(AIActionBase.AIActionBase):
	"""
	沿着高度上下移动（不穿地板）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self._height = 0.0
		self.moveSpeed = 0.0
		self._fallClearance = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		self._height = float( section["param1"] )
		if section["param2"].strip():
			self.moveSpeed = float(section["param2"].strip())
		if section["param3"]:
			self._fallClearance = float( section["param3"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		pos = Math.Vector3( entity.position ) + Math.Vector3(0, self._height, 0)
		posList = KBEngine.collideVertical( entity.spaceID, entity.layer, pos, 0, int(- self._height) )
		if posList:
			pos = posList[0]
			pos = Math.Vector3(pos)
			pos.y += self._fallClearance
		entity.moveFlyToPoint(pos, self.moveSpeed)

class AIAction284(AIActionBase.AIActionBase):
	"""
	创建移动的防护罩
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.inEffectID = ""
		self.outEffectID = ""
		self.inRotatTime = 0.0
		self.outRotatTime = 0.0
		self.inERotatAngle = 0.0
		self.outRotatAngle = 0.0

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			param1 = section["param1"].split("|")
			self.inEffectID = param1[0]
			self.outEffectID = param1[1]
		if section["param2"]:
			param2 = section["param2"].split("|")
			self.inRotatTime = float(param2[0])
			self.outRotatTime = float(param2[1])
		if section["param3"]:
			param3 = section["param3"].split("|")
			self.inERotatAngle = float(param3[0])
			self.outRotatAngle = float(param3[1])

	def do(self, ai, entity, triggerEntity):
		entity.allClients.OpenMoveShield( entity.id, self.inEffectID, self.inRotatTime, self.inERotatAngle, self.outEffectID, self.outRotatTime, self.outRotatAngle )

class AIAction285(AIActionBase.AIActionBase):
	"""
	移除移动的防护罩
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		entity.allClients.CloseMoveShield( entity.id )

class AIAction286(AIActionBase.AIActionBase):
	"""
	怪物在球内随机移动
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.moveSpeed = 0.0
		self.cmd1 = ""
		self.cmd2 = ""

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"].strip():
			self.moveSpeed = float(section["param1"].strip())
		self.radius = int(section["param2"])
		param3 = section["param3"].split("|")
		self.cmd1 = param3[0]
		if len(param3) > 1:
			self.cmd2 = param3[1]
		Param4 = section["param4"].split("|")
		self.minTime = float(Param4[0])
		self.maxTime = self.minTime
		if len(Param4) > 1:
			self.maxTime = float(Param4[1])

	def do(self, ai, entity, triggerEntity):
		(moveSpeed, isUpdateSpeed) = (self.moveSpeed, False) if self.moveSpeed>0 else (entity.getSpeed(), True)
		entity.moveRandomInSphere(moveSpeed, isUpdateSpeed, entity.position, self.radius, self.cmd1, self.cmd2, self.maxTime, self.minTime)

class AIAction287(AIActionBase.AIActionBase):
	"""
	清除怪物累计血量
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.isAdd = False

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.isAdd = bool(int( section["param1"]))

	def do(self, ai, entity, triggerEntity):
		if self.isAdd:
			entity.removeTemp( "MonsterHPAddValue" )
		else:
			entity.removeTemp( "MonsterHPSubValue" )


class AIAction288(AIActionBase.AIActionBase):
	"""
	通知将领增援
	(增援数量由策划配置，判断依据，根据将领到自身的距离把将领排序，兵力满足的情况下，优先距离)
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.amount = 0 #需要通知的将领数量
		self.scriptIDs = [] #将领的scriptID
		self.soldierAmount = 0 #将领携带最少士兵数量
		self.cmd = "" #发送给将领的指令

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		if section["param1"]:
			self.amount = int(section["param1"])
		if section["param2"]:
			self.scriptIDs = section["param2"].split("|")
		if section["param3"]:
			self.soldierAmount = int(section["param3"])
		self.cmd = section["param4"]

	def do(self, ai, entity, triggerEntity):
		if not self.amount or not self.scriptIDs:
			return
		entities = []
		s = entity.getCurrentSpace()
		
		for sid in self.scriptIDs:
			ids = s.getEntityRecord(sid)
			elist = []
			if len(ids):
				for eid in ids:
					e = KBEngine.entities.get(eid, None)
					if e:
						sAmount = len(e.getAllMember())
						if sAmount>=self.soldierAmount:
							elist.append(e)
			entities.extend(elist)
		
		amount = min(self.amount, len(entities))

		minDist = 10000
		pos = entity.position
		for i in range(len(entities)):
			for j in range(i+1,len(entities)):
				if entities[j].position.flatDistTo(pos)<entities[i].position.flatDistTo(pos):
					temp = entities[i]
					entities[i] = entities[j]
					entities[j] = temp

		for i in range(amount):
			entity.monsterAISendCommand(entities[i].id, self.cmd)


class AIAction289(AIActionBase.AIActionBase):
	"""
	给自身主动反应范围内，带领远程兵并且兵数量最少，距离最近的一个将领发通知（坐标跟指令）
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.position = (0,0,0) #指定坐标 换兵点坐标
		self.cmd = "" #发送给将领的指令
		self.scriptIDs = [] #远程兵scriptID

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)
		position = Functions.vector3TypeConvert( section["param1"] )
		self.position = KBEMath.Unreal2KBEnginePosition( position )
		self.cmd = section["param2"]
		self.scriptIDs = section["param3"].split("|")

	def do(self, ai, entity, triggerEntity):
		cmderList = []
		minA = 100
		proximityID = entity.findProximityByUserArg( ECBProximityDefine.PROXIMITY_AI_INITIATIVE_1 )
		if proximityID in entity.shapeProximityEnters:
			entityIDList = entity.shapeProximityEnters[proximityID]
			for id in entityIDList:
				ety = KBEngine.entities.get(id, None)
				if not ety:
					continue
				if ety.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_COMMANDER:
					if ety.soldierScriptID in self.scriptIDs:
						amount = len(ety.getAllMember())
						if amount<minA:
							minA = amount
							cmderList =[ety]
						elif amount == minA:
							cmderList.append(ety)

			minDist = 10000
			target = None
			for ety in cmderList:
				dist = ety.position.flatDistTo(self.position)
				if dist<minDist:
					minDist = dist
					target = ety
			if target:
				entity.monsterAISendCommand(target.id, self.cmd)


class AIAction290(AIActionBase.AIActionBase):
	"""
	跟随当前攻击目标到一定范围内 
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.chaseDist = 0.0
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.chaseDist = float( section["param1"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get( entity.getTargetID() )
		if not targetEntity:
			KBEDebug.ERROR_MSG("targetEntity is not exist")
			return
	
		entity.chaseEntity(targetEntity, self.chaseDist)

class AIAction291(AIActionBase.AIActionBase):
	"""
	以某个坐标为中心(如果没有指定则表示以自身为中心）在一定范围内随机位置，从几种怪物中随机召唤一种或者几种怪物
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.isJudge = []
		self.centerPos = None	#param1 中心点坐标	
		self.radius = 0.0 		#param2	指定半径
		self.isAtTheCircle = False #param3 是否在圆上
		self.isHasFlag = False  #param3是否是浮空召唤
		self.numberList = [] 		#param4	entity的数量
		self.scriptIDList = []		#param5	entity的scriptID

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )	
		if not section["param1"].strip():
			self.centerPos = None
		else:
			position = Functions.vector3TypeConvert( section["param1"] )
			if position is None:
				KBEDebug.ERROR_MSG("Vector3 Type Error: AIID(%s) param1(%s)" %( self.getAIID(), section["param1"] ) )
			else:
				self.centerPos = KBEMath.Unreal2KBEnginePosition( position )
		
		self.radius = float(section[ "param2" ])

		if len(section["param3"]):
			self.isJudge = [int(x) for x in section["param3"].split("|")]
			self.isAtTheCircle = bool(int(self.isJudge[0]))
			if len(self.isJudge) > 1:
				self.isHasFlag = bool(int(self.isJudge[1]))

		self.numberList = [int(x) for x in section["param4"].split("|")]

		self.scriptIDList = section[ "param5" ].split("|")

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity	
		"""

		def getRandPosInCircle( centerPos, radius, num, entity ):
			"""
			在圆内获得随机点坐标
			"""
			posList = []
			while num:
				x = centerPos[2]+random.uniform(-1,1)*radius
				y = centerPos[0]+random.uniform(-1,1)*radius
				posList.append(Math.Vector3( y, entity.position[1], x ))
				num-=1
			return posList

		def getRandPosAtTheCircle( centerPos, radius, num, entity ):
			"""
			在圆边缘上获得随机点坐标
			"""
			PIE = 3.1415926
			radian = PIE*2/num
			posList = []
			while num:
				x = centerPos[2]+radius*math.cos(radian*num)
				y = centerPos[0]+radius*math.sin(radian*num)
				posList.append(Math.Vector3( y, entity.position[1], x ))
				num-=1
			return posList

		posList = []
		if not self.centerPos:
			centerPos = Math.Vector3( entity.position )
		else:
			centerPos = Math.Vector3( self.centerPos )
		targetDirection = Math.Vector3( entity.direction )
		if len( self.numberList ) == 1:
			if self.isAtTheCircle:
				posList = getRandPosAtTheCircle( centerPos, self.radius, self.numberList[0], entity )
			else:
				posList = getRandPosInCircle( centerPos, self.radius, self.numberList[0], entity )
			
			for targetPosition in posList:
				tarPosition = KBEngine.collideVertical( entity.spaceID, entity.layer, targetPosition, 10, - 10 )
				scriptID = random.sample( self.scriptIDList, 1 )
				if self.isHasFlag:
					newEntity = entity.createEntityByScriptID(scriptID[0], Math.Vector3(targetPosition), targetDirection,{ "spawnPos":Math.Vector3( targetPosition ) ,"spawnDir":Math.Vector3( targetDirection )})
				elif tarPosition:
					newEntity = entity.createEntityByScriptID(scriptID[0], Math.Vector3(tarPosition[0]), targetDirection,{ "spawnPos":Math.Vector3( tarPosition[0] ) ,"spawnDir":Math.Vector3( targetDirection )})
		else:
			for index, number in enumerate(self.numberList):
				if self.isAtTheCircle:
					posList = getRandPosAtTheCircle( centerPos, self.radius, number, entity )
				else:
					posList = getRandPosInCircle( centerPos, self.radius, number, entity )
				for targetPosition in posList:
					tarPosition = KBEngine.collideVertical( entity.spaceID, entity.layer, targetPosition, 10, - 10 )
					if self.isHasFlag:
						newEntity = entity.createEntityByScriptID(self.scriptIDList[index], Math.Vector3(targetPosition), targetDirection,{ "spawnPos":Math.Vector3( targetPosition ) ,"spawnDir":Math.Vector3( targetDirection )})
					elif tarPosition:
						newEntity = entity.createEntityByScriptID(self.scriptIDList[index], Math.Vector3(tarPosition[0]), targetDirection,{ "spawnPos":Math.Vector3( tarPosition[0] ) ,"spawnDir":Math.Vector3( targetDirection )})


class AIAction292(AIActionBase.AIActionBase):
	"""
	攻城战 远离当前攻击目标 
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.distance = 0.0
	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.distance = float( section["param1"] )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		targetEntity = KBEngine.entities.get(entity.targetID, None)
		if not targetEntity:
			return
		entity.chaseEntity( targetEntity, self.distance )

class AIAction293(AIActionBase.AIActionBase):
	"""
	浮空怪物死亡后落地
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		pos = Math.Vector3(entity.position)
		layers = entity.getCurrentSpace().getScript().getNavmeshLayers()
		for i in range(layers):
			posList = KBEngine.collideVertical( entity.spaceID, i, entity.position, 0, -50)
			if posList:
				pos = Math.Vector3(posList[0])
				pos.y += 1.0
				break
		entity.addTimerCallBack( 0.5 , "moveToPointExt", ( pos, 5.0, 0.1 ))


class AIAction294(AIActionBase.AIActionBase):
	"""
	练兵场任务将领接敌
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		space = entity.getCurrentSpace()
		if space:
			space.moveMonster()

class AIAction295(AIActionBase.AIActionBase):
	"""
	轮回秘境机缘玩法 怪物被击杀触发机缘
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		#概率
		self.odds = float(section["param1"])
		#传送门ScriptID
		self.scriptID = section["param2"]

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if not triggerEntity or triggerEntity.getEntityFlag()!=csdefine.ENTITY_FLAG_ROLE:
			return
		odds = random.uniform(0, 1)
		#KBEDebug.ERROR_MSG("self.odds=%s,  odds = %s  "%(self.odds, odds	))
		if odds>self.odds:
			return
		entity.createEntityByScriptID(self.scriptID, entity.position, entity.direction, {"lifetime":600, "creatorDBID":triggerEntity.playerDBID})
		triggerEntity.statusMessage(csstatus.LHMJ_JYWF_NOTICE_SELF)
		#curSpace = entity.getCurrentSpace()
		#for role in curSpace._spaceRoles:
		#	role.statusMessage(csstatus.LHMJ_JYWF_NOTICE_ALL, role.playerName, curSpace.getScript().getSpaceName(), self.spaceName)


class AIAction296(AIActionBase.AIActionBase):
	"""
	轮回秘境建筑被打坏，掉落物品并记录
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.buildType = 0
		self.dropMap = {}

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.buildType = int(section["param1"])			# 1:灵泉，2:工坊，3:乾坤鼎，4:兽栏，5:灵田
		for splitStr in section["param2"].split("|"):
			dropStr = splitStr.split(",")
			if len(dropStr) >= 2:
				self.dropMap[int(dropStr[0])] = dropStr[1]
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		space = entity.getCurrentSpace()
		if space.getScript().getSpaceType() == csdefine.SPACE_TYPE_DONG_FU:
			dropInst = DropMgr.g_dropMgr.getDrop(entity.scriptID)
			if dropInst is None:
				return
			level = space.buildLevel.get( self.buildType, 1 )
			if not level in self.dropMap:
				return
			dropInst._dropDatas["drops"] = self.dropMap[level]
			
			ownerMap = entity.calculateBootyOwner()
			for id, dbid in ownerMap.items():
				owner = KBEngine.entities.get( id )
				if owner:
					dropInst.doDrop( entity, owner, {} )
					break
			itemDict = dropInst.getDropItemDict()
			itemStr = ""
			for itemID, amount in itemDict.items():
				if itemStr:
					itemStr += "|"
				itemStr = str( itemID ) + ":" + str( amount )
			space.onDFBuildDestroy( self.buildType )
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].onDFBuildDestroy( space.belongDBID, self.buildType, itemStr )
			
class AIAction297(AIActionBase.AIActionBase):
	"""
	把怪物 注册到 space上
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.type = int(section["param1"])			# 副本里面自己定义类型
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		space = entity.getCurrentSpace()
		try:
			space.registSpecialMonsterToSpace( self.type, entity.id, entity.scriptID )
		except:None
			
class AIAction298(AIActionBase.AIActionBase):
	"""
	把怪物 取消注册到 space
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.type = int(section["param1"])			# 副本里面自己定义类型
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		space = entity.getCurrentSpace()
		try:
			space.unRegistSpecialMonsterToSpace( self.type, entity.id, entity.scriptID )
		except:None
		
class AIAction299(AIActionBase.AIActionBase):
	"""
	守卫升级提示
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.msgID = int( section["param1"] )			# 提示的messageID
		self.lingneng = int(section["param2"])			# 消耗灵能
		self.monsterType = int(section["param3"])	# 0:默认型，1：攻击型，2：控制型
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if triggerEntity and triggerEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE):
			triggerEntity.client.ShowUpgradeGuardMsg( self.msgID, self.lingneng, entity.id, self.monsterType )
			
class AIAction300(AIActionBase.AIActionBase):
	"""
	兽栏被击毁，有概率掉幻兽
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.dropPro = {}				# 幻兽品质对应掉落概率
		dropStrList = section["param1"].split("|")
		for dropStr in dropStrList:
			drops = dropStr.split(":")
			if len(drops) >= 2:
				self.dropPro[int(drops[0])] = int( drops[1] )
				
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		ownerMap = entity.calculateBootyOwner()
		for id, dbid in ownerMap.items():
			owner = KBEngine.entities.get( id )
			if owner and owner.isEntityFlag( csdefine.ENTITY_FLAG_ROLE):
				space = owner.getCurrentSpace()
				if space.getScript().getSpaceType() == csdefine.SPACE_TYPE_DONG_FU:
					space.onPetCorralDestroy( owner, entity.id, self.dropPro )

class AIAction301(AIActionBase.AIActionBase):
	"""
	将攻（守）方玩家，加入AI目标
	0:攻方，1：守方
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		self.belongSide = int( section["param1"] )
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity:
			for player in spaceEntity._spaceRoles:
				if player.isBelongSide( self.belongSide ):
					entity.monsterAISetTarget( player.id )
					break
					
class AIAction302(AIActionBase.AIActionBase):
	"""
	攻击目标，如果离目标超过一定距离则进行追击
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		self.priorityLevel = csdefine.BEHAVIOUR_COMMON
		self.distance = 3.0

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )
		if section["param1"]:
			self.distance = float(section["param1"]) if float(section["param1"]) > 3.0 else 3.0
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		target = KBEngine.entities.get(entity.getTargetID())
		if target is None:
			return
		
		if entity.position.flatDistTo(target.position) >= self.distance:
			entity.chaseEntity(target, 2.0)
			return
		
		skillIDs = list( entity.attrSkills )
		for skillID in skillIDs:
			result = entity.monsterAIIsCanUseSkillToTarget( skillID ) and entity.behaviours[2].isCanAddBehavior( entity,[ skillID, entity.id,False], self.priorityLevel )
			if not result:
				skillIDs.remove( skillID )
		
		if not len(skillIDs):
			return
		
		skillID = random.choice( skillIDs )
		entity.turnToPos(target.position)
		entity.behAdd(csdefine.BEHAVIOUR_TYPE_SPELL, [ skillID, entity.getTargetID(),False])

class AIAction303(AIActionBase.AIActionBase):
	"""
	结束面向玩家行为
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData( self, section ):
		AIActionBase.AIActionBase.initData( self, section )


	def do(self, ai, entity, triggerEntity):
		entity.onFaceToPlayer(False)
		
class AIAction304(AIActionBase.AIActionBase):
	"""
	MonsterExtFenShen选择主人敌人列表中距离主人最近的一个作为攻击目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )
		

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	
	def do(self, ai, entity, triggerEntity):
		if not hasattr( entity, 'ownerID' ):
			return

		master = KBEngine.entities.get( entity.ownerID, None )
		if not master:
			return
		
		enemyListCopy = dict(master.enemyList)
		enemyIDList = [e for e in enemyListCopy.keys() if entity.monsterAICheckInViewRange(e)]
		if not len(enemyIDList):
			return
			
		minDis = 100000.0
		targetID = 0
		for eID in enemyIDList:
			e = KBEngine.entities.get(eID,None)
			if not e:
				continue
			distance = e.position.flatDistTo( master.position )
			if distance<=minDis:
				if e.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
					continue
				minDis = distance
				targetID = eID
		
		entity.behControlReset(csdefine.BEHAVIOUR_TYPE_SPELL)
		entity.setTargetID(targetID)

class AIAction305(AIActionBase.AIActionBase):
	"""
	把仇恨最高的entity设置成攻击目标
	"""
	def __init__( self, aiID ):
		AIActionBase.AIActionBase.__init__( self, aiID )

	def initData(self, section):
		AIActionBase.AIActionBase.initData(self, section)

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		hatredDatas = sorted(entity.hatredList,key=lambda x:entity.hatredList[x], reverse = True)
		for id in hatredDatas:
			maxDamEntity = KBEngine.entities.get( id )
			if maxDamEntity and maxDamEntity.hasEffectState( csdefine.EFFECT_STATE_HIDE ):
				continue
			if id == entity.getTargetID():
				return
		
			if entity.monsterAIIsCanAttackUseID(id):
				entity.setTargetID(id)
				return


AIActionBase.AIActionBase.setActionClass("AIAction1", AIAction1)
AIActionBase.AIActionBase.setActionClass("AIAction2", AIAction2)
AIActionBase.AIActionBase.setActionClass("AIAction3", AIAction3)
AIActionBase.AIActionBase.setActionClass("AIAction4", AIAction4)
AIActionBase.AIActionBase.setActionClass("AIAction5", AIAction5)
AIActionBase.AIActionBase.setActionClass("AIAction6", AIAction6)
AIActionBase.AIActionBase.setActionClass("AIAction7", AIAction7)
AIActionBase.AIActionBase.setActionClass("AIAction8", AIAction8)
AIActionBase.AIActionBase.setActionClass("AIAction9", AIAction9)
AIActionBase.AIActionBase.setActionClass("AIAction10", AIAction10)
AIActionBase.AIActionBase.setActionClass("AIAction11", AIAction11)
AIActionBase.AIActionBase.setActionClass("AIAction12", AIAction12)
AIActionBase.AIActionBase.setActionClass("AIAction13", AIAction13)
AIActionBase.AIActionBase.setActionClass("AIAction14", AIAction14)
AIActionBase.AIActionBase.setActionClass("AIAction15", AIAction15)
AIActionBase.AIActionBase.setActionClass("AIAction16", AIAction16)
AIActionBase.AIActionBase.setActionClass("AIAction17", AIAction17)
AIActionBase.AIActionBase.setActionClass("AIAction18", AIAction18)
AIActionBase.AIActionBase.setActionClass("AIAction19", AIAction19)
AIActionBase.AIActionBase.setActionClass("AIAction20", AIAction20)
AIActionBase.AIActionBase.setActionClass("AIAction21", AIAction21)
AIActionBase.AIActionBase.setActionClass("AIAction22", AIAction22)
AIActionBase.AIActionBase.setActionClass("AIAction23", AIAction23)
AIActionBase.AIActionBase.setActionClass("AIAction24", AIAction24)
AIActionBase.AIActionBase.setActionClass("AIAction25", AIAction25)
AIActionBase.AIActionBase.setActionClass("AIAction26", AIAction26)
AIActionBase.AIActionBase.setActionClass("AIAction27", AIAction27)
AIActionBase.AIActionBase.setActionClass("AIAction28", AIAction28)
AIActionBase.AIActionBase.setActionClass("AIAction29", AIAction29)
AIActionBase.AIActionBase.setActionClass("AIAction30", AIAction30)
AIActionBase.AIActionBase.setActionClass("AIAction31", AIAction31)
AIActionBase.AIActionBase.setActionClass("AIAction32", AIAction32)
AIActionBase.AIActionBase.setActionClass("AIAction33", AIAction33)
AIActionBase.AIActionBase.setActionClass("AIAction34", AIAction34)
AIActionBase.AIActionBase.setActionClass("AIAction35", AIAction35)
AIActionBase.AIActionBase.setActionClass("AIAction36", AIAction36)
AIActionBase.AIActionBase.setActionClass("AIAction37", AIAction37)
AIActionBase.AIActionBase.setActionClass("AIAction38", AIAction38)
AIActionBase.AIActionBase.setActionClass("AIAction39", AIAction39)
AIActionBase.AIActionBase.setActionClass("AIAction40", AIAction40)
AIActionBase.AIActionBase.setActionClass("AIAction41", AIAction41)
AIActionBase.AIActionBase.setActionClass("AIAction42", AIAction42)
AIActionBase.AIActionBase.setActionClass("AIAction43", AIAction43)
AIActionBase.AIActionBase.setActionClass("AIAction44", AIAction44)
AIActionBase.AIActionBase.setActionClass("AIAction45", AIAction45)
AIActionBase.AIActionBase.setActionClass("AIAction46", AIAction46)
AIActionBase.AIActionBase.setActionClass("AIAction47", AIAction47)
AIActionBase.AIActionBase.setActionClass("AIAction48", AIAction48)
AIActionBase.AIActionBase.setActionClass("AIAction49", AIAction49)
AIActionBase.AIActionBase.setActionClass("AIAction50", AIAction50)
AIActionBase.AIActionBase.setActionClass("AIAction51", AIAction51)
AIActionBase.AIActionBase.setActionClass("AIAction52", AIAction52)
AIActionBase.AIActionBase.setActionClass("AIAction53", AIAction53)
AIActionBase.AIActionBase.setActionClass("AIAction54", AIAction54)
AIActionBase.AIActionBase.setActionClass("AIAction55", AIAction55)
AIActionBase.AIActionBase.setActionClass("AIAction56", AIAction56)
AIActionBase.AIActionBase.setActionClass("AIAction57", AIAction57)
AIActionBase.AIActionBase.setActionClass("AIAction58", AIAction58)
AIActionBase.AIActionBase.setActionClass("AIAction59", AIAction59)
AIActionBase.AIActionBase.setActionClass("AIAction60", AIAction60)
AIActionBase.AIActionBase.setActionClass("AIAction61", AIAction61)
AIActionBase.AIActionBase.setActionClass("AIAction62", AIAction62)
AIActionBase.AIActionBase.setActionClass("AIAction63", AIAction63)
AIActionBase.AIActionBase.setActionClass("AIAction64", AIAction64)
AIActionBase.AIActionBase.setActionClass("AIAction65", AIAction65)
AIActionBase.AIActionBase.setActionClass("AIAction66", AIAction66)
AIActionBase.AIActionBase.setActionClass("AIAction67", AIAction67)
AIActionBase.AIActionBase.setActionClass("AIAction68", AIAction68)
AIActionBase.AIActionBase.setActionClass("AIAction69", AIAction69)
AIActionBase.AIActionBase.setActionClass("AIAction70", AIAction70)
AIActionBase.AIActionBase.setActionClass("AIAction71", AIAction71)
AIActionBase.AIActionBase.setActionClass("AIAction72", AIAction72)
AIActionBase.AIActionBase.setActionClass("AIAction73", AIAction73)
AIActionBase.AIActionBase.setActionClass("AIAction74", AIAction74)
AIActionBase.AIActionBase.setActionClass("AIAction75", AIAction75)
AIActionBase.AIActionBase.setActionClass("AIAction76", AIAction76)
AIActionBase.AIActionBase.setActionClass("AIAction77", AIAction77)
AIActionBase.AIActionBase.setActionClass("AIAction78", AIAction78)
AIActionBase.AIActionBase.setActionClass("AIAction79", AIAction79)
AIActionBase.AIActionBase.setActionClass("AIAction80", AIAction80)
AIActionBase.AIActionBase.setActionClass("AIAction81", AIAction81)
AIActionBase.AIActionBase.setActionClass("AIAction82", AIAction82)
AIActionBase.AIActionBase.setActionClass("AIAction83", AIAction83)
AIActionBase.AIActionBase.setActionClass("AIAction84", AIAction84)
AIActionBase.AIActionBase.setActionClass("AIAction85", AIAction85)
AIActionBase.AIActionBase.setActionClass("AIAction88", AIAction88)
AIActionBase.AIActionBase.setActionClass("AIAction89", AIAction89)
AIActionBase.AIActionBase.setActionClass("AIAction90", AIAction90)
AIActionBase.AIActionBase.setActionClass("AIAction91", AIAction91)
AIActionBase.AIActionBase.setActionClass("AIAction92", AIAction92)
AIActionBase.AIActionBase.setActionClass("AIAction93", AIAction93)
AIActionBase.AIActionBase.setActionClass("AIAction94", AIAction94)
AIActionBase.AIActionBase.setActionClass("AIAction95", AIAction95)
AIActionBase.AIActionBase.setActionClass("AIAction96", AIAction96)
AIActionBase.AIActionBase.setActionClass("AIAction97", AIAction97)
AIActionBase.AIActionBase.setActionClass("AIAction98", AIAction98)
AIActionBase.AIActionBase.setActionClass("AIAction99", AIAction99)
AIActionBase.AIActionBase.setActionClass("AIAction100", AIAction100)
AIActionBase.AIActionBase.setActionClass("AIAction101", AIAction101)
AIActionBase.AIActionBase.setActionClass("AIAction102", AIAction102)
AIActionBase.AIActionBase.setActionClass("AIAction103", AIAction103)
AIActionBase.AIActionBase.setActionClass("AIAction104", AIAction104)
AIActionBase.AIActionBase.setActionClass("AIAction105", AIAction105)
AIActionBase.AIActionBase.setActionClass("AIAction106", AIAction106)
AIActionBase.AIActionBase.setActionClass("AIAction107", AIAction107)
AIActionBase.AIActionBase.setActionClass("AIAction108", AIAction108)
AIActionBase.AIActionBase.setActionClass("AIAction109", AIAction109)
AIActionBase.AIActionBase.setActionClass("AIAction110", AIAction110)
AIActionBase.AIActionBase.setActionClass("AIAction111", AIAction111)
AIActionBase.AIActionBase.setActionClass("AIAction112", AIAction112)
AIActionBase.AIActionBase.setActionClass("AIAction113", AIAction113)
AIActionBase.AIActionBase.setActionClass("AIAction114", AIAction114)
AIActionBase.AIActionBase.setActionClass("AIAction115", AIAction115)
AIActionBase.AIActionBase.setActionClass("AIAction116", AIAction116)
AIActionBase.AIActionBase.setActionClass("AIAction117", AIAction117)
AIActionBase.AIActionBase.setActionClass("AIAction118", AIAction118)
AIActionBase.AIActionBase.setActionClass("AIAction119", AIAction119)
AIActionBase.AIActionBase.setActionClass("AIAction120", AIAction120)
AIActionBase.AIActionBase.setActionClass("AIAction121", AIAction121)
AIActionBase.AIActionBase.setActionClass("AIAction122", AIAction122)
AIActionBase.AIActionBase.setActionClass("AIAction123", AIAction123)
AIActionBase.AIActionBase.setActionClass("AIAction124", AIAction124)
AIActionBase.AIActionBase.setActionClass("AIAction125", AIAction125)
AIActionBase.AIActionBase.setActionClass("AIAction126", AIAction126)
AIActionBase.AIActionBase.setActionClass("AIAction127", AIAction127)
AIActionBase.AIActionBase.setActionClass("AIAction128", AIAction128)
AIActionBase.AIActionBase.setActionClass("AIAction129", AIAction129)
AIActionBase.AIActionBase.setActionClass("AIAction130", AIAction130)
AIActionBase.AIActionBase.setActionClass("AIAction131", AIAction131)
AIActionBase.AIActionBase.setActionClass("AIAction132", AIAction132)
AIActionBase.AIActionBase.setActionClass("AIAction133", AIAction133)
AIActionBase.AIActionBase.setActionClass("AIAction134", AIAction134)
AIActionBase.AIActionBase.setActionClass("AIAction135", AIAction135)
AIActionBase.AIActionBase.setActionClass("AIAction136", AIAction136)
AIActionBase.AIActionBase.setActionClass("AIAction137", AIAction137)
AIActionBase.AIActionBase.setActionClass("AIAction138", AIAction138)
AIActionBase.AIActionBase.setActionClass("AIAction139", AIAction139)
AIActionBase.AIActionBase.setActionClass("AIAction140", AIAction140)
AIActionBase.AIActionBase.setActionClass("AIAction141", AIAction141)
AIActionBase.AIActionBase.setActionClass("AIAction142", AIAction142)
AIActionBase.AIActionBase.setActionClass("AIAction143", AIAction143)
AIActionBase.AIActionBase.setActionClass("AIAction144", AIAction144)
AIActionBase.AIActionBase.setActionClass("AIAction145", AIAction145)
AIActionBase.AIActionBase.setActionClass("AIAction146", AIAction146)
AIActionBase.AIActionBase.setActionClass("AIAction147", AIAction147)
AIActionBase.AIActionBase.setActionClass("AIAction148", AIAction148)
AIActionBase.AIActionBase.setActionClass("AIAction149", AIAction149)
AIActionBase.AIActionBase.setActionClass("AIAction150", AIAction150)
AIActionBase.AIActionBase.setActionClass("AIAction151", AIAction151)
AIActionBase.AIActionBase.setActionClass("AIAction152", AIAction152)
AIActionBase.AIActionBase.setActionClass("AIAction153", AIAction153)
AIActionBase.AIActionBase.setActionClass("AIAction154", AIAction154)
AIActionBase.AIActionBase.setActionClass("AIAction155", AIAction155)
AIActionBase.AIActionBase.setActionClass("AIAction156", AIAction156)
AIActionBase.AIActionBase.setActionClass("AIAction157", AIAction157)
AIActionBase.AIActionBase.setActionClass("AIAction158", AIAction158)
AIActionBase.AIActionBase.setActionClass("AIAction159", AIAction159)
AIActionBase.AIActionBase.setActionClass("AIAction160", AIAction160)
AIActionBase.AIActionBase.setActionClass("AIAction161", AIAction161)
AIActionBase.AIActionBase.setActionClass("AIAction162", AIAction162)
AIActionBase.AIActionBase.setActionClass("AIAction163", AIAction163)
AIActionBase.AIActionBase.setActionClass("AIAction164", AIAction164)
AIActionBase.AIActionBase.setActionClass("AIAction165", AIAction165)
AIActionBase.AIActionBase.setActionClass("AIAction166", AIAction166)
AIActionBase.AIActionBase.setActionClass("AIAction167", AIAction167)
AIActionBase.AIActionBase.setActionClass("AIAction168", AIAction168)
AIActionBase.AIActionBase.setActionClass("AIAction169", AIAction169)
AIActionBase.AIActionBase.setActionClass("AIAction170", AIAction170)
AIActionBase.AIActionBase.setActionClass("AIAction171", AIAction171)
AIActionBase.AIActionBase.setActionClass("AIAction172", AIAction172)
AIActionBase.AIActionBase.setActionClass("AIAction173", AIAction173)
AIActionBase.AIActionBase.setActionClass("AIAction174", AIAction174)
AIActionBase.AIActionBase.setActionClass("AIAction175", AIAction175)
AIActionBase.AIActionBase.setActionClass("AIAction176", AIAction176)
AIActionBase.AIActionBase.setActionClass("AIAction177", AIAction177)
AIActionBase.AIActionBase.setActionClass("AIAction178", AIAction178)
AIActionBase.AIActionBase.setActionClass("AIAction179", AIAction179)
AIActionBase.AIActionBase.setActionClass("AIAction180", AIAction180)
AIActionBase.AIActionBase.setActionClass("AIAction181", AIAction181)
AIActionBase.AIActionBase.setActionClass("AIAction182", AIAction182)
AIActionBase.AIActionBase.setActionClass("AIAction183", AIAction183)
AIActionBase.AIActionBase.setActionClass("AIAction184", AIAction184)
AIActionBase.AIActionBase.setActionClass("AIAction185", AIAction185)
AIActionBase.AIActionBase.setActionClass("AIAction186", AIAction186)
AIActionBase.AIActionBase.setActionClass("AIAction187", AIAction187)
AIActionBase.AIActionBase.setActionClass("AIAction188", AIAction188)
AIActionBase.AIActionBase.setActionClass("AIAction189", AIAction189)
AIActionBase.AIActionBase.setActionClass("AIAction190", AIAction190)
AIActionBase.AIActionBase.setActionClass("AIAction191", AIAction191)
AIActionBase.AIActionBase.setActionClass("AIAction192", AIAction192)
AIActionBase.AIActionBase.setActionClass("AIAction193", AIAction193)
AIActionBase.AIActionBase.setActionClass("AIAction194", AIAction194)
AIActionBase.AIActionBase.setActionClass("AIAction195", AIAction195)
AIActionBase.AIActionBase.setActionClass("AIAction196", AIAction196)
AIActionBase.AIActionBase.setActionClass("AIAction197", AIAction197)
AIActionBase.AIActionBase.setActionClass("AIAction198", AIAction198)
AIActionBase.AIActionBase.setActionClass("AIAction199", AIAction199)
AIActionBase.AIActionBase.setActionClass("AIAction200", AIAction200)
AIActionBase.AIActionBase.setActionClass("AIAction201", AIAction201)
AIActionBase.AIActionBase.setActionClass("AIAction202", AIAction202)
AIActionBase.AIActionBase.setActionClass("AIAction203", AIAction203)
AIActionBase.AIActionBase.setActionClass("AIAction204", AIAction204)
AIActionBase.AIActionBase.setActionClass("AIAction205", AIAction205)
AIActionBase.AIActionBase.setActionClass("AIAction206", AIAction206)
AIActionBase.AIActionBase.setActionClass("AIAction207", AIAction207)
AIActionBase.AIActionBase.setActionClass("AIAction208", AIAction208)
AIActionBase.AIActionBase.setActionClass("AIAction209", AIAction209)
AIActionBase.AIActionBase.setActionClass("AIAction210", AIAction210)
AIActionBase.AIActionBase.setActionClass("AIAction211", AIAction211)
AIActionBase.AIActionBase.setActionClass("AIAction212", AIAction212)
AIActionBase.AIActionBase.setActionClass("AIAction213", AIAction213)
AIActionBase.AIActionBase.setActionClass("AIAction214", AIAction214)
AIActionBase.AIActionBase.setActionClass("AIAction215", AIAction215)
AIActionBase.AIActionBase.setActionClass("AIAction216", AIAction216)
AIActionBase.AIActionBase.setActionClass("AIAction217", AIAction217)
AIActionBase.AIActionBase.setActionClass("AIAction218", AIAction218)
AIActionBase.AIActionBase.setActionClass("AIAction219", AIAction219)
AIActionBase.AIActionBase.setActionClass("AIAction220", AIAction220)
AIActionBase.AIActionBase.setActionClass("AIAction221", AIAction221)
AIActionBase.AIActionBase.setActionClass("AIAction222", AIAction222)
AIActionBase.AIActionBase.setActionClass("AIAction223", AIAction223)
AIActionBase.AIActionBase.setActionClass("AIAction224", AIAction224)
AIActionBase.AIActionBase.setActionClass("AIAction225", AIAction225)
AIActionBase.AIActionBase.setActionClass("AIAction226", AIAction226)
AIActionBase.AIActionBase.setActionClass("AIAction227", AIAction227)
AIActionBase.AIActionBase.setActionClass("AIAction228", AIAction228)
AIActionBase.AIActionBase.setActionClass("AIAction229", AIAction229)
AIActionBase.AIActionBase.setActionClass("AIAction230", AIAction230)
AIActionBase.AIActionBase.setActionClass("AIAction231", AIAction231)
AIActionBase.AIActionBase.setActionClass("AIAction232", AIAction232)
AIActionBase.AIActionBase.setActionClass("AIAction233", AIAction233)
AIActionBase.AIActionBase.setActionClass("AIAction234", AIAction234)
AIActionBase.AIActionBase.setActionClass("AIAction235", AIAction235)
AIActionBase.AIActionBase.setActionClass("AIAction236", AIAction236)
AIActionBase.AIActionBase.setActionClass("AIAction237", AIAction237)
AIActionBase.AIActionBase.setActionClass("AIAction238", AIAction238)
AIActionBase.AIActionBase.setActionClass("AIAction239", AIAction239)
AIActionBase.AIActionBase.setActionClass("AIAction240", AIAction240)
AIActionBase.AIActionBase.setActionClass("AIAction241", AIAction241)
AIActionBase.AIActionBase.setActionClass("AIAction242", AIAction242)
AIActionBase.AIActionBase.setActionClass("AIAction243", AIAction243)
AIActionBase.AIActionBase.setActionClass("AIAction244", AIAction244)
AIActionBase.AIActionBase.setActionClass("AIAction245", AIAction245)
AIActionBase.AIActionBase.setActionClass("AIAction246", AIAction246)
AIActionBase.AIActionBase.setActionClass("AIAction247", AIAction247)
AIActionBase.AIActionBase.setActionClass("AIAction248", AIAction248)
AIActionBase.AIActionBase.setActionClass("AIAction249", AIAction249)
AIActionBase.AIActionBase.setActionClass("AIAction250", AIAction250)
AIActionBase.AIActionBase.setActionClass("AIAction251", AIAction251)
AIActionBase.AIActionBase.setActionClass("AIAction252", AIAction252)
AIActionBase.AIActionBase.setActionClass("AIAction253", AIAction253)
AIActionBase.AIActionBase.setActionClass("AIAction254", AIAction254)
AIActionBase.AIActionBase.setActionClass("AIAction255", AIAction255)
AIActionBase.AIActionBase.setActionClass("AIAction256", AIAction256)
AIActionBase.AIActionBase.setActionClass("AIAction257", AIAction257)
AIActionBase.AIActionBase.setActionClass("AIAction258", AIAction258)
AIActionBase.AIActionBase.setActionClass("AIAction259", AIAction259)
# AIActionBase.AIActionBase.setActionClass("AIAction260", AIAction260)
# AIActionBase.AIActionBase.setActionClass("AIAction261", AIAction261)
# AIActionBase.AIActionBase.setActionClass("AIAction262", AIAction262)
AIActionBase.AIActionBase.setActionClass("AIAction263", AIAction263)
AIActionBase.AIActionBase.setActionClass("AIAction264", AIAction264)
AIActionBase.AIActionBase.setActionClass("AIAction265", AIAction265)
AIActionBase.AIActionBase.setActionClass("AIAction266", AIAction266)
AIActionBase.AIActionBase.setActionClass("AIAction267", AIAction267)
AIActionBase.AIActionBase.setActionClass("AIAction268", AIAction268)
AIActionBase.AIActionBase.setActionClass("AIAction269", AIAction269)
AIActionBase.AIActionBase.setActionClass("AIAction270", AIAction270)
AIActionBase.AIActionBase.setActionClass("AIAction271", AIAction271)
AIActionBase.AIActionBase.setActionClass("AIAction272", AIAction272)
AIActionBase.AIActionBase.setActionClass("AIAction273", AIAction273)
AIActionBase.AIActionBase.setActionClass("AIAction274", AIAction274)
AIActionBase.AIActionBase.setActionClass("AIAction275", AIAction275)
AIActionBase.AIActionBase.setActionClass("AIAction276", AIAction276)
AIActionBase.AIActionBase.setActionClass("AIAction277", AIAction277)
AIActionBase.AIActionBase.setActionClass("AIAction278", AIAction278)
AIActionBase.AIActionBase.setActionClass("AIAction279", AIAction279)
AIActionBase.AIActionBase.setActionClass("AIAction280", AIAction280)
AIActionBase.AIActionBase.setActionClass("AIAction281", AIAction281)
AIActionBase.AIActionBase.setActionClass("AIAction282", AIAction282)
AIActionBase.AIActionBase.setActionClass("AIAction283", AIAction283)
AIActionBase.AIActionBase.setActionClass("AIAction284", AIAction284)
AIActionBase.AIActionBase.setActionClass("AIAction285", AIAction285)
AIActionBase.AIActionBase.setActionClass("AIAction286", AIAction286)
AIActionBase.AIActionBase.setActionClass("AIAction287", AIAction287)
AIActionBase.AIActionBase.setActionClass("AIAction288", AIAction288)
AIActionBase.AIActionBase.setActionClass("AIAction289", AIAction289)
AIActionBase.AIActionBase.setActionClass("AIAction290", AIAction290)
AIActionBase.AIActionBase.setActionClass("AIAction291", AIAction291)
AIActionBase.AIActionBase.setActionClass("AIAction292", AIAction292)
AIActionBase.AIActionBase.setActionClass("AIAction293", AIAction293)
AIActionBase.AIActionBase.setActionClass("AIAction294", AIAction294)
AIActionBase.AIActionBase.setActionClass("AIAction295", AIAction295)
AIActionBase.AIActionBase.setActionClass("AIAction296", AIAction296)
AIActionBase.AIActionBase.setActionClass("AIAction297", AIAction297)
AIActionBase.AIActionBase.setActionClass("AIAction298", AIAction298)
AIActionBase.AIActionBase.setActionClass("AIAction299", AIAction299)
AIActionBase.AIActionBase.setActionClass("AIAction300", AIAction300)
AIActionBase.AIActionBase.setActionClass("AIAction301", AIAction301)
AIActionBase.AIActionBase.setActionClass("AIAction302", AIAction302)
AIActionBase.AIActionBase.setActionClass("AIAction303", AIAction303)
AIActionBase.AIActionBase.setActionClass("AIAction304", AIAction304)
AIActionBase.AIActionBase.setActionClass("AIAction305", AIAction305)

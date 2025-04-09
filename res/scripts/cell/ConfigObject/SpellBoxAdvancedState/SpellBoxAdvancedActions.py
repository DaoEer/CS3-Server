# -*- coding: utf-8 -*-
"""
"""
import KBEngine
import KBEDebug

import csdefine
import Functions
import Math
from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase.SpellBoxAdvancedActionBase import SpellBoxAdvancedActionBase



class SpellBoxAdvancedAction1( SpellBoxAdvancedActionBase ):
	"""
	添加效果
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.effectIDList = section["param1"].split("|")
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		for effectID in self.effectIDList:
			effectID = int(effectID)
			entity.addFixIDHoldEffect(effectID, entity)


class SpellBoxAdvancedAction2( SpellBoxAdvancedActionBase ):
	"""
	移除效果
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.effectIDList = section["param1"].split("|")
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		for effectID in self.effectIDList:
			effectID = int(effectID)
			entity.removeFixIDHoldEffectByID(effectID)
		
class SpellBoxAdvancedAction3( SpellBoxAdvancedActionBase ):
	"""
	移除所有效果
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.removeAllFixIDHoldEffect()
		
class SpellBoxAdvancedAction4( SpellBoxAdvancedActionBase ):
	"""
	切换状态
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.status = int(section["param1"])
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		entity.changeInteractiveState(self.status)
		
class SpellBoxAdvancedAction5( SpellBoxAdvancedActionBase ):
	"""
	更新自身进度
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.scriptID = section["param1"]
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		#防弹罩怪物
		pos = entity.position
		dir = entity.direction
		entity.createMonster(self.scriptID, tuple(Math.Vector3((pos.x, pos.y-1, pos.z))), dir, {})
		
class SpellBoxAdvancedAction6( SpellBoxAdvancedActionBase ):
	"""
	加入交互列表
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.effectIDList = section["param1"].split("|")
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if triggerEntity is None:
			return
		
		for effectID in self.effectIDList:
			effectID = int(effectID)
			triggerEntity.addFixIDHoldEffect(effectID, triggerEntity)
			
		entity.addInteractiveTarget(triggerEntity.id)
		
class SpellBoxAdvancedAction7( SpellBoxAdvancedActionBase ):
	"""
	移除交互者的定身buff
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.buffID = int(section["param1"])
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		#移除交互者的定身buff
		for targetID in entity.interactiveTargets:
			target = KBEngine.entities.get(targetID, None)
			if target:
				target.removeBuffByID(self.buffID)
				
class SpellBoxAdvancedAction8( SpellBoxAdvancedActionBase ):
	"""
	从交互列表移除
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.effectIDList = section["param1"].split("|")
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if triggerEntity is None:
			return
		
		for effectID in self.effectIDList:
			effectID = int(effectID)
			triggerEntity.removeFixIDHoldEffectByID(effectID)
			
class SpellBoxAdvancedAction9( SpellBoxAdvancedActionBase ):
	"""
	添加阵眼
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.scriptID = section["param1"].split("|")
		self.position = section["param2"].split("|")
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		pos = entity.position
		dir = entity.direction
		
		if len(self.scriptID) != len(self.position):
			return
		
		for i in range(len(self.scriptID)):
			scriptID = self.scriptID[i]
			position = Functions.vector3TypeConvert(self.position[i])
			entity.createSpellBox(scriptID, tuple(Math.Vector3((pos.x+position[0], pos.y+position[1], pos.z+position[2]))), dir, {"masterID":entity.id, "teamID":entity.teamID})

class SpellBoxAdvancedAction10( SpellBoxAdvancedActionBase ):
	"""
	法阵给一定范围内的队内玩家加buff
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.radius = float(section["param1"])
		self.buffID = int(section["param2"])
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		players = entity.entitiesInRangeExtCircle(self.radius, "Role")

		for player in players:
			if player.isInTeam() and player.teamMailbox.id == entity.teamID:
				player.addBuff(player, self.buffID)
			
class SpellBoxAdvancedAction11( SpellBoxAdvancedActionBase ):
	"""
	法阵交互完成(玩家占领真言)（法阵）
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		id = entity.queryTemp("entityID", -1)
		dstEntity = KBEngine.entities.get(id)
		if dstEntity is None:
			KBEDebug.ERROR_MSG("not found entity(%d)" %(id))
			return
		
		if dstEntity.spaceID != entity.spaceID:
			return
		
		dstEntity.completeOccupyByRole()
		
class SpellBoxAdvancedAction12( SpellBoxAdvancedActionBase ):
	"""
	法阵交互未完成（Boss占领真言）（法阵）
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		id = entity.queryTemp("entityID", -1)
		dstEntity = KBEngine.entities.get(id)
		if dstEntity is None:
			KBEDebug.ERROR_MSG("not found entity(%d)" %(id))
			return
			
		if dstEntity.spaceID != entity.spaceID:
			return
		
		dstEntity.completeOccupyByBoss()
		
class SpellBoxAdvancedAction13( SpellBoxAdvancedActionBase ):
	"""
	加入交互列表（阵眼）
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.effectIDList = section["param1"].split("|")
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if triggerEntity is None:
			return
		
		for effectID in self.effectIDList:
			effectID = int(effectID)
			entity.addFixIDHoldEffect(effectID, triggerEntity)
			
		entity.addInteractiveTarget(triggerEntity.id)
		
class SpellBoxAdvancedAction14( SpellBoxAdvancedActionBase ):
	"""
	更新对应的真言腐化进度(百分比)
	"""
	def __init__( self ):
		"""
		"""
		SpellBoxAdvancedActionBase.__init__( self )

	def initData(self, section):
		"""
		"""
		SpellBoxAdvancedActionBase.initData(self, section)
		self.percent = int(section["param1"])
		
	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		id = entity.queryTemp("entityID", -1)
		dstEntity = KBEngine.entities.get(id)
		if dstEntity is None:
			KBEDebug.ERROR_MSG("not found entity(%d)" %(id))
			return
			
		if dstEntity.spaceID != entity.spaceID:
			return
		
		dstEntity.updateCorruptValue(self.percent)

SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction1", SpellBoxAdvancedAction1)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction2", SpellBoxAdvancedAction2)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction3", SpellBoxAdvancedAction3)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction4", SpellBoxAdvancedAction4)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction5", SpellBoxAdvancedAction5)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction6", SpellBoxAdvancedAction6)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction7", SpellBoxAdvancedAction7)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction8", SpellBoxAdvancedAction8)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction9", SpellBoxAdvancedAction9)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction10", SpellBoxAdvancedAction10)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction11", SpellBoxAdvancedAction11)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction12", SpellBoxAdvancedAction12)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction13", SpellBoxAdvancedAction13)
SpellBoxAdvancedActionBase.setActionClass("SpellBoxAdvancedAction14", SpellBoxAdvancedAction14)

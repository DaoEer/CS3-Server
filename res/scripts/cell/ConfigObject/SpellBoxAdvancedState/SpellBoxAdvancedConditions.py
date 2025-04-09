# -*- coding: utf-8 -*-
"""
"""
import KBEngine
import KBEDebug

import csdefine

from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase.SpellBoxAdvancedConditionBase import SpellBoxAdvancedConditionBase


class SpellBoxAdvancedCondition1( SpellBoxAdvancedConditionBase ):
	"""
	"""
	def __init__( self ):
		"""
		初始化
		"""
		SpellBoxAdvancedConditionBase.__init__( self )
		
	def initData( self, section ):
		"""
		virtual method
		@param	section	: 	存储数据的数据段
		@type	section	:	PyDataSection
		"""
		SpellBoxAdvancedConditionBase.initData( self, section )
	
	def check( self, ai, entity, args, triggerEntity ):
		"""
		vitural method
		@param	ai		: 	拥有此条件的AI  ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AI of instance, AIBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		#创建状态/关闭状态/查收状态/重启状态
		if entity.isInteractiveState(csdefine.INTERACTIVE_STATE_CREATE) \
			or entity.isInteractiveState(csdefine.INTERACTIVE_STATE_CLOSED) \
			or entity.isInteractiveState(csdefine.INTERACTIVE_STATE_ACCEPT)\
			or entity.isInteractiveState(csdefine.INTERACTIVE_STATE_REOPEN):
			return False
			
		if  entity.interactiveTargetNum and  len(entity.interactiveTargets) >= entity.interactiveTargetNum:
			return False
			
		if triggerEntity is None:
			return False

		if triggerEntity.id in entity.interactiveTargets:
			return False
		
		if entity.id == triggerEntity.id:
			return False
		
		if triggerEntity.spaceID != entity.spaceID:
			return False
		
		if triggerEntity.position.flatDistTo(entity.position) < entity.minGossipDis:
			return False
		
		if not triggerEntity.isInTeam() or triggerEntity.teamMailbox.id != entity.teamID:
			return 	False
			
		return True
		
class SpellBoxAdvancedCondition2( SpellBoxAdvancedConditionBase ):
	"""
	entity是否处于某些状态
	"""
	def __init__( self ):
		"""
		初始化
		"""
		SpellBoxAdvancedConditionBase.__init__( self )
		
	def initData( self, section ):
		"""
		virtual method
		@param	section	: 	存储数据的数据段
		@type	section	:	PyDataSection
		"""
		SpellBoxAdvancedConditionBase.initData( self, section )
		self.statusList = section["param1"].split("|")
	
	def check( self, ai, entity, args, triggerEntity ):
		"""
		vitural method
		@param	ai		: 	拥有此条件的AI  ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AI of instance, AIBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		for status in self.statusList:
			if entity.isInteractiveState(status):
				return True
		return False
		
class SpellBoxAdvancedCondition3( SpellBoxAdvancedConditionBase ):
	"""
	当前是否有某个buff
	"""
	def __init__( self ):
		"""
		初始化
		"""
		SpellBoxAdvancedConditionBase.__init__( self )
		
	def initData( self, section ):
		"""
		virtual method
		@param	section	: 	存储数据的数据段
		@type	section	:	PyDataSection
		"""
		SpellBoxAdvancedConditionBase.initData( self, section )
		self.buffID = section["param1"]
	
	def check( self, ai, entity, args, triggerEntity ):
		"""
		vitural method
		@param	ai		: 	拥有此条件的AI  ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AI of instance, AIBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		if triggerEntity is None:
			return False
			
		if triggerEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
			
		if len(triggerEntity.findBuffsByBuffID(self.buffID)) <= 0:
			return False
			
		return True


SpellBoxAdvancedConditionBase.setConditionClass( "SpellBoxAdvancedCondition1", SpellBoxAdvancedCondition1 )
SpellBoxAdvancedConditionBase.setConditionClass( "SpellBoxAdvancedCondition2", SpellBoxAdvancedCondition2 )
SpellBoxAdvancedConditionBase.setConditionClass( "SpellBoxAdvancedCondition3", SpellBoxAdvancedCondition3 )

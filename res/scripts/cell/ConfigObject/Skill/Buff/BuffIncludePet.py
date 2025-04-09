# -*- coding: utf-8 -*-

import KBEngine
import csdefine

from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffIncludePet( BuffHold ):
	"""
	连动幻兽buff，玩家会连动给幻兽
	"""
	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_PET_ACTIVE, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_PET_ACTIVE, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_PET_ACTIVE:
			if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				pet = KBEngine.entities.get( receiver.activePetID, None )
				if pet:
					if pDict["isActive"]:
						pet.addBuff(receiver, self.getID())
					else:
						pet.removeBuffByID( self.getID())
		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			pet = KBEngine.entities.get( receiver.activePetID, None )
			if pet:
				pet.addBuff( receiver, self.getID())

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			pet = KBEngine.entities.get( receiver.activePetID, None )
			if pet:
				pet.removeBuffByID( self.getID())

		BuffHold.doEnd( self, receiver, buffData, reason )
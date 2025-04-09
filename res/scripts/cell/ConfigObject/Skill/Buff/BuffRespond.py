# -*- coding: utf-8 -*-
import KBEngine
import csdefine
import KBEDebug
import csconst
import SkillTargetObjImpl
from ConfigObject.Skill.Buff.BuffHold import BuffHold
import ConfigObject.Skill.SkillBase.HitDefine as HitDefine
import ConfigObject.Skill.SkillBase.EventDefine as EventDefine

class BuffRespond( BuffHold ):
	"""
	事件响应Buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._triggerBuffEvent = EventDefine.ReceiverEventDefine()
		self._triggerHitList = HitDefine.BuffHitData()	

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._triggerBuffEvent.init( dictDat["TriggerBuffEvent"] )
		self._triggerHitList.init( dictDat["TriggerHitList"], self )


	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		self._triggerBuffEvent.registerBuffEvent( buffData, receiver )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		self._triggerBuffEvent.unRegisterBuffEvent( buffData, receiver )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if self._triggerBuffEvent.canTriggerEvent( eventType, pDict ):
			caster = KBEngine.entities.get( buffData.casterID, None )
			target = SkillTargetObjImpl.createTargetObjEntity( receiver )
			if caster:
				self._triggerHitList.onHit( self, caster, target, "_triggerHitList" )

		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )


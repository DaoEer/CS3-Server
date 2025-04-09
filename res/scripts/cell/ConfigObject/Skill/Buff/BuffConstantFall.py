# -*- coding: utf-8 -*-
import KBEDebug
import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffConstantFall( BuffHold ):
	"""
	匀速下落
	"""
	def __init__( self):
		BuffHold.__init__( self )

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			return BuffHold.addBuffCheck( self, caster, receiver )
	
	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_ROLE_END_FALL, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_ROLE_END_FALL, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_ROLE_END_FALL:
			receiver.removeBuffByID( buffData.buffID )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.CLIENT_StartConstantFall()

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		receiver.startFallingHeight = receiver.position.y
		receiver.client.CLIENT_EndConstantFall()
		BuffHold.doEnd( self, receiver, buffData, reason )

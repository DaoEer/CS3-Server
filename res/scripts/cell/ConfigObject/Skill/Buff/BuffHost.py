# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffHost( BuffHold ):
	"""
	主从buff(主)
	和BuffGuest关联
	"""
	def __init__( self ):
		BuffHold.__init__( self )

	def receive( self, caster, receiver ):
		if not self.addBuffCheck(caster, receiver) or not BuffHold.receive(self, caster, receiver):			#策划要求 主buff加不上，从buff也要关闭
			guestBuffIndex = receiver.queryTemp( "guestBuffIndex", -1 )
			caster.removeBuffByIndex(guestBuffIndex)
			receiver.removeTemp("guestBuffIndex")

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_BUFFGUEST_END, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_BUFFGUEST_END, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_BUFFGUEST_END:
			trigger = KBEngine.entities.get( triggerID, None )
			_guestBuffIndex = pDict.get( "guestBuffIndex", 0 )
			_buffindex = buffData.getTempData("guestBuffIndex",-1)
			if trigger and _guestBuffIndex == _buffindex:
				trigger.removeBuffByIndex( buffData.index )

		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		guestBuffIndex = receiver.queryTemp( "guestBuffIndex", -1 )
		if guestBuffIndex != -1:
			buffData.setTempData( "guestBuffIndex", guestBuffIndex )
			receiver.removeTemp("guestBuffIndex")

		BuffHold.doBegin( self, receiver, buffData )
		guest = KBEngine.entities.get( buffData.casterID )
		if guest and guest.isReal():
			if not guest.getBuffData(guestBuffIndex):
				receiver.removeBuffByIndex( buffData.index )
				return

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		guest = KBEngine.entities.get( buffData.casterID, None )
		_buffindex = buffData.getTempData("guestBuffIndex")
		if guest and _buffindex in guest.attrBuffs:
			guest.removeBuffByIndex(_buffindex)
		BuffHold.doEnd( self, receiver, buffData,reason )
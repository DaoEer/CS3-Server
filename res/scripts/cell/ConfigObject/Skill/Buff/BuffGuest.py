# -*- coding: utf-8 -*-

import KBEngine
import csstatus
import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffGuest( BuffHold ):
	"""
	主从buff(客)
	和BuffHost关联
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.buffHostId = 0  		#关联buff的id

	def addBuffCheck( self, caster, receiver ):
		"""
		检测主Buff的添加条件
		"""
		buffHost = receiver.getBuff( self.buffHostId )
		if not buffHost.addBuffCheck( receiver,caster ):
			return False
		if buffHost._replaceCondition.valid( receiver, caster, True ) == csstatus.SKILL_GO_ON:
			return False

		return BuffHold.addBuffCheck( self, caster, receiver )

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.buffHostId = int(dictDat["Param1"])

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		host = KBEngine.entities.get( buffData.casterID, None )
		if self.buffHostId and host:
			host.setTemp("guestBuffIndex",buffData.index)
			host.addBuff(receiver,self.buffHostId)

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		host = KBEngine.entities.get( buffData.casterID, None )
		BuffHold.doEnd( self, receiver, buffData,reason )
		if host:
			host.onBuffGuestEndEvent(buffData.index)		
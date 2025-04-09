# -*- coding: utf-8 -*-

import csdefine
#engine
import KBEngine
import Functions
import KBEMath
#cell
from ConfigObject.Skill.Buff.BuffLoop import BuffLoop


class BuffShenfengMiJing( BuffLoop ):
	"""
	神风秘径副本
	玩家骑上啸风鹰
	"""
	def __init__( self ):
		BuffLoop.__init__( self )

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffLoop.init( self, dictDat )
		self.flyRoute = dictDat["Param4"]

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffLoop.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_ROLE_DROP_GLEDE, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffLoop.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_ROLE_DROP_GLEDE, buffData.index )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffLoop.doBegin( self, receiver, buffData )
		receiver.client.CLIENT_RideCopyGlede(self.flyRoute)

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.client.CLIENT_DismountCopyGlede()
		BuffLoop.doEnd( self, receiver, buffData,reason )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_ROLE_DROP_GLEDE:
			isThrow = pDict.get( "isThrow", 0 )
			if not isThrow:
				receiver.removeBuffByIndex( buffData.index )



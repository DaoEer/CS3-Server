# -*- coding: utf-8 -*-

import csdefine
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffDark( BuffHold ):
	"""
	玩家处于一片漆黑中
	"""
	def __init__( self ):
		BuffHold.__init__( self )
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff目前只适用于玩家
			return BuffHold.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffDark ):		#移除其他同类buff
				receiver.removeBuffByID( buffData.buffID, csdefine.BUFF_END_RESON_BY_REPLACE )
		
		BuffHold.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		if receiver.getClient():
			receiver.client.EnterDark()
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		if receiver.getClient():
			receiver.client.EnterDark()
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		if reason != csdefine.BUFF_END_RESON_BY_REPLACE:
			receiver.allClients.LeaveDark()
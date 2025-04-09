# -*- coding: utf-8 -*-

import csdefine
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffLight( BuffHold ):
	"""
	能照明玩家一定范围
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.lightRange = 0.0
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.lightRange = float( dictDat["Param1"] ) if len( dictDat["Param1"] ) > 0 else 0.0
		
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffLight ):		#移除其他同类buff
				receiver.removeBuffByID( buffData.buffID, csdefine.BUFF_END_RESON_BY_REPLACE )
		
		BuffHold.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		if receiver.getClient():
			receiver.client.CLIENT_TurnOnLight( self.lightRange)
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		if receiver.getClient():
			receiver.client.CLIENT_TurnOnLight( self.lightRange )
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.client.CLIENT_TurnOffLight()
# -*- coding: utf-8 -*-

from ConfigObject.Skill.Buff.BuffHold import BuffHold
import csdefine


class BuffAimingThrowMode( BuffHold ):
	"""
	瞄准状态（晶石洞窟副本）
	"""
	def __init__( self ):
		BuffHold.__init__( self )
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData, reason )
		receiver.client.CLIENT_OnLeaveAimingThrowMode()
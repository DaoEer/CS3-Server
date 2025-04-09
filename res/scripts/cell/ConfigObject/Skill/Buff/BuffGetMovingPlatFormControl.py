# -*- coding: utf-8 -*-

import csdefine
#engine
import KBEngine
import KBEDebug
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffGetMovingPlatFormControl( BuffHold ):
	"""
	控制移动平台移动，转向
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

	
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffGetMovingPlatFormControl ):		#如果当前有此类型buff就不再重新添加
				return False
		
		BuffHold.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		#控制石台
		receiver.client.GetMovingPlatFormControl()
		KBEDebug.ERROR_MSG("GetMovingPlatFormControl")
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )

	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		#结束控制石台
		receiver.client.LoseMovingPlatFormControl()
		KBEDebug.ERROR_MSG("LoseMovingPlatFormControl")

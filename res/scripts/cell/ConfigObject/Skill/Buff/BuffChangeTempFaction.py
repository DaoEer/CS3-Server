# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffChangeTempFaction( BuffHold ):
	"""
	改变临时势力
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._faction = 0
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._faction = int(dictDat["Param1"])
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			return False
		return BuffHold.addBuffCheck( self, caster, receiver )
	
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffChangeTempFaction ):		#移除同类buff
				receiver.removeBuffByID( buffData.buffID, csdefine.BUFF_END_RESON_BY_REPLACE )
		BuffHold.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.setTempFaction( self._faction )
	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData, reason )
		if reason != csdefine.BUFF_END_RESON_BY_REPLACE:
			receiver.setTempFaction( 0 )
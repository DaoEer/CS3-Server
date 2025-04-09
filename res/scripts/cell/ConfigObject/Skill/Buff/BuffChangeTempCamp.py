# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffChangeTempCamp( BuffHold ):
	"""
	改变临时阵营
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._camp = 0
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._camp = int(dictDat["Param1"])
		if self._camp not in csdefine.CAMP_LIST:
			KBEDebug.ERROR_MSG("Buff(%s) config error camp:%s!" % (self.getID(), self._camp))
	
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffChangeTempCamp ):		#移除同类buff
				receiver.removeBuffByID( buffData.buffID, csdefine.BUFF_END_RESON_BY_REPLACE )
		BuffHold.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.setTempCamp( self._camp )
	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData, reason )
		if reason != csdefine.BUFF_END_RESON_BY_REPLACE:
			receiver.setTempCamp( csdefine.CMAP_NONE )
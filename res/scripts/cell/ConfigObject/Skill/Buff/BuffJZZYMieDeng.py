# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffJZZYMieDeng( BuffHold ):
	"""
	灭灯（CST-4246 九字真言）
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		#灭多少
		self._amount = 0
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._amount = int(dictDat["Param1"])
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER: #此buff只给Monster
			return BuffHold.addBuffCheck( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		spaceEntity = receiver.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onExtinguishLight(spaceEntity, self._amount)
		

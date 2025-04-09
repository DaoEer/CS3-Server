# -*- coding: utf-8 -*-
import csdefine
import KBEngine
from ConfigObject.Skill.Buff.BuffBeLink import BuffBeLink


class BuffBeHook( BuffBeLink ):
	"""
	被钩buff
	"""
	def __init__( self ):
		BuffBeLink.__init__( self )
		self._speed = 0

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffBeLink.init( self, dictDat )
		if self._loopTime == 0.0:		# CST-9200提供缺省支持
			self._loopTime = 1.0
		if dictDat["Param2"]:
			self._speed = float(dictDat["Param2"])

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff不能给玩家
			return False

		return BuffBeLink.addBuffCheck( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffBeLink.doBegin( self, receiver, buffData )
		caster = KBEngine.entities.get( buffData.casterID )
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			receiver.changeState(csdefine.ENTITY_STATE_SHOW)
		receiver.moveToPointExt(caster.position, self._speed, 0.1)

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.resetEnemyList()
		receiver.changeState(csdefine.ENTITY_STATE_FREE)
		BuffBeLink.doEnd( self, receiver, buffData,reason )	

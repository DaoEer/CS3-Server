# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
from ConfigObject.Skill.Buff.BuffLink import BuffLink


class BuffHook( BuffLink ):
	"""
	钩取buff
	"""
	def __init__( self ):
		BuffLink.__init__( self )
		self.__Mindistance = 0.0
		self._triggerSkillId = 0

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffLink.init( self, dictDat )
		if self._loopTime == 0.0:		# CST-9200提供缺省支持
			self._loopTime = 1.0
		if dictDat["Param3"]:
			self.__Mindistance = float(dictDat["Param3"])
		if dictDat["Param4"]:
			self._triggerSkillId = int(dictDat["Param4"])

	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffLink.doLoopHit( self, receiver, buffData )
		beLinker = KBEngine.entities.get( buffData.casterID )
		if self.__Mindistance > 0:
			if receiver and beLinker:
				if receiver.position.distTo( beLinker.position ) < self.__Mindistance:
					if self._triggerSkillId:
						receiver.useSkillToEntity( self._triggerSkillId, buffData.casterID )
					receiver.removeBuff( buffData.index )
# -*- coding: utf-8 -*-


import csdefine
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffLoop import BuffLoop

class BuffReplace(BuffLoop):
	"""
	可顶替Buff
	"""
	def __init__(self ):
		BuffLoop.__init__(self)
		self._replaceType = 0			# 顶替类型
		self._replacePriority = 0		# 顶替优先级

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffLoop.init( self, dictDat )

		if dictDat["Param1"] and int(dictDat["Param1"])>0:
			self._replaceType = int(dictDat["Param1"])

		if dictDat["Param2"]:
			self._replacePriority = int(dictDat["Param2"])

	def addBuffCheck( self, caster, receiver ):
		"""
		检测buff是可以替换
		如能替换就在此处移除buff效果
		"""
		tempBuffDataList = list(receiver.getAttrBuffs().values())
		for buffData in tempBuffDataList:
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffReplace ) and buff._replaceType == self._replaceType:
				if self._replacePriority >= buff._replacePriority:
					receiver.removeBuffByID( buffData.buffID )
				else:
					return False
		return BuffLoop.addBuffCheck( self, caster, receiver )




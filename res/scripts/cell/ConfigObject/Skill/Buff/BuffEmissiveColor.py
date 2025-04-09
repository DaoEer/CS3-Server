# -*- coding: utf-8 -*-


import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffEmissiveColor( BuffHold ):
	"""
	材质自发光Buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._alpha = 0.0 # 蒙版修正
		self._conflictPriority = csdefine.BUFF_CONFLICT_PRIORITY_PERF
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_MATERIAL)

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._filterColor = dictDat["Param1"].split("|")
		self._alpha = float(dictDat["Param2"])

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.allClients.OnRage(receiver.id,float(self._filterColor[0]),float(self._filterColor[1]),float(self._filterColor[2]),self._alpha)

	def doReload( self, effectData, receiver ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.allClients.OnRage(receiver.id,float(self._filterColor[0]),float(self._filterColor[1]),float(self._filterColor[2]),self._alpha)

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.allClients.EndRage(receiver.id)
		BuffHold.doEnd( self, receiver, buffData,reason )
		
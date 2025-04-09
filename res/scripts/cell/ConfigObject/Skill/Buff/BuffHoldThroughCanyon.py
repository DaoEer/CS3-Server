# -*- coding: utf-8 -*-


"""
usage:
	buff

attribute:
	pass

member function:
	pass

callback:
	pass

"""

#engine
import KBEngine
import KBEDebug
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#common
import csdefine



class BuffHoldThroughCanyon( BuffHold ):
	"""
	穿越峡谷表现
	玩家 坐上飞行道具，并自动向前下方滑行
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._mountModelId = ""						# 飞行载具模型
		self._forwardSpeed = 0.0					# 自动向前的速度
		self._downSpeed = 0.0						# 自动向下的速度

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._mountModelId = dictDat["Param1"]
		if dictDat["Param2"]:
			self._forwardSpeed = float( dictDat["Param2"])
		if dictDat["Param3"]:
			self._downSpeed = float( dictDat["Param3"])
	
	def doBegin( self, receiver, buffData ):
		"""
		变换开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.allClients.OnStartThroughCanyon(self._mountModelId, self._forwardSpeed, self._downSpeed)

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.allClients.OnStartThroughCanyon(self._mountModelId, self._forwardSpeed, self._downSpeed)

	def doEnd( self, receiver, buffData,reason ):
		"""
		变换结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.allClients.OnEndThroughCanyon()
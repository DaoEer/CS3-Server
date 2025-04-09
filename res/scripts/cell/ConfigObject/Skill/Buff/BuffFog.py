# -*- coding: utf-8 -*-

import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffFog( BuffHold ):
	"""
	迷雾buff,以摄像机为中心点
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._fogType = 0
		self._efogDensity = 0.0
		self._evisibleDistance = 0.0
		self._eheightFalloff = 0.0
		self._enterTime = 0.0
		self._ofogDensity = 0.0
		self._ovisibleDistance = 0.0
		self._oheightFalloff = 0.0
		self._outTime = 0.0

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._fogType = int(dictDat["Param1"])
		enterList = dictDat["Param2"].split("|")
		self._efogDensity = float(enterList[0])
		self._evisibleDistance = float(enterList[1])
		if len(enterList) > 2:
			self._eheightFalloff = float(enterList[2])
		outList = dictDat["Param3"].split("|")
		self._ofogDensity = float(outList[0])
		self._ovisibleDistance = float(outList[1])
		if len(outList) > 2:
			self._oheightFalloff = float(outList[2])
		timeList = dictDat["Param4"].split("|")
		self._enterTime = float(timeList[0])
		self._outTime = float(timeList[1])

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			return BuffHold.addBuffCheck( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.CLIENT_StartFog(self._fogType, self._efogDensity, self._evisibleDistance, self._eheightFalloff, self._enterTime)


	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.client.CLIENT_StartFog(self._fogType, self._efogDensity, self._evisibleDistance, self._eheightFalloff, self._enterTime)


	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.client.CLIENT_EndFog(self._fogType, self._ofogDensity, self._ovisibleDistance, self._oheightFalloff, self._outTime)
		BuffHold.doEnd( self, receiver, buffData,reason )

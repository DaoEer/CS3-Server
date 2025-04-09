# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#common
import csdefine

class BuffLXDistortScene(BuffHold):
	"""
	屏幕螺旋扭曲效果的Buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._rotationAngle = 0.0 		# 旋转角度
		self._maskScale = 0.0 			# 遮罩大小
		self._startTime = 0.0			# 淡入时间
		self._endTime = 0.0				# 淡出时间
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		if dictDat["Param1"] != "":
			self._rotationAngle = float(dictDat["Param1"])
		if dictDat["Param2"] != "":
			self._maskScale = float(dictDat["Param2"])
		if dictDat["Param3"] != "":
			self._startTime = float(dictDat["Param3"])
		if dictDat["Param4"] != "":
			self._endTime = float(dictDat["Param4"])
		
	def receiveSuccess( self, caster, receiver ):
		"""
		"""
		tempBuffDataList = list(receiver.getAttrBuffs().values())
		for buffData in tempBuffDataList:
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffLXDistortScene ):
				receiver.removeBuffByID( buffData.buffID )
		BuffHold.receiveSuccess( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.LXDistortScene(self._rotationAngle, self._maskScale, self._startTime, self._endTime, self._holdTime)

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.client.LXDistortScene(self._rotationAngle, self._maskScale, self._startTime, self._endTime,self._holdTime)
		
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )


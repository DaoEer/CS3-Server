# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#common
import csdefine

class BuffDistortScene(BuffHold):
	"""
	屏幕扭曲效果的Buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._startTime = 0.0	# 淡入时间
		self._endTime = 0.0		# 淡出时间
		self._distortion = 0.0	# 扭曲强度
		self._filterColor = "1|1|1"	# 滤镜 R|G|B
		self._maskColor = "1|1|1|0" # 蒙版修正

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		if dictDat["Param1"] != "":
			self._startTime = float(dictDat["Param1"])
		if dictDat["Param2"] != "":
			self._endTime = float(dictDat["Param2"])
		if dictDat["Param3"] != "":
			self._distortion = float(dictDat["Param3"])
		if dictDat["Param4"] != "":
			self._filterColor = dictDat["Param4"]
		if dictDat["Param5"] != "":
			self._maskColor = dictDat["Param5"]


	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		return BuffHold.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		"""
		tempBuffDataList = list(receiver.getAttrBuffs().values())
		for buffData in tempBuffDataList:
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffDistortScene ):
				receiver.removeBuffByID( buffData.buffID )
		BuffHold.receiveSuccess( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.DistortScene(self._distortion, self._filterColor, self._startTime, self._endTime, 0.0, self._maskColor)

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.client.DistortScene(self._distortion, self._filterColor, self._startTime, self._endTime, 0.0, self._maskColor)
		
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		if receiver.client:
			receiver.client.EndDistortScene()
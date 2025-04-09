# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#common
import csdefine


class BuffOverLookScene(BuffHold):
	"""
	镜头俯瞰Buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._cameraLoaction = ""		# 摄像机位置基于玩家位置偏移量
		self._cameraRotation = ""		# 摄像机旋转基于玩家位置偏移量
		self._startTime = 0.0 			# 开始时间
		self._loopTime = 0.0			# 持续时间
		self._endTime = 0.0				# 结束时间

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._cameraLoaction = dictDat["Param1"]
		self._cameraRotation = dictDat["Param2"]
		if dictDat["Param3"] != "":	
			self._startTime = float(dictDat["Param3"])		
		if dictDat["Param4"] != "":
			self._loopTime = float(dictDat["Param4"])
		if dictDat["Param5"] != "":
			self._endTime = float(dictDat["Param5"])

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		return BuffHold.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		"""
		tempBuffDataList = list(receiver.getAttrBuffs().values())
		for buffData in tempBuffDataList:
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffOverLookScene ):
				receiver.removeBuffByID( buffData.buffID )
		BuffHold.receiveSuccess( self, caster, receiver )


	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.StartOverLookScene(self._cameraLoaction, self._cameraRotation, self._startTime, self._loopTime, self._endTime)

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.client.StartOverLookScene(self._cameraLoaction, self._cameraRotation, self._startTime, self._loopTime, self._endTime)

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.client.EndOverLookScene(self._endTime)
		BuffHold.doEnd( self, receiver, buffData,reason )

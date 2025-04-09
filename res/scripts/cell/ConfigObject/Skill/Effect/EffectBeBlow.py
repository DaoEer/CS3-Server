# -*- coding: utf-8 -*-

import csdefine
import Math
import KBEMath
import csarithmetic
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase


class EffectBeBlow(EffectSkillBase):
	"""
	吹风效果
	"""
	def __init__(self):
		EffectSkillBase.__init__( self )
		self._windDirection = (0,0,0)	#风向
		self._speed = 0.0		# 速度
		self._time = 0.0		# 时间

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )

		if dictDat["Param1"]:
			self._speed = float(dictDat["Param1"])
		if dictDat["Param2"]:
			self._time = float(dictDat["Param2"])

	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if not receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:	#只支持对玩家使用
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		self._windDirection = KBEMath.KBEngine2UnrealDirection(Math.Vector3(0,0,csarithmetic.getYawByVector3(receiver.position-caster.position)))
		receiver.allClients.AddAxternalVelocity( self._windDirection[0], self._windDirection[1], self._windDirection[2], self._speed )
		receiver.addTimerCallBack(self._time, "timerRemoveAxternalVelocity", (self._windDirection[0], self._windDirection[1], self._windDirection[2], self._speed) )


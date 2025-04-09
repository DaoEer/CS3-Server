# -*- coding: utf-8 -*-


import Functions
import csdefine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect


class HoldEffectBeBlow( HoldEffect ):
	"""
	吹风效果：给玩家添加一个外部的速度
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._windDirection = (0,0,0)	#风向
		self._windSpeed = 0.0		#风速
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self._windDirection = Functions.vector3TypeConvert( dictDat["Param1"] )
		if dictDat["Param2"]:
			self._windSpeed = float( dictDat["Param2"] )
	
	def canEffect( self, caster, receiver ):
		"""
		效果添加检测
		"""
		return HoldEffect.canEffect( self, caster, receiver )

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.client.AddAxternalVelocity( self._windDirection[0], self._windDirection[1], self._windDirection[2], self._windSpeed )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
			receiver.getScript().addBlow( receiver, self._windDirection, self._windSpeed )

	def onClientActorCreate( self, effectData, receiver, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
			receiver.getScript().addBlow( receiver, self._windDirection, self._windSpeed, srcEntityID )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.client.RemoveAxternalVelocity( self._windDirection[0], self._windDirection[1], self._windDirection[2], self._windSpeed )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
			receiver.getScript().endBlow( receiver )
		HoldEffect.onEnd( self, effectData, receiver )
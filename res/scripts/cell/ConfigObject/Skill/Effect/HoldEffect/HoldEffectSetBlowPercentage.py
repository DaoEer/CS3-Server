# -*- coding: utf-8 -*-


import csdefine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect


class HoldEffectSetBlowPercentage( HoldEffect ):
	"""
	更改额外风力百分比（与HoldEffectBeBlow一起使用，更改后风的速度为 speed = speed + speed * Percentage）
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._percentage = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._percentage = float( dictDat["Param1"] )
	
	def canEffect( self, caster, receiver ):
		"""
		效果添加检测
		"""
		if not receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:	#只支持对玩家使用
			return False
		return HoldEffect.canEffect( self, caster, receiver )

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.client.ChangeAxternalPercentage( self._percentage )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.client.ChangeAxternalPercentage( 0.0 )
		HoldEffect.onEnd( self, effectData, receiver )
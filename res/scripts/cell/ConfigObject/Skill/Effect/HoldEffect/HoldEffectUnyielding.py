# -*- coding: utf-8 -*-


import csdefine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect

class HoldEffectUnyielding( HoldEffect ):
	"""
	不屈效果：玩家的生命值掉到1点后，将不会在扣除。
	"""
	def __init__( self ):
		HoldEffect.__init__( self )

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )


	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.effectStateInc( csdefine.EFFECT_STATE_UNYIELDING )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.effectStateDec( csdefine.EFFECT_STATE_UNYIELDING )
		HoldEffect.onEnd( self, effectData, receiver )
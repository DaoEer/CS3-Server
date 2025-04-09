# -*- coding: utf-8 -*-

from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect


class HoldEffectAddKvDecayRate( HoldEffect ):
	"""
	增加杀气值衰减速率
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._addRate = 0.0	#增加百分比
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._addRate = float( dictDat["Param1"] )

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		addValue = int( receiver.kvDecayRate * self._addRate )
		effectData.setTempData( "addValue", addValue )
		receiver.kvDecayRate += addValue

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		addValue = effectData.getTempData( "addValue" )
		receiver.kvDecayRate -= addValue

		HoldEffect.onEnd( self, effectData, receiver )


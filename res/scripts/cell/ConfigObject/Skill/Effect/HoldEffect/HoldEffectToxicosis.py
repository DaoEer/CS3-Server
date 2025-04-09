# -*- coding: utf-8 -*-

#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine


class HoldEffectToxicosis( HoldEffect ):
	"""
	中毒表现的全屏动态效果
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
		if hasattr(receiver, "client") and receiver.client:
			receiver.client.EnterToxicosis()

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		if hasattr(receiver, "client") and receiver.client:
			receiver.client.LeaveToxicosis()
		HoldEffect.onEnd( self, effectData, receiver )


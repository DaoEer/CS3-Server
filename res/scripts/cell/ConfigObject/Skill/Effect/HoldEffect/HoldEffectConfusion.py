# -*- coding: utf-8 -*-


"""
usage:
	Buff持有效果,onBegin 和 onEnd 必须成对存在，分别做buff添加和删除，增添的效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine


class HoldEffectConfusion( HoldEffect ):
	"""
	持有效果：混乱（PC无法被控制，乱走）
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
		receiver.effectStateInc( csdefine.EFFECT_STATE_CONFUSION )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.client.onBeginConfusion()

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.effectStateDec( csdefine.EFFECT_STATE_CONFUSION )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.client.onEndConfusion()
		HoldEffect.onEnd( self, effectData, receiver )


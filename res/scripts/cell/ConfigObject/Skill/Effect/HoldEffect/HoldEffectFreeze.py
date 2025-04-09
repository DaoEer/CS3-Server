# -*- coding: utf-8 -*-

#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine

class HoldEffectFreeze(HoldEffect):
	"""
	持有效果：冻结
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
		receiver.stopMovingForType( csdefine.SYSTEM_MOVE )
		receiver.effectStateInc( csdefine.EFFECT_STATE_FREEZE )
		receiver.allClients.Frozee()

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.effectStateDec( csdefine.EFFECT_STATE_FREEZE )
		if not receiver.hasEffectState(csdefine.EFFECT_STATE_FREEZE):
			receiver.allClients.Unfreeze()
		HoldEffect.onEnd( self, effectData, receiver )

	def onClientActorCreate( self, effectData, receiver, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		HoldEffect.onClientActorCreate( self, effectData, receiver, srcEntityID )
		receiver.allClients.Frozee()
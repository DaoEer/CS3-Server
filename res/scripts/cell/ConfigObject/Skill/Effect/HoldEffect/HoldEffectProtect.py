#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine


class HoldEffectProtect( HoldEffect ):
	"""
	持有效果：保护
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
		receiver.isInPending = 1
		receiver.effectStateInc( csdefine.EFFECT_STATE_PROTECT )
		receiver.updateRelation()
		#如果受术者是玩家，其手下（幻兽，召唤怪）进入准备AI状态
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			receiver.addCallEntityProtect()

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.effectStateDec( csdefine.EFFECT_STATE_PROTECT )
		receiver.updateRelation()
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			receiver.removeCallEntityProtect()
		if not receiver.hasEffectState( csdefine.EFFECT_STATE_PROTECT ) and receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			receiver.reTriggerNearTrap()
		receiver.isInPending = 0
		HoldEffect.onEnd( self, effectData, receiver )
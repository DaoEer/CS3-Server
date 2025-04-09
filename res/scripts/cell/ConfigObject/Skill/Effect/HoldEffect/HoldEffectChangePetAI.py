# -*- coding: utf-8 -*-


"""
"""


#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine
import KBEDebug



class HoldEffectChangePetAI( HoldEffect ):
	"""
	改变幻兽AI行为模式
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._petAINum = ""					# 见DT_PetSTAICfg
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self._petAINum = dictDat["Param1"]


	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET ):
			owner = receiver.getOwnerEntity()
			if owner:
				owner.client.OnChangePetAI( self._petAINum )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET ):
			owner = receiver.getOwnerEntity()
			if owner:
				owner.client.OnFinishChangePetAI()
		HoldEffect.onEnd(self, effectData, receiver)



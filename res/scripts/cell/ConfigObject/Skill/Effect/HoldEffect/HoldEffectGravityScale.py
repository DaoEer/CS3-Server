# -*- coding: utf-8 -*-

#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine


class HoldEffectGravityScale(HoldEffect):
	"""
	持有效果：重力加速度修正
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._attrPercent = 0.0
		self._attrValue = 0.0	

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		if dictDat["Param1"]:
			propertiesList = dictDat["Param1"].split("|")
			self._attrPercent = float(propertiesList[0])
			if len(propertiesList) > 1:
				self._attrValue = float(propertiesList[1])

	def canEffect( self, caster, receiver ):
		"""
		效果添加检测
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		return HoldEffect.canEffect( self, caster, receiver )

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.client.OnSetPlayerAddGravityScale(self._attrPercent, self._attrValue)

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.client.OnSetPlayerAddGravityScale(-self._attrPercent, -self._attrValue)	
		HoldEffect.onEnd( self, effectData, receiver )

	def onClientActorCreate( self, effectData, receiver, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		HoldEffect.onClientActorCreate( self, effectData, receiver, srcEntityID )
		receiver.client.OnSetPlayerAddGravityScale(self._attrPercent, self._attrValue)
# -*- coding: utf-8 -*-

import csdefine
import KBEngine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect

class HoldEffectFabaoPlayEffect( HoldEffect ):
	"""
	法宝 播放动作、光效、音效
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self.action = ""
		self.effect = ""
		self.playtime = ""
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self.action = dictDat["Param1"]
		self.effect = dictDat["Param2"]
		self.playtime = dictDat["Param3"]

	
	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		casterID = effectData.casterID
		caster = KBEngine.entities.get(casterID,None)
		if not caster:
			return
		caster.allClients.FabaoPlayEffect(receiver.id, caster.id, self.action, self.effect, self.playtime)
	
	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		casterID = effectData.casterID
		caster = KBEngine.entities.get(casterID,None)
		if not caster:
			return
		caster.allClients.FabaoPlayEffectEnd()
		HoldEffect.onEnd( self, effectData, receiver )
	
	
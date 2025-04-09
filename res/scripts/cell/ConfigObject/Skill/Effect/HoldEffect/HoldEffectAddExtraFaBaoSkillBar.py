# -*- coding: utf-8 -*-

import csdefine
import KBEngine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect

class HoldEffectAddExtraFaBaoSkillBar( HoldEffect ):
	"""
	法宝额外技能栏
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self.skillIDStr = ""		#法宝技能
		
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		if len( dictDat["Param1"].strip() ):
			self.skillIDStr = dictDat["Param1"].strip()
	
	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.client.ShowBuffExtraFaBaoSkillBar(self.skillIDStr)
	
	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.client.CloseBuffExtraFaBaoSkillBar()

		HoldEffect.onEnd( self, effectData, receiver )
	
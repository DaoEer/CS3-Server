# -*- coding: utf-8 -*-

import csdefine
import KBEngine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect

class HoldEffectCreateFaBao( HoldEffect ):
	"""
	创建法宝
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self.fabaoName = ""


	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self.fabaoName = dictDat["Param1"]

	
	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		receiver.allClients.CreateFaBao(receiver.id, self.fabaoName)
	
	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.allClients.RemoveFaBao()
	
	
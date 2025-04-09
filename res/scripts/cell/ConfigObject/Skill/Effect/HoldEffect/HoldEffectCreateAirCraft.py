# -*- coding: utf-8 -*-

import csdefine
import KBEngine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect

class HoldEffectCreateAirCraft( HoldEffect ):
	"""
	创建飞行器
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self.flyBindMeshID = ""
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self.flyBindMeshID = dictDat["Param1"].strip()


	def canEffect( self, caster, receiver ):
		"""
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		return HoldEffect.canEffect(self, caster, receiver)

	
	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		receiver.allClients.CLIENT_CreateAircraft(self.flyBindMeshID, receiver.id)
	
	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.allClients.CLIENT_RemoveAircraft(receiver.id)
	
	
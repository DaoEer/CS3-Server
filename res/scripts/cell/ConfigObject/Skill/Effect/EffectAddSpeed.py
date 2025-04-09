# -*- coding: utf-8 -*-


import Functions
import csdefine
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase


class EffectAddSpeed( EffectSkillBase ):
	"""
	根据玩家朝向添加一个速度
	"""
	def __init__( self ):
		self._dire = 0				# 方向
		self._forceSpeed = 0.0		# 速度
		self._forceTime = 0.0		# 时间
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._dire = int( dictDat["Param1"] )
		if dictDat["Param2"]:
			self._forceSpeed = float( dictDat["Param2"] )
		if dictDat["Param3"]:
			self._forceTime = float( dictDat["Param3"] )
	
	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if not receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:	#只支持对玩家使用
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		receiver.allClients.AddFlyForce( self._dire, self._forceSpeed, self._forceTime )

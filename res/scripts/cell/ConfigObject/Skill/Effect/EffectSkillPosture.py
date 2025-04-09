# -*- coding: utf-8 -*-

#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine

class EffectSkillPosture( EffectSkillBase ):
	"""
	切换心法效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._skillPosture = 0
		self._skillPostureLevel = 0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._skillPosture = int( dictDat["Param1"] )
		self._skillPostureLevel = int( dictDat["Param2"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		EffectSkillBase.onReceive( self, skill, caster, receiver )
		receiver.changeSkillPosture( self._skillPosture, self._skillPostureLevel, skill )
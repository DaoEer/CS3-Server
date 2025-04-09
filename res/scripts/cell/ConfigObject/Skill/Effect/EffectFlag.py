# -*- coding: utf-8 -*-


#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase

class EffectFlag( EffectSkillBase ):
	"""
	停止飞行传送效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._operation = 0
		self._flags = []

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._operation = int( dictDat["Param1"] )
		self._flags =  [int(i) for i in  dictDat["Param2"].split("|")]

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		for flag in self._flags:
			if self._operation:
				receiver.addFlag(flag)		
			else:
				receiver.removeFlag(flag)


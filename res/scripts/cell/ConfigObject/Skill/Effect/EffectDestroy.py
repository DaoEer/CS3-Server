# -*- coding: utf-8 -*-


from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase


class EffectDestroy( EffectSkillBase ):
	"""
	销毁
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		receiver.delayDestroy(0.1)	#延时0.1秒，让技能流程走完




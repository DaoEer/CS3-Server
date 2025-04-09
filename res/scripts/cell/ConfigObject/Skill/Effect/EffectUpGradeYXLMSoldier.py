# -*- coding: utf-8 -*-


from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import csconst

class EffectUpGradeYXLMSoldier( EffectSkillBase ):
	"""
	英雄王座升级小兵
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
		if receiver.levelYXLM < csconst.MONSTERYXLM_MAX_LEVEL:
			receiver.setlevelYXLM( (receiver.levelYXLM + 1) )
		

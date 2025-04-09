# -*- coding: utf-8 -*-

#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine

class EffectRequestSkill( EffectSkillBase ):
	"""
	触发一个技能申请
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._skillID = 0	

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._skillID = int( dictDat["Param1"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		useSkill = caster.getSkill(self._skillID)			
		if useSkill.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_POSITION:
			caster.useSkillToPosition(self._skillID,receiver.position)
		else:
			caster.useSkillToEntity( self._skillID, receiver.id)




		
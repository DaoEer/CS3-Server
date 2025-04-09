# -*- coding: utf-8 -*-


from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import csdefine

class EffectUpdateScoreForLHSL( EffectSkillBase ):
	"""
	灵魂狩猎副本专用
	更新计分
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
		if receiver.getEntityFlag()==csdefine.ENTITY_FLAG_ROLE:
			return
		spaceEntity = receiver.getCurrentSpace()
		obj = spaceEntity.getScript()
		obj.updateScore_2(spaceEntity, receiver.scriptID)
		




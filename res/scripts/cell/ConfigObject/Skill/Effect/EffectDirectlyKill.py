# -*- coding: utf-8 -*-

#common
import csdefine
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase

class EffectDirectlyKill(EffectSkillBase):
	"""
	直接击杀效果
	"""
	def __init__(self):
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
		virtual method;
		效果开始
		"""
		receiver.changeState(csdefine.ENTITY_STATE_DEAD)
		receiver.onBeKill(caster.id, 0, self._actForbid)
		

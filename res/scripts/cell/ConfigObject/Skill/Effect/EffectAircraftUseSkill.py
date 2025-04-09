# -*- coding: utf-8 -*-


"""
usage:
	效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine
import csconst



class EffectAircraftUseSkill( EffectSkillBase ):
	"""
	飞行器放技能
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



	def canEffect( self,skill, caster, receiver ):
		"""
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		return EffectSkillBase.canEffect(self,skill, caster, receiver)

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		receiver.allClients.AircraftUseSkill(receiver.id)
			




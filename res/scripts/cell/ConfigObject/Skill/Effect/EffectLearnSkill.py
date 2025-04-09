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

from KBEDebug import *

#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase




class EffectLearnSkill( EffectSkillBase ):
	"""
	学习技能
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
		
	def canEffect( self, skill, caster, receiver  ):
		"""
		效果添加检测
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		
		if self._skillID in receiver.attrSkills:
			return False
		
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		receiver.presentedSkill(self._skillID)




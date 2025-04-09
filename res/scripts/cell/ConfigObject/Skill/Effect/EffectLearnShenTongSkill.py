# -*- coding: utf-8 -*-

#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine

class EffectLearnShenTongSkill( EffectSkillBase ):
	"""
	神通技能学习
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._shentongSkillID = 0
		self._times = 0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._shentongSkillID = int( dictDat["Param1"] )
		self._times = int( dictDat["Param2"] )

	def canEffect( self, skill, caster, receiver  ):
		"""
		效果添加检测
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False	
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		EffectSkillBase.onReceive( self, skill, caster, receiver )
		receiver.learnShenTongSkill(self._shentongSkillID, self._times)
# -*- coding: utf-8 -*-

import math
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine
import KBEDebug


class EffectPassiveAbsorbHP( EffectSkillBase ):
	"""
	被动吸血效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._radio = 0.0
		self._value = 0

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )

		if dictDat["Param1"]:
			Param1 = dictDat["Param1"].split("|")
			self._radio = float( Param1[0] )
			if len(Param1) > 1:
				self._value = int( Param1[1] )

	def canEffect( self, skill, caster, receiver  ):
		"""
		效果添加检测
		"""
		if receiver.getState() == csdefine.ENTITY_STATE_DEAD:
			return False
		if not skill.isPassiveSkill():
			return False
		attackDamag = caster.queryTemp( "takeDamage", 0 )
		if attackDamag <= 0:
			KBEDebug.WARNING_MSG( "EffectPassiveAbsorbHP is failed!!!Because of has not attackDamag!!" )
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		attackDamag = caster.queryTemp( "takeDamage" )
		absorbHP = math.ceil(attackDamag * self._radio + self._value)
		absorbHP = max(0, absorbHP)
		receiver.addHP(absorbHP)

# -*- coding: utf-8 -*-

#python
import math
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine
import KBEDebug

class EffectReboundDamage( EffectSkillBase ):
	"""
	反弹伤害效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._deadEffect = 0					# 死亡时，是否播放特殊效果（暴尸）
		self._skillRadio = 0.0					# 技能效率
		self._skillValue = 0					# 技能固定值
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._deadEffect = int( dictDat["Param1"] )
		if dictDat["Param2"]:
			Param2 = dictDat["Param2"].split("|")
			self._skillRadio = float( Param2[0] )
			if len( Param2 ) > 1:
				self._skillValue = int( Param2[1] )


	def canEffect( self, skill, caster, receiver  ):
		"""
		效果添加检测
		"""
		if receiver.getState() == csdefine.ENTITY_STATE_DEAD:
			return False
		if not hasattr( skill, "isPassiveSkill") or not skill.isPassiveSkill():
			return False
		_reboundDamage = caster.queryTemp( "takeDamage", 0 )
		if _reboundDamage <= 0:
			KBEDebug.WARNING_MSG( "EffectReboundDamage is failed!!!Because of has not reboundDamage!!" )
			return False

		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		_damage = caster.queryTemp( "takeDamage" )
		finalDamage = math.ceil(_damage * self._skillRadio + self._skillValue)
		finalDamage = max(0, finalDamage)
		receiver.receiveDamage( caster.id, skill._id, csdefine.DAMAGE_TYPE_VOID, finalDamage, False, False, self._deadEffect, self._actForbid )
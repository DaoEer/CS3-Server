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
import math
#engine
import KBEngine
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import KBEDebug
import csdefine
from ItemSystemExp import g_CombatNormalDamager


class EffectHatred( EffectSkillBase ):
	"""
	仇恨改变效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._effectType = 0
		self._value = 0
		self._percent = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )

		if dictDat["Param1"]:
			self._effectType = int(dictDat["Param1"])

		# 伤害百分比（浮点型）|固定值（整型）
		if dictDat["Param2"]:
			Param2 = dictDat["Param2"].split("|")
			self._percent = float( Param2[0] )
			if len(Param2) > 1:
				self._value = int(Param2[1])

	def canEffect( self, skill, caster, receiver  ):
		"""
		效果添加检测
		"""
		if receiver.getState() == csdefine.ENTITY_STATE_DEAD:
			return False

		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		hatredValue = 0
		if self._effectType == 1:
			casterBaseCom = g_CombatNormalDamager.getBaseCombatData( caster.getLevel(), caster.getProfession() )
			hatredValue = math.ceil(casterBaseCom["BHatred"] * self._percent + self._value)
		elif self._effectType == 2:
			receiverBaseCom = g_CombatNormalDamager.getBaseCombatData( receiver.getLevel(), receiver.getProfession() )
			hatredValue = math.ceil(receiverBaseCom["BHatred"] * self._percent + self._value)
		receiver.addHatredList(caster.id, hatredValue)



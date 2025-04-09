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
import KBEDebug


class EffectRevive( EffectSkillBase ):
	"""
	原地复活效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._hpPercent = 0.0
		self._addHPValue = 0
		self._mpPercent = 0.0
		self._addMPValue = 0
	
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
			self._hpPercent = float(Param1[0])
			if len(Param1) > 1:
				self._addHPValue = int(Param1[1])

		if dictDat["Param2"]:
			Param2 = dictDat["Param2"].split("|")
			self._mpPercent = float(Param2[0])
			if len(Param2) > 1:
				self._addMPValue = int(Param2[1])

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if not hasattr( receiver, "reviveOnOrigin" ):
			return
		if receiver.isState( csdefine.ENTITY_STATE_DEAD ):
			receiver.reviveOnOrigin()
			receiver.setHP( max(int( receiver.HP_Max * self._hpPercent + self._addHPValue), 1) )
			receiver.setMP( max(int( receiver.MP_Max * self._mpPercent + self._addMPValue), 0) )



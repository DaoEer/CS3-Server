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
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine



class EffectAddPetMPSlot( EffectSkillBase ):
	"""
	幻兽蓝槽添加效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._addValue = 0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._addValue = int( dictDat["Param1"] )
	
	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if receiver.isState( csdefine.ENTITY_STATE_DEAD ):
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		value = self._addValue + receiver.petExtraMP
		receiver.setExtraMP( value )

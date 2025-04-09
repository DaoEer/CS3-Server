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



class EffectAddMP( EffectSkillBase ):
	"""
	加蓝效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._addValue = 0
		self._percent = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		
		# 治疗百分比（如“0.5”代表“50%MP上限治疗”）|固定值（整型）	
		if dictDat["Param1"]:
			Param1 = dictDat["Param1"].split("|")
			self._percent = float(Param1[0])
			if len(Param1) > 1:
				self._addValue = int(Param1[1])

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
		value = math.ceil( receiver.MP_Max * self._percent + self._addValue + receiver.MP )
		value = max(0, value)
		receiver.setMP( value )




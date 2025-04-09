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
import KBEDebug



class EffectEnergyChange( EffectSkillBase ):
	"""
	充能效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._buffID = 0
		self._addValue = 0
		self._percent = 0.0
		self._isBuffAgainTime = False
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._buffID = int(dictDat["Param1"])
		# 治疗百分比（如“0.5”代表“50%HP上限治疗”）|固定值（整型）
		if dictDat["Param2"]:
			Param2 = dictDat["Param2"].split("|")
			self._percent = float(Param2[0])
			if len(Param2) > 1:
				self._addValue = int(Param2[1])
				
		# 标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）		
		if dictDat["Param3"]:
			Param3 = dictDat["Param3"].split("|")
			for i in Param3:
				List = i.split(":")
				if List[0] == "IsBuffAgainTime":	# “IsSkipEvent”代表“需要跳过事件触发”
					self._isBuffAgainTime = True
				else:
					KBEDebug.ERROR_MSG("EffectEnergyChange: %s is not a correct tag name "%List[0])
	
	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		receiver.triggerSkillEvent( csdefine.SKILL_EVENT_ADD_ENERGY, caster.id, \
		{"EnergyBuffID":self._buffID, "addValue": self._addValue, "percent": self._percent,"IsBuffAgainTime":self._isBuffAgainTime} )




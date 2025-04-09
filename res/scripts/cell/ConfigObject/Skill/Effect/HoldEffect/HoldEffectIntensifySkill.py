# -*- coding: utf-8 -*-


"""
usage:
	Buff持有效果,onBegin 和 onEnd 必须成对存在，分别做buff添加和删除，增添的效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine


class HoldEffectIntensifySkill( HoldEffect ):
	"""
	持有效果：技能进阶
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._quickID = 0
		self._passiveSkillLevel = 0
		self._skillLevel = 0

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self._quickID = int(dictDat["Param1"])
		if dictDat["Param2"]:
			self._skillLevel = int(dictDat["Param2"])
		if dictDat["Param3"]:
			self._passiveSkillLevel = int(dictDat["Param3"])

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		if receiver.client:
			receiver.client.IntensifySkill( self._quickID, self._passiveSkillLevel, self._skillLevel )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		HoldEffect.onEnd( self, effectData, receiver )
		if receiver.client:
			receiver.client.CancelIntensifySkill( self._quickID, self._passiveSkillLevel, self._skillLevel )

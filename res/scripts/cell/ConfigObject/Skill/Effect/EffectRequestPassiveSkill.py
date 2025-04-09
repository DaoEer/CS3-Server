# -*- coding: utf-8 -*-

#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import KBEDebug
import csdefine

class EffectRequestPassiveSkill( EffectSkillBase ):
	"""
	触发一个被动技能申请
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._passiveSkillID = 0
		self._param = {}

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._passiveSkillID = int( dictDat["Param1"] )
		if dictDat["Param2"]:
			Param2 = dictDat["Param2"].split("|")
			for i in Param2:
				List = i.split(":")
				if List[0] == "IsReDict":				
					self._param[List[1]] = eval(List[2])
				else:
					KBEDebug.ERROR_MSG("EffectRequestPassiveSkill: %s is not a correct tag name "%List[0])

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		requestSkill = caster.getSkill(self._passiveSkillID)			
		requestSkill.requestPassiveSkill(caster, receiver.id, self._param)


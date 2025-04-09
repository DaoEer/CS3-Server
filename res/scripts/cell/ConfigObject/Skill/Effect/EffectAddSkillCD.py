# -*- coding: utf-8 -*-


from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import KBEDebug

class EffectAddSkillCD( EffectSkillBase ):
	"""
	添加技能CD
	"""
	def __init__(self):
		EffectSkillBase.__init__( self )
		self._coolDownDict = {}
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )

		time = float(dictDat["Param2"]) if dictDat["Param2"] and float(dictDat["Param2"]) > 0.0 else 0.0

		# 冷却类型列表（整型，|竖号分隔，不得缺省，多个代表“一起改变”）
		if dictDat["Param1"]:
			coolDownIdList = dictDat["Param1"].split("|")
			if len(coolDownIdList) != len(set(coolDownIdList)):
				KBEDebug.ERROR_MSG("Skill EffectAddSkillCD has duplicate configuration! SkillID=%s" % skill.getID())
			for coolDownID in coolDownIdList:
				self._coolDownDict[int(coolDownID)] = time
		else:
			KBEDebug.ERROR_MSG("Skill EffectAddSkillCD config is none! SkillID=%s" % skill.getID())
		

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if len(self._coolDownDict):
			receiver.setCooldown( self._coolDownDict )
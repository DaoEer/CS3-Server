# -*- coding: utf-8 -*-


from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import KBEDebug

class EffectChangeSkillCD( EffectSkillBase ):
	"""
	增/减技能CD
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._cooldownIdList = []
		self._time = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )


		if dictDat["Param1"]:
			coolDownIdList = dictDat["Param1"].split("|")
			if len(coolDownIdList) != len(set(coolDownIdList)):
				KBEDebug.ERROR_MSG("Skill EffectChangeSkillCD has duplicate configuration! SkillID=%s" % skill.getID())
			for coolDownID in coolDownIdList:
				self._cooldownIdList.append(int(coolDownID))
		else:
			KBEDebug.ERROR_MSG("Skill EffectChangeSkillCD config is none! SkillID=%s" % skill.getID())
		if dictDat["Param2"]:
			self._time = float(dictDat["Param2"])

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		for coolDownID in self._cooldownIdList:
			receiver.changeCooldown({coolDownID: self._time})





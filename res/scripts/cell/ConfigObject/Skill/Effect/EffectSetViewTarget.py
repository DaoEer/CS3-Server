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



class EffectSetViewTarget( EffectSkillBase ):
	"""
	镜头转向
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.durationTimeStr = "0 0 0"
		self.range = 0.0
		self.startViewRotatorStr = "0 0 0"
		self.targetViewRotatorStr = "0 0 0"
		self.bIsResetPlayerCamera = 1
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.durationTimeStr = dictDat["Param1"]
		self.startViewRotatorStr = dictDat["Param2"]
		self.targetViewRotatorStr = dictDat["Param3"]
		if dictDat["Param4"]:
			self.range = float(dictDat["Param4"])
		if dictDat["Param5"]:
			self.bIsResetPlayerCamera = int(dictDat["Param5"])

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.getClient():
			receiver.client.OnSetViewTarget(  caster.id, self.durationTimeStr, self.range, self.startViewRotatorStr, self.targetViewRotatorStr, self.bIsResetPlayerCamera)




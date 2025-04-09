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

import KBEngine
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase

class EffectCompleteTask( EffectSkillBase ):
	"""
	完成某任务目标
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.questID = 0
		self.taskIDs = []
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.questID = int(dictDat["Param1"])
		self.taskIDs = [int(i) for i in dictDat["Param2"].split("|")]

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		for taskID in self.taskIDs:
			caster.forceQuestTaskIncreaseState( self.questID, taskID )

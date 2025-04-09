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
import Math
import csdefine


class EffectUseSkillByQuestID( EffectSkillBase ):
	"""
	玩家通过任务ID选择技能
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.questIDs = []
		self.skillIDs = []


	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.questIDs = dictDat["Param1"].strip().split("|")
		self.skillIDs = dictDat["Param2"].strip().split("|")

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		for i,questID in enumerate(self.questIDs):
			if receiver.hasQuest( int(questID) ):
				if len(self.skillIDs)<i:
					return
				receiver.useSkillToEntity( int(self.skillIDs[i]),receiver.id )
				return	


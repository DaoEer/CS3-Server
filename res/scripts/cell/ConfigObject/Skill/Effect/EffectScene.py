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


class EffectScene( EffectSkillBase ):
	"""
	镜头效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._sceneID = ""
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._sceneID = dictDat["Param1"]

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.__class__.__name__ == "Role":
			receiver.client.StartPlayStory( self._sceneID, 1 )



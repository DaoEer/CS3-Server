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
#common
import csdefine
import Math



class EffectCreateFaZhen( EffectSkillBase ):
	"""
	创建法阵
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.scriptID = dictDat["Param1"]

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		pos = caster.position
		if not caster.isInTeam():
			return
		posList = KBEngine.collideVertical(caster.spaceID, caster.layer, caster.position, 10, -10)
		if len(posList):
			pos = posList[0]

		caster.createSpellBox(self.scriptID, tuple(Math.Vector3(pos)), (0.0, 0.0, 0.0), {"teamID":caster.teamMailbox.id})



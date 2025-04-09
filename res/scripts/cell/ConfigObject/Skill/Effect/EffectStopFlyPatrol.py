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


class EffectStopFlyPatrol( EffectSkillBase ):
	"""
	停止飞行传送效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._flyPatrolID = ""

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._flyPatrolID = dictDat["Param1"]

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE: return

		receiver.allClients.CLIENT_StopFlyPatrol(self._flyPatrolID)


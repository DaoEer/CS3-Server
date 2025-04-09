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


class EffectFlyTeleport( EffectSkillBase ):
	"""
	飞行传送
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._flyPatrolID = ""
		self._model = ""
		self._FlyModleId = ""

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._flyPatrolID = dictDat["Param1"]
		self._model = dictDat["Param2"]
		self._FlyModleId = dictDat["Param3"]

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE: return
		receiver.withdrawPetByReason( csdefine.PET_WITHDRAW_FLYTELEPORT )
		receiver.allClients.FlyPatrol( self._flyPatrolID, self._model, self._FlyModleId )


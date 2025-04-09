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
import csdefine


class EffectTeleportAppointSpace( EffectSkillBase ):
	"""
	神行石进行传送时用
	玩家传送至指定地图
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE: return
		receiver.teleportToNPCPos()

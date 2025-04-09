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

import math
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine
import csconst
import csstatus

class EffectPetReviveMP( EffectSkillBase ):
	"""
	幻兽蓝槽中的蓝量补充给幻兽蓝条规则效果
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
	
	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if receiver.isState( csdefine.ENTITY_STATE_DEAD ):
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		owner = receiver.getOwnerEntity()
		if owner is None:return

		percentMP = int(math.floor(receiver.MP/receiver.MP_Max*100))
		if percentMP >= owner.percentMP:
			receiver.removeBuffByID( csconst.PET_USE_BLUE_CHANNEL_BUFF )
			return

		if owner.petExtraMP == 0:
			if not receiver.hintOver:
				owner.statusMessage( csstatus.PET_HPSLOT_AND_MPSLOT_IS_NONE )
				receiver.hintOver = True
			receiver.removeBuffByID( csconst.PET_USE_BLUE_CHANNEL_BUFF )
			return

		value = receiver.MP_Max - receiver.MP
		if owner.petExtraMP > value:
			receiver.setMP( value + receiver.MP )
			owner.setExtraMP( owner.petExtraMP - value )
		else:
			receiver.setMP( owner.petExtraMP + receiver.MP )
			owner.setExtraMP( 0 )
		receiver.hintOver = False
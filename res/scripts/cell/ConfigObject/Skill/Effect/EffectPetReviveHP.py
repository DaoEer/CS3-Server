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
import KBEDebug


class EffectPetReviveHP( EffectSkillBase ):
	"""
	幻兽血槽中的血量补充给幻兽血条规则效果
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

		percentHP = int(math.floor(receiver.HP/receiver.HP_Max*100))
		if percentHP >= owner.percentHP:
			receiver.removeBuffByID( csconst.PET_USE_BLOOD_SLOT_BUFF )
			return

		if owner.petExtraHP == 0:
			if not receiver.hintOver:
				owner.statusMessage( csstatus.PET_HPSLOT_AND_MPSLOT_IS_NONE )
				receiver.hintOver = True
			receiver.removeBuffByID( csconst.PET_USE_BLOOD_SLOT_BUFF )
			return

		value = receiver.HP_Max - receiver.HP
		if owner.petExtraHP > value:
			receiver.setHP( value + receiver.HP )
			owner.setExtraHP( owner.petExtraHP - value )
		else:
			receiver.setHP( owner.petExtraHP + receiver.HP )
			owner.setExtraHP( 0 )
		receiver.hintOver = False
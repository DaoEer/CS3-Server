# -*- coding: utf-8 -*-


"""

"""


#cell
import ConfigObject.Skill.SkillBase.CombatSkill as CombatSkill
#common
import csdefine
import KBEDebug

import csstatus

class SkillFillFloor( CombatSkill.CombatSkill ):
	"""
	环任务【仙岛归墟】 填充格子技能
	"""
	def __init__( self ):
		CombatSkill.CombatSkill.__init__( self )
			
	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		if not caster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			return csstatus.SKILL_CAST_FAILED

		spaceEntity = caster.getCurrentSpace()
		if not spaceEntity:
			return csstatus.SKILL_CAST_FAILED

		floorID = spaceEntity.getFillFloorID( target.getObject() )
		if spaceEntity.isInFloorIDList( floorID ):
			return csstatus.SKILL_CAST_FAILED

		return CombatSkill.CombatSkill.useableCheck( self, caster, target )

	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		if castResult:
			spaceEntity = caster.getCurrentSpace()
			if not spaceEntity:
				return
			floorID = spaceEntity.getFillFloorID( target.getObject() )
			spaceEntity.addFloorID(floorID)			
		CombatSkill.CombatSkill.onSkillEnd( self, caster, target, castResult )
# -*- coding: utf-8 -*-


"""

"""


#cell
import ConfigObject.Skill.SkillBase.CombatSkill as CombatSkill
#common
import csdefine
import KBEDebug

import csstatus

class SkillMountOnPet( CombatSkill.CombatSkill ):
	"""
	玩家 上马表现
	"""
	def __init__( self ):
		CombatSkill.CombatSkill.__init__( self )
		self._forbidActTime = 0.0							# 禁止操作时间
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		CombatSkill.CombatSkill.init( self, dictDat )
		if dictDat["Param1"]:
			self._forbidActTime = float( dictDat["Param1"])
			
	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		if not caster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			return csstatus.SKILL_CAST_FAILED
		return CombatSkill.CombatSkill.useableCheck( self, caster, target )

	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		"""
		CombatSkill.CombatSkill.onSkillBegin( self, caster, target )
		pet = caster.getActivePetCell()
		if pet:
			pet.moveToPosition( caster.getRightPos() )
		if self._forbidActTime:
			caster.mountPetTimerID = caster.addTimerCallBack( self._forbidActTime, "onSkillBeginMountPet", () )
		
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""			
		CombatSkill.CombatSkill.onSkillEnd( self, caster, target, castResult )
		if castResult:
			caster.onMountPet()
		if self._forbidActTime:
			caster.onSkillEndMountPet()
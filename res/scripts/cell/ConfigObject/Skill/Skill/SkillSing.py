# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine
import Settings
import SkillTargetObjImpl
from ConfigObject.Skill.SkillBase.CombatSkill import CombatSkill


class SkillSing( CombatSkill ):
	"""
	吟唱技能
	"""

	def __init__( self ):
		CombatSkill.__init__( self )


	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		CombatSkill.init( self, dictDat )
		self._endHitSkill = int( dictDat["Param1"] )

	def useSkill( self, caster, target ):
		"""
		"""
		if not self.skillDefineCheck(caster, target):  #CST-4084/CST-2113
			return csstatus.SKILL_CAST_FAILED
		# 将吟唱技能的目标传递给触发子技能
		self.setSkillSingTarget(caster, target)
		# 当配置里的技能目标类型和传过来的技能目标类型不符时
		target = self.adaptiveTarget(caster, target)
		if not target:
			return csstatus.SKILL_CAST_FAILED

		state = self.useableCheck( caster, target )
		if state != csstatus.SKILL_GO_ON:
			return state

		space = caster.getCurrentSpace()
		if space:
			if len(space.getScript().getAllowUseSkillIDs()) and self._id not in space.getScript().getAllowUseSkillIDs():
				return csstatus.SKILL_SPACE_FORBID
			if len(space.getScript().getForbidUseSkillIDs()) and self._id in space.getScript().getForbidUseSkillIDs():
				return csstatus.SKILL_SPACE_FORBID

		caster.beforeUseSkill( self, target )
		self.use( caster, target )
		return csstatus.SKILL_GO_ON

	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		CombatSkill.onSkillEnd( self, caster, target, castResult )
		if not castResult:
			return

		target = self.getSkillSingTarget(caster)
		self.removeSkillSingTarget(caster)
		statusID = self.continueCastSkill(caster, target)
		if statusID != csstatus.SKILL_GO_ON and caster.isEntityFlag(csdefine.ENTITY_FLAG_ROLE):
			caster.statusMessage( statusID)	
		
	def continueCastSkill(self, caster, target):
		"""
		继续施放技能
		"""	
		if not target:
			return csstatus.SKILL_CAST_FAILED
		skill = caster.getSkill( self._endHitSkill )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( caster.id, self._endHitSkill ) )
			return csstatus.SKILL_NOT_EXIST

		return skill.useSkill(caster, target)

	def setSkillSingTarget(self, caster, target):
		"""
		设置技能申请目标
		"""
		targetList = caster.queryTemp("SkillSingTarget", {})
		targetList[self._endHitSkill] = target
		caster.setTemp("SkillSingTarget", targetList)

	def getSkillSingTarget(self, caster):
		"""
		获得技能申请目标
		"""
		targetList = caster.queryTemp("SkillSingTarget", {})
		if not targetList:
			return None
		return targetList[self._endHitSkill]

	def removeSkillSingTarget(self, caster):
		"""
		移除技能申请目标
		"""
		targetList = caster.queryTemp("SkillSingTarget", {})
		targetList.pop(self.getID(), None)
		if not targetList:
			caster.removeTemp("SkillSingTarget")
			return
		caster.setTemp("SkillSingTarget", targetList)
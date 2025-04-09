# -*- coding: utf-8 -*-

import Math
import csdefine
import csstatus
from ConfigObject.Skill.SkillBase.CombatSkill import CombatSkill



class SkillJump( CombatSkill ):
	"""
	跳扑技能
	"""
	def __init__( self ):
		CombatSkill.__init__( self )
		self.delayTime = 0.0
		self.moveTime = 0.0

	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		CombatSkill.init( self, dictDat )
		if dictDat["Param1"]:
			self.delayTime = float( dictDat["Param1"] )
		if dictDat["Param2"]:
			self.moveTime = float( dictDat["Param2"] )
	
	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		if caster.__class__.__name__ == "Role":
			return csstatus.SKILL_CAST_FAILED
		return CombatSkill.useableCheck( self, caster, target )
	
	def cast( self, caster, target ):
		"""
		施放技能
		"""
		CombatSkill.cast( self, caster, target )
		targetPos = target.getObjectPosition()
		direction = targetPos - caster.position
		direction.normalise()
		dist = caster.position.distTo( targetPos )
		if self.moveTime > 0.0:
			moveSpeed = dist / self.moveTime
		else:
			moveSpeed = 0.0
			dest = Math.Vector3(0,0,0)
		dstPos = caster.position + direction * dist
		
		if self.delayTime:
			caster.addTimerCallBack( self.delayTime, "skillJumpPosition", (Math.Vector3(dstPos), moveSpeed, 0.1))
		else:
			caster.skillJumpPosition( Math.Vector3(dstPos), moveSpeed, 0.1)
	
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		CombatSkill.onSkillEnd( self, caster, target, castResult )
		caster.stopMoving( csdefine.MOVE_TYPE_SKILL_JUMP )

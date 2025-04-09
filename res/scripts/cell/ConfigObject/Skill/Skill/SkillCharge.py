# -*- coding: utf-8 -*-

import Math
import math
import csdefine
import csstatus
import KBEDebug
import KBEngine
import csarithmetic
import KBEMath
from ConfigObject.Skill.SkillBase.CombatSkill import CombatSkill


class SkillCharge( CombatSkill ):
	"""
	怪物冲锋技能
	"""
	def __init__( self ):
		CombatSkill.__init__( self )
		self.casterMoveSpeed    = 0.0	#冲刺速度
		self.casterMoveDistance = 0.0	#冲刺距离

	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		CombatSkill.init( self, dictDat )
		if dictDat["Param1"]:
			self.casterMoveSpeed = max(0, float( dictDat["Param1"] ))
		if dictDat["Param2"]:
			self.casterMoveDistance = max(0, float( dictDat["Param2"] ))

	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		return CombatSkill.useableCheck( self, caster, target )

	def cast( self, caster, target ):
		"""
		施放技能
		"""	
		targetPos = target.getObjectPosition()
		v = targetPos - caster.position
		z = csarithmetic.getYawByVector3(v)
		if self.casterMoveSpeed > 0:
			if self.getTargetType() != csdefine.SKILL_CAST_OBJECT_TYPE_NONE:
				if targetPos.flatDistTo(caster.position)>0.1:
					direction = (0.0, 0.0, z)
					caster.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
			yaw = caster.direction.z

			dstPos = Math.Vector3(caster.position.x + self.casterMoveDistance*math.sin(yaw), caster.position.y+ v.y*self.casterMoveDistance, caster.position.z + self.casterMoveDistance * math.cos(yaw))
			#dstPos = caster.position + v*self.casterMoveDistance
			raycastList = caster.navmeshRaycast( caster.position, dstPos )
			if raycastList:
				dstPos = raycastList[0]

			if caster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
				CPosition = KBEMath.KBEngine2UnrealPosition(dstPos)
				caster.client.CLIENT_RoleChargePosition(CPosition, self.casterMoveSpeed)
			else:
				caster.chargeToPosition( dstPos, self.casterMoveSpeed, 0.1 )
		CombatSkill.cast( self, caster, target )	
	
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		CombatSkill.onSkillEnd( self, caster, target, castResult )
		caster.stopMoving(csdefine.MOVE_TYPE_CHARGE)
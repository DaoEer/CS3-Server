# -*- coding: utf-8 -*-


import csdefine
import csstatus
import KBEDebug
import KBEngine
import Math
from ConfigObject.Skill.SkillBase.CombatSkill import CombatSkill

class SkillChase( CombatSkill ):
	"""
	跟随并打击技能
	"""
	def __init__( self ):
		CombatSkill.__init__( self )
		self.chaseSpeed = 0.0	#跟随速度
		self.chaseMinDis = 0.0	#保持距离
		self.endHitSkill = 0	#打击技能（跟随结束怼一下）

	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		CombatSkill.init( self, dictDat )
		if dictDat["Param1"]:
			self.chaseSpeed = max(0.0, float( dictDat["Param1"] ))
		if dictDat["Param2"]:
			self.chaseMinDis = max(0.0, float( dictDat["Param2"] ))
		if dictDat["Param3"]:
			self.endHitSkill = int( dictDat["Param3"] )
	
	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		return CombatSkill.useableCheck( self, caster, target )
	
	def cast( self, caster, target ):
		"""
		施放技能
		"""
		if caster.position.distTo( target.getObject().position ) <= self.chaseMinDis + 0.1:		#因为大于但非常接近“保持距离”的情况下，底层追踪接口会调用失败，所以这里加个0.1，避免卡住。
			caster.interruptSkill( csstatus.SKILL_CAST_FAILED )
			self.useEndHitSkill( caster, target.getObject() )
		else:
			if target.getObject():
				if caster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
					caster.client.CLIENT_RoleChaseEntity(self.getID(), target.getObject().id, self.chaseMinDis, self.chaseSpeed)
				else:
					caster.skillChaseEntity( target.getObject(), self.chaseMinDis, self.chaseSpeed, self )
		CombatSkill.cast( self, caster, target )
	
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		CombatSkill.onSkillEnd( self, caster, target, castResult )
		caster.stopMoving( csdefine.MOVE_TYPE_SKILL_CHASE )
		if not caster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			caster.changeDefaultMove()
		else:
			caster.client.CLIENT_RoleChaseEntityEnd()
	
	def onSkillChaseOver( self, caster, isSuccess ):
		"""
		"""
		targetEntityID = caster.receiverID					#保存一下，因为打断技能后会清除此数据
		caster.interruptSkill( csstatus.SKILL_CAST_FAILED )
		if isSuccess:
			targetEntity = KBEngine.entities.get( targetEntityID )
			if targetEntity:
				self.useEndHitSkill( caster, targetEntity )	#跟随成功则使用打击技能
	
	def useEndHitSkill( self, caster, targetEntity ):
		"""
		"""
		if not self.endHitSkill:
			return
		caster.useSkillToEntity( self.endHitSkill, targetEntity.id )
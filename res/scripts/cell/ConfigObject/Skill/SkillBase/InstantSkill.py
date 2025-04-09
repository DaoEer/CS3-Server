# -*- coding: utf-8 -*-


"""
usage:
	战斗技能类

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
import ConfigObject.Skill.SkillBase.Skill as Skill
#common
import csdefine
import csstatus
import KBEDebug


class InstantSkill( Skill.Skill ):
	"""
	瞬发技能
	"""
	def __init__( self ):
		Skill.Skill.__init__( self )
		self._isInstantSkill = True

	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		Skill.Skill.init( self, dictDat )	

	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		#观察者标志位禁止施法
		if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			if caster.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
				return csstatus.SKILL_STATE_CANT_CAST

		if self._actForbid != csdefine.ACTION_FORBID_NONE: #解决某些如果只需要释放技能，而没有state属性的问题
			#是否有禁止标记
			if caster.actionForbidSign( self._actForbid ):
				return csstatus.SKILL_STATE_CANT_CAST

		#是异常抵抗
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			if self.checkExceptionResist( target.getObject() ):
				return csstatus.SKILL_STATE_CANT_CAST

		if self._targetActForbid != csdefine.ACTION_FORBID_NONE: #解决某些如果只需要释放技能，而没有state属性的问题
			#技能目标是否有禁止标记
			if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
				if target.getObject().actionForbidSign( self._targetActForbid ):
					return csstatus.SKILL_TARGET_STATE_CANT_CAST

		#检查技能cooldown
		if self.isCasterCooldown( caster ):
			return csstatus.SKILL_NOT_READY

		#目标检查技能cooldown
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			if self.isTargetCooldown( target ):
				return csstatus.SKILL_TARGET_NOT_READY

		#施法需求检查
		state = self.checkCasterRequire( caster )
		if state != csstatus.SKILL_GO_ON:
			return state

		#目标需求检查
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			state = self.checkTargetRequire( target )
			if state != csstatus.SKILL_GO_ON:
				return state

		#施法者检查
		state = self.castValidCheck( caster, caster )
		if state != csstatus.SKILL_GO_ON:
			return state

		#检查目标是否符合法术施展
		state = self.getCastObject().valid( caster, target )
		if state != csstatus.SKILL_GO_ON:
			return state
		
		#施法目标检查
		state = self.targetValidCheck( caster, target )
		if state != csstatus.SKILL_GO_ON:
			return state

		return csstatus.SKILL_GO_ON

	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		不需要改碰撞类型
		"""
		caster.onSkillBegin( self, target )
		target.onSkillBegin( caster )
		caster.isInterruptInstantSkill[self._id] = 0
		isHit = 1

		self.addHoldEffect( caster )			# 添加持有效果

		caster.triggerEventSkillBegin( self )	# 触发施法者“施展开始时”

		if caster.isInterruptInstantSkill.get(self._id, 0):		# 技能中断响应
			caster.interruptInstantSkill( self._id, csstatus.SKILL_CAST_FAILED )
			isHit = 0
		caster.isInterruptInstantSkill[self._id] = 1

		if isHit: 								#开始打击
			self._hitData.begin( self, caster, target )

	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		Skill.Skill.onSkillEnd( self, caster, target, castResult )	
		caster.isInterruptInstantSkill.pop(self._id, 0)	

	def triggerSkillEvent( self, caster, eventType, triggerID, pDict ):
		"""
		virtual method
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_ACT_WORD_CHANGE:
			if pDict.get( "actWord", 0 ) == self._actForbid:
				if caster.isInterruptInstantSkill.get(self._id, 0):
					caster.interruptInstantSkill( self._id, csstatus.SKILL_CAST_FAILED )
				else:
					caster.isInterruptInstantSkill[self._id] = 1
		
		if self._interruptEvent.canTriggerEvent( eventType, pDict ):
			caster.interruptInstantSkill( self._id, csstatus.SKILL_CAST_FAILED )

	def triggerReceiverSkillEvent( self, caster, receiver, eventType, triggerID, pDict ):
		"""
		virtual method
		触发受术目标事件
		"""	
		pass
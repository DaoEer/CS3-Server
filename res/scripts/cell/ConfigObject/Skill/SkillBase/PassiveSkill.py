# -*- coding: utf-8 -*-


"""
usage:
	被动技能类
	1、只有技能流程事件（包括自定义事件），才能触发被动技能
	2、被动技能不会触发技能流程事件

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
import ConfigObject.Skill.SkillBase.Skill as Skill
import ConfigObject.Skill.SkillBase.ObjectCondition as ObjectCondition
import ConfigObject.Skill.SkillBase.RequireDefine as RequireDefine
import ConfigObject.Skill.SkillBase.ObjectDefine as ObjectDefine
import ConfigObject.Skill.SkillBase.HitDefine as HitDefine
import ConfigObject.Skill.EffectLoader as EffectLoader
import ConfigObject.Skill.SkillBase.EventDefine as EventDefine
#common
import csdefine
import csstatus
import KBEDebug
import KBEngine
import Settings
#user_type
import SkillTargetObjImpl
#data
import Skill.SkillReceiverDefine as SkillReceiverDefine
import Skill.SkillCasterDefine as SkillCasterDefine


class PassiveSkill( Skill.Skill ):
	"""
	"""
	def __init__( self ):
		self._id 				= 0
		self._name 					= ""
		self._castRangeMax 		= 0.0
		self._actForbid 		= csdefine.ACTION_FORBID_NONE
		self._targetActForbid 	= csdefine.ACTION_FORBID_NONE
		self._targetType 		= csdefine.SKILL_CAST_OBJECT_TYPE_NONE
		self._casterCondition 	= ObjectCondition.ObjectCondition()
		self._targetCondition 	= ObjectCondition.ObjectCondition()
		self._casterCoolDown	= {}
		self._targetCoolDown	= {}
		self._casterRequire 	= RequireDefine.newInstance( None )
		self._targetRequire 	= RequireDefine.newInstance( None )
		self._hitData 			= HitDefine.PassiveSkillHitData()
		self._triggerEvent 		= EventDefine.EventDefine()
		self._collisionType 	= csdefine.COLLISION_DEFAULT
		self._quality			= 0
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		self._isPassiveSkill = True													# 是否被动技能
		self._isInstantSkill = True													# 是否瞬发技能
		self._id = int( dictDat["Name"] )
		self._name = dictDat["SkillName"]											# 技能名称
		self._quality = dictDat["Quality"]
		self._targetType = dictDat[ "TargetType" ]									# 施法目标类型
		
		for cdata in dictDat["CasterCoolDown"]:											# 技能冷却
			self._casterCoolDown[ cdata["CooldownId"] ] = cdata["CoolDownTime"]

		for cdata in dictDat["TargetCoolDown"]:											# 技能冷却
			self._targetCoolDown[ cdata["CooldownId"] ] = cdata["CoolDownTime"]
		
		if len( dictDat[ "CasterRequireDefine" ] ) > 0: #list
			self._casterRequire = RequireDefine.newInstance( dictDat[ "CasterRequireDefine" ] )		# 施放消耗
		if len( dictDat[ "TargetRequireDefine" ] ) > 0: #list
			self._targetRequire = RequireDefine.newInstance( dictDat[ "TargetRequireDefine" ] )		# 施放消耗
		if len( dictDat[ "CasterCondition" ] ) > 0: #dict							# 施法者条件
			self._casterCondition.init( dictDat["CasterCondition"] )
		if len( dictDat[ "TargetCondition" ] ) > 0: #dict							# 施法目标条件
			self._targetCondition.init( dictDat["TargetCondition"] )
		
		self._actForbid = \
		getattr( csdefine, dictDat["CasterActForbid"], csdefine.ACTION_FORBID_NONE )		# 玩法类型限制（不放到objectCondition,因为它还有中断技能作用）

		self._targetActForbid = \
		getattr( csdefine, dictDat["TargetActForbid"], csdefine.ACTION_FORBID_NONE )		# 玩法类型限制（不放到objectCondition,因为它还有中断技能作用）
		
		self._castObject = ObjectDefine.newInstance( self._targetType, self )
		self._castObject.init( dictDat )
		
		self._hitData.init( dictDat["HitList"], self )
		
		self._triggerEvent.init( dictDat["TriggerSkillEvent"] )						# 触发被动技能事件
		
	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		#是否有禁止标记
		if caster.actionForbidSign( self._actForbid ):
			return csstatus.SKILL_STATE_CANT_CAST

		#技能目标是否有禁止标记
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			if target.getObject().actionForbidSign( self._targetActForbid ):
				return csstatus.SKILL_TARGET_STATE_CANT_CAS
			
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
		
	def attachToCaster( self, caster ):
		"""
		"""
		self._triggerEvent.registerEvent( self, caster )
		
	def detachToCaster( self, caster ):
		"""
		"""
		self._triggerEvent.unRegisterEvent( self, caster )
		
	def registerSkillEvent( self, caster, target ):
		"""注册技能事件"""
		pass
	
	def unRegisterSkillEvent( self, caster, target ):
		"""取消技能事件"""
		pass
		
	def triggerSkillEvent( self, caster, eventType, triggerID, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if self._triggerEvent.canTriggerEvent( eventType, pDict ):
			self.requestPassiveSkill(caster, triggerID, pDict)

	def requestPassiveSkill( self, caster, targetID, pDict):
		"""
		申请施法被动技能
		"""
		if self._targetType == csdefine.SKILL_CAST_OBJECT_TYPE_NONE:
			target = caster
		elif self._targetType == csdefine.SKILL_CAST_OBJECT_TYPE_ENTITY:
			target = KBEngine.entities.get( targetID )
		
		if not target or target.inDestroying():
			KBEDebug.WARNING_MSG( "%s(%s) skill target is destroying or destroyed. targetID:%s" %( self.getName(), self.id, targetID ) )
			return csstatus.SKILL_UNKNOWN
		
		if target.spaceID != caster.spaceID:
			KBEDebug.WARNING_MSG( "%s(%s): skill target %s spaceID error." % ( self.getName(), self.id, targetID ) )
			return csstatus.SKILL_UNKNOWN
		if not self.skillDefineCheck(caster, target):
			return csstatus.SKILL_CAST_FAILED			

		caster.setTemp("takeDamage", pDict.get("takeDamage", 0))		
		self.useSkill( caster, SkillTargetObjImpl.createTargetObjEntity( target ) )		
	
	def useSkill( self, caster, target ):
		"""
		"""
		state = self.useableCheck( caster, target )
		if state != csstatus.SKILL_GO_ON:
			return state
		
		self.use( caster, target )
		return csstatus.SKILL_GO_ON
		
	def use( self, caster, target ):
		"""
		"""
		# 设置技能冷却时间
		if len(self._casterCoolDown):
			caster.setCooldown( self._casterCoolDown )

		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			if len(self._targetCoolDown):
				target.getObject().setCooldown( self._targetCoolDown )
		# 处理消耗
		self.doCasterRequire( caster )
		self.cast( caster, target )

	def cast( self, caster, target ):
		"""
		施放技能
		"""
		self.onSkillBegin( caster, target )
		
	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		"""
		caster.onSkillBegin( self, target )
		
		#开始打击
		self._hitData.onHit( self, caster, target )
		
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		caster.removeTemp("takeDamage")
		caster.onSkillEnd( self, castResult )
		
	def skillDefineCheck(self, caster, target):
		"""
		受术者/施法者 可战斗单位要求
		"""
		skillName = self.__class__.__name__
		if skillName in SkillReceiverDefine.Datas:
			flag = target.getEntityFlag()
			if flag in SkillReceiverDefine.Datas[skillName]:
				if not SkillReceiverDefine.Datas[skillName][flag]:
					KBEDebug.WARNING_MSG( "receiver(type:%d) in skill skillName(%s) is limit(SkillReceiverDefine)!!"%(flag,skillName) )
				return SkillReceiverDefine.Datas[skillName][flag]

		if skillName in SkillCasterDefine.Datas:
			_flag = caster.getEntityFlag()
			if _flag in SkillCasterDefine.Datas[skillName]:
				if not SkillCasterDefine.Datas[skillName][_flag]:
					KBEDebug.WARNING_MSG( "caster(type:%d) in skill skillName(%s) is limit(SkillCasterDefine)!!"%(_flag,skillName) )
				return SkillReceiverDefine.Datas[skillName][flag]
		return True
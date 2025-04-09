# -*- coding: utf-8 -*-


#engine
import KBEngine

import Math
import time
import random
#cell
import Define
import FightRuleMgr
from CoreInterface import CombatInterface
from CoreInterface import MonsterAIInterface
from CoreInterface import MonsterOwnerInterface
from StateInterface.MonsterStateInterface import MonsterStateInterface
import CoreInterface.GangQiInterface as GangQiInterface
#common
import csdefine
import csconst
import csstatus
import QuestEventDefine
import KBEDebug
from ConfigObject.Drop.DropBase import DropMgr
import ItemSystemExp
import math
import ItemTypeEnum
import Const

AI_START_TIME_VALUE = 2.0

class MonsterCombatInterface(
		MonsterStateInterface,
		CombatInterface.CombatInterface,
		MonsterAIInterface.MonsterAIInterface,
		MonsterOwnerInterface.MonsterOwnerInterface,
	):
	def __init__( self ):
		MonsterStateInterface.__init__(self)
		MonsterAIInterface.MonsterAIInterface.__init__(self)
		CombatInterface.CombatInterface.__init__( self )
		MonsterOwnerInterface.MonsterOwnerInterface.__init__( self )
		self.updateBornHPMP()
		self._isPlayDeadEffect = False # 是否播放死亡特效
		if self.hasFlag(csdefine.FLAG_AI_TICK):			#拥有此标志位表示不在玩家AOI范围内也需要开始执行AI
			self.addTimerCallBack( AI_START_TIME_VALUE, "monsterAIStart", () )
		

	def updateBornHPMP(self):
		"""
		怪物出生满血
		"""
		self.setHP( self.HP_Max )
		self.setMP( self.MP_Max )

	def beforeDestroy( self ):
		"""
		销毁前做一些事
		"""
		self.triggerEvent(csdefine.ENTITY_EVENT_DESTORY_SELF,"")
		CombatInterface.CombatInterface.beforeDestroy( self )
		self.resetEnemyList()
	
	#---------------战斗相关----------------------------------
	def receiveDamage( self, casterID, skillID, damageType, damage, isCritical, isParry, deadEffect, actForbid ):
		"""
		"""
		caster = KBEngine.entities.get( casterID )

		if self.isState( csdefine.ENTITY_STATE_DEAD ) or self.isState( csdefine.ENTITY_STATE_PEAD ) \
			or self.isState( csdefine.ENTITY_STATE_RESET ):
			return

		if deadEffect:
			self.setPlayDeadEffect(True)

		if caster:
			self.addDamageList( caster.id, damage )

		# 如果伤害大于0
		if damage > 0 and casterID != self.id:
			self.setBootyOwner(caster)
	
			if not self.firstBruise:
				if self.queryRelation( caster ) == csdefine.COMBAT_RELATION_ENEMY:
					self.firstBruise = True
					# 进入战斗状态后第一个产生伤害目标将被作为所有者
					KBEDebug.DEBUG_MSG("The firstAttacker is ----->>>>> %s" % casterID )
					# 第一次受击事件
					self.onFirstBruise( caster, damage, skillID )
		
		if self.HP == 0 and self.getState() == csdefine.ENTITY_STATE_DEAD:
			return

		isUnyielding = 0
		if self.hasEffectState( csdefine.EFFECT_STATE_UNYIELDING ):
			if int(self.HP - damage ) <= 1:
				isUnyielding = 1

		oldHP = self.HP
		if self.minHPPercent > 0:
			if ( self.HP - damage ) / float( self.HP_Max )  * 100 <= self.minHPPercent:
				self.setHP( math.ceil(self.HP_Max * (self.minHPPercent / 100.0) ))
			else:
				self.setHP( int(self.HP - damage ))
		else:
			if isUnyielding:
				self.setHP(1)
			else:
				self.setHP( int(self.HP - damage ))
		
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			self.setMP( 0 )
			self.onBeKill( casterID, deadEffect, actForbid )
			
		self.setPlayDeadEffect(False)
		
		finalDamage = oldHP - self.HP
		self.onReceiveDamage( casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )
		self.autoAddHatred(casterID, damage)
	
	def onHPChanged( self, oldValue ):
		"""
		血量改变回调
		"""
		CombatInterface.CombatInterface.onHPChanged( self, oldValue )
		self.triggerEvent( csdefine.ENTITY_EVENT_HP_CHANGE,(self.HP, oldValue))
		self.getScript().onHPChanged( self, oldValue )

	def onFirstBruise( self, caster, damage, skillID ):
		"""
		第一次受击事件

		@param 		 caster: 对你产生伤害的人
		@type  		 caster: Entity
		@param       damage: 伤害
		@type        damage: int
		@param      skillID: 法术ID
		@type       skillID: INT
		@return:             无
		"""
		pass

	def addDamageList( self, entityID, damage ):
		"""
		添加伤害列表
		@param entityID  : entityID
		@param damage	 : 伤害值
		"""
		# 如果回走状态 则忽略任何敌人
		if self.isState( csdefine.ENTITY_STATE_RESET ):
			return
		CombatInterface.CombatInterface.addDamageList( self, entityID, damage )

	def autoAddHatred(self, entityID, damage):
		"""	
		自然增加仇恨
		"""
		target = KBEngine.entities.get(entityID)
		if not target:
			return
		if self.queryRelation( target ) != csdefine.COMBAT_RELATION_ENEMY:
			return
		BaseCom = ItemSystemExp.g_CombatNormalDamager.getBaseCombatData( self.getLevel(), self.getProfession() )
		value = damage * BaseCom["HatredRatio"] * target.hatred_correction / ItemTypeEnum.PRECENTRATIO
		value = max(BaseCom["HatredLL"], value)
		self.addHatredList(entityID, int(value))

	def autoAddRelatedHatred(self, entityID, value):
		"""	
		自然增加连带仇恨
		"""
		target = KBEngine.entities.get(entityID)
		if not target:
			return
		BaseCom = ItemSystemExp.g_CombatNormalDamager.getBaseCombatData( self.getLevel(), self.getProfession() )
		value = value * BaseCom["RelatedHatredRatio"] * target.related_hatred_correction / ItemTypeEnum.PRECENTRATIO
		value = max(BaseCom["RelatedHatredLL"], value)
		self.addHatredList(entityID, int(value))

	def addHatredList( self, entityID, value ):
		"""
		添加仇恨列表
		@param entityID  : entityID
		@param value	 : 仇恨值
		"""
		# 如果回走状态 则忽略任何敌人
		if self.isState( csdefine.ENTITY_STATE_RESET ):
			return
		CombatInterface.CombatInterface.addHatredList( self, entityID, value )

	def onAddEnemy( self, entityID ):
		"""
		"""
		CombatInterface.CombatInterface.onAddEnemy( self, entityID )
		self.getScript().onAddEnemy( self, entityID )

	def onRemoveEnemy( self, entityID ):
		"""
		"""
		if not len( self.enemyList ):
			self.setSpawnPosBySpawnRoute()
		CombatInterface.CombatInterface.onRemoveEnemy( self, entityID )
		MonsterOwnerInterface.MonsterOwnerInterface.onRemoveEnemy(self, entityID)
		self.getScript().onRemoveEnemy( self, entityID )

	def changeAttackTarget( self, newTargetID ):
		"""
		改变攻击目标
		@param newTargetID: 目标entityID
		@type  newTargetID: OBJECT_ID
		@return:            无
		"""
		if self.isState( csdefine.ENTITY_STATE_DEAD ) or self.isState( csdefine.ENTITY_STATE_PEAD ) or self.isState( csdefine.ENTITY_STATE_RESET ):
			return

		target = KBEngine.entities.get( newTargetID )
		if not target or target.spaceID != self.spaceID:
			self.onChangeTargetFailed( newTargetID )
			return
			
		if self.monsterAIGetTarget() == newTargetID:
			return

		if self.queryRelation( target ) != csdefine.COMBAT_RELATION_ENEMY:
			KBEDebug.DEBUG_MSG( "RelationError: self.className = %s" % ( self.className ) )

		if self.isMoving():
			self.stopMovingForType( csdefine.NORMAL_MOVE )
		
		oldEnemyID = self.monsterAIGetTarget()
		self.monsterAISetTarget( newTargetID )
		KBEDebug.DEBUG_MSG( "%i: oldEnemy = %i, targetID = %i, current state = %i" % (self.id, oldEnemyID, self.monsterAIGetTarget(), self.getState()) )

		if self.isState( csdefine.ENTITY_STATE_FREE ):
			self.changeState( csdefine.ENTITY_STATE_FIGHT )

		self.onChangeTarget( oldEnemyID )	# 回调，改变攻击目标

	def onChangeTargetFailed( self, newTargetID ):
		"""
		改变目标失败通知
		"""
		target = KBEngine.entities.get(newTargetID)
		if target:
			FightRuleMgr.g_fightMgr.breakEnemyRelation( self, target )

	def onChangeTarget( self, oldEnemyID ):
		"""
		告诉其它人，当前的攻击目标改变；可以被派生，但继承者必须先调用这个方法后再判断其它相关值才是正确的。
		这里有几种可能性：1.如果oldEnemyID为0即表示它之前没有攻击目标；2.如果self.monsterAISetTarget()为0即表示攻击目标丢失
		@param oldEnemyID: 旧的攻击目标
		@type  oldEnemyID: OBJECT_ID
		@return: 无
		"""
		KBEDebug.DEBUG_MSG( "--------Monster(%s) onChangeTarget from %s to %s" %( self.id, oldEnemyID, self.monsterAIGetTarget() ) )

	def doMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		self.behOver( csdefine.BEHAVIOUR_TYPE_MOVING )
		self.randomWalkTime = random.randint( 3, 10 )	# 随机走动；待在原地一段时间后继续走

	def doMoveFailure( self, controllerID, userData ):
		"""
		virtual method
		移动失败
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		self.behOver( csdefine.BEHAVIOUR_TYPE_MOVING )
		if self.isState( csdefine.ENTITY_STATE_RESET ):									# 如果走不过去则直接跳回
			self.position = Math.Vector3( self.getSpawnPos() )
			self.changeState( csdefine.ENTITY_STATE_FREE )
	
	def moveFailure( self, mScriptID, mArgs ):
		"""
		开启某个移动失败
		"""
		self.behOver( csdefine.BEHAVIOUR_TYPE_MOVING )
	
	def onViewRange( self ):
		"""
		视野范围
		清理已经不在视野内的所有敌人 只有在战斗状态时才进行检测
		return :None
		"""
		for id in list(self.enemyList):
			if not self.monsterAICheckInViewRange( id ):
				enemyEntity = KBEngine.entities.get( id, None )
				if enemyEntity:
					FightRuleMgr.g_fightMgr.breakEnemyRelation( self, enemyEntity )
				else:
					self.removeEnemy(id)

	
	def setPlayDeadEffect( self, boolValue ):
		"""
		"""
		self._isPlayDeadEffect = boolValue

	def isPlayDeadEffect( self ):
		"""
		是否播放死亡特效
		"""
		if self.getScript().getDeadEffectType() == csdefine.MONSTER_DEAD_EFFECT_TYPE_NORMAL:
			return False
		if self.getScript().getDeadEffectType() == csdefine.MONSTER_DEAD_EFFECT_TYPE_ALWAYS:
			return True

		return self._isPlayDeadEffect

	def isPlayDeadMortuaryEffect( self ):
		"""
		是否播放死亡停尸效果
		"""
		if self.getScript().getDeadEffectType() == csdefine.MONSTER_DEAD_EFFECT_TYPE_MORTUARY:
			return True
		return False

	def onBeKill( self, killerID, deadEffect, actForbid ):
		"""
		被击杀
		执行怪物被击杀的处理
		"""
		CombatInterface.CombatInterface.onBeKill( self, killerID, deadEffect, actForbid )
		
		# 触发任务目标:怪物击杀事件
		killer = KBEngine.entities.get( killerID )
		realKiller = killer
		if killer:
			if killer.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER and \
					killer.getMonsterType() == csdefine.MONSTER_TYPE_MONSTER_EXT_CALL and killer.owner:
				realKiller = KBEngine.entities.get( killer.owner.id, None )

			if killer.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
				realKiller = killer.getOwnerEntity()
				
			if realKiller.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:				# 只有玩家才进奖励流程
				DropMgr.g_dropMgr.drop(self, realKiller, {})
			self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_BE_KILL, [], realKiller)

		#CST-11812 程序需求——怪物所有权功能拓展
		#触发怪物拥有者玩家的击杀怪物任务事件
		for eid in self.getOwnerIDList():
			entity = KBEngine.entities.get(eid, None)
			if entity and entity.getEntityFlag()==csdefine.ENTITY_FLAG_ROLE:
				entity.triggerQuestEvent(QuestEventDefine.EVENT_MONSTER_DIE, self.scriptID)
		
		self.spaceEvent_onMonsterBeKill(killerID)
			

	def resetEnemyList( self ):
		"""
		重置所有敌人信息表
		"""
		CombatInterface.CombatInterface.resetEnemyList( self )
		self.resetHatredList()
		self.monsterAISetTarget( 0 )
		self.firstBruise = False
		
		
	def onSkillInterrupted( self, skillID, reason):
		"""
		virtual method
		当施法被打断时的通知
		"""
		CombatInterface.CombatInterface.onSkillInterrupted(self, skillID, reason)
		self.behOver( csdefine.BEHAVIOUR_TYPE_SPELL)
		#self.triggerEvent(csdefine.ENTITY_EVENT_SKILL_SUCCESSFUL,skillInstance.getID())

	def onSkillEnd( self, skillInstance, castResult ):
		"""
		virtual method.
		技能打击结束
		@param  skillInstance: 技能实例
		@type   skillInstance: SPELL
		"""
		CombatInterface.CombatInterface.onSkillEnd( self, skillInstance, castResult )
		self.behOver( csdefine.BEHAVIOUR_TYPE_SPELL)
		self.triggerEvent(csdefine.ENTITY_EVENT_SKILL_SUCCESSFUL, [skillInstance.getID(),])

	def gangQi_changeState( self, state ):
		"""
		罡气状态改变
		"""
		CombatInterface.CombatInterface.gangQi_changeState( self, state )
		self.monsterAITriggerEvent( csdefine.ENTITY_EVENT_GANG_QI_CHANGE )

	def isWillDead(self, damage):
		"""
		受术者是否会死亡
		"""
		if self.isState( csdefine.ENTITY_STATE_DEAD ) or self.isState( csdefine.ENTITY_STATE_PEAD ) \
			or self.isState( csdefine.ENTITY_STATE_RESET ):
			return False
		if self.hasEffectState( csdefine.EFFECT_STATE_UNYIELDING ):
			return False
			
		return damage >= self.HP

	#----------------------------------------------------------------------------------------------
	def onFightCall( self, targetID ):
		"""
		<define method>
		战斗呼叫
		@param  targetID: 攻击目标ID
		@type   targetID: OBJECT_ID
		"""
		if self.callSign:
			return

		if self.getState() == csdefine.ENTITY_STATE_FIGHT:
			return
		
		targetEntity = KBEngine.entities.get( targetID, None )
		if not targetEntity:
			KBEDebug.DEBUG_MSG("onFightCall targetID = %d is not found!"%targetID)
			return
		
		if self.canBuildEnemyRelation( targetEntity ):
			self.callSign = True
			FightRuleMgr.g_fightMgr.buildEnemyRelation( self, targetEntity )

	#-------------------------------------------------------------------------------------------------
	def getTargetID( self ):
		"""
		得到攻击目标ID
		"""
		if self.getTauntID() and self.getTauntID() in self.enemyList:
			return self.getTauntID()
		return self.targetID

	#-----------------event-----------------------------------
	def triggerEvent( self, eventType, args, triggerEntity = None ):
		"""
		触发事件
		"""
		self.monsterAITriggerEvent( eventType, args, triggerEntity )

	#-----------------------Property-----------------------------------------------------------
	#-----------------------monster property--------------------------
	def getEquipAttachProperties(self):
		"""
		为了在CombatInterface中统一处理属性计算
		"""
		return {}

	#----------------------------获取属性数据，重新对属性的4个值进行赋值-----------------------
	#----------------------------需要的才需要重载，部分方法------------------------------------
	def getBaseProperties(self):
		"""
		通过配置获取基础属性数值
		@return: dict {propertyID: value}
		"""
		profession = self.profession
		attrlevel = self.attrLevel
		level = self.level
		#KBEDebug.DEBUG_MSG("Monster[%s], profession[%d], attrlevel[%d], level[%d]"%(self.scriptID, profession, attrlevel, level))
		return ItemSystemExp.g_MonsterPropertyValueCfg.getData(profession, attrlevel, level)

	#----------------------------属性计算的部分-----------------------------------------------
	def calcBaseProperties(self):
		"""
		重新设置基础属性值, xxx_base
		"""
		self.setMonsterBaseProperties()

	def calcExtraProperties(self):
		"""
		计算属性的成长值，xxx_extra
		装备只影响属性成长值
		"""
		buffdic = self.getBuffProperties().get("_extra", {})
		dic = ItemSystemExp.combineDict(buffdic, self.getEquipAttachProperties().get("_extra", {}))
		self.setMonsterExtraProperties(dic)

	#----------------------------需要的才需要重载，部分方法------------------------------------
	def getBasicValue( self, key, value ):
		"""
		"""
		spaceHPModifyRatio = 1.0
		spaceDamageModifyRatio = 1.0
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceHPModifyRatio = spaceEntity.spaceHPModifyRatio
			spaceDamageModifyRatio = spaceEntity.spaceDamageModifyRatio
		if key == ItemTypeEnum.HP or key == ItemTypeEnum.CORPOREITY:
			return int(value * self.hpModifyRatio * spaceHPModifyRatio)
		elif key == ItemTypeEnum.DAMAGE or key == ItemTypeEnum.MAGICDAMAGE or key == ItemTypeEnum.CORPOREITY or key == ItemTypeEnum.STRENGTH or key == ItemTypeEnum.INTELLECT:
			return int(value * self.damageModifyRatio * spaceDamageModifyRatio)
		else:
			return value
	#---------------------- timer --------------------------
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		MonsterAIInterface.MonsterAIInterface.timerValeDelCB( self, timerArg )
		CombatInterface.CombatInterface.timerValeDelCB( self, timerArg )

	#-------------------------------------------
	# KBEngine calback
	#-------------------------------------------
	def onWitnessed( self, isWitnessed ):
		"""
		玩家视野范围内才开始执行AI
		"""
		MonsterAIInterface.MonsterAIInterface.onWitnessed( self, isWitnessed )

	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		MonsterStateInterface.onEnterDead(self)
		GangQiInterface.GangQiInterface.onEnterDead( self )
		self.setHPAttrValue(0)
		self.setMPAttrValue(0)
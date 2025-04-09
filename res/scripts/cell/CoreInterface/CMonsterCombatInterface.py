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
from CoreInterface import CMonsterAIInterface
from CoreInterface import MonsterOwnerInterface
from StateInterface import CMonsterStateInterface
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


class CMonsterCombatInterface(
		CMonsterStateInterface.CMonsterStateInterface,
		CombatInterface.CombatInterface,
		CMonsterAIInterface.CMonsterAIInterface,
		MonsterOwnerInterface.MonsterOwnerInterface,
	):
	def __init__( self ):
		CMonsterStateInterface.CMonsterStateInterface.__init__(self)
		CMonsterAIInterface.CMonsterAIInterface.__init__(self)
		CombatInterface.CombatInterface.__init__( self )
		MonsterOwnerInterface.MonsterOwnerInterface.__init__( self )
		self.updateBornHPMP()
		self._isPlayDeadEffect = False # 是否播放死亡特效
		

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
	
	def onHPChanged( self, oldValue ):
		"""
		血量改变回调
		"""
		CombatInterface.CombatInterface.onHPChanged( self, oldValue )
		self.triggerEvent( csdefine.ENTITY_EVENT_HP_CHANGE,(self.HP, oldValue))

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

	def c_addDamageList( self, entityID, damage ):
		"""
		添加伤害列表
		@param entityID  : entityID
		@param damage	 : 伤害值
		"""
		# 如果回走状态 则忽略任何敌人
		if self.isState( csdefine.ENTITY_STATE_RESET ):
			return
		CombatInterface.CombatInterface.addDamageList( self, entityID, damage )

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
		caster = KBEngine.entities.get( killerID )
		if caster:
			if caster.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER and caster.getMonsterType() == csdefine.MONSTER_TYPE_MONSTER_EXT_CALL \
				and caster.owner:
					master = KBEngine.entities.get( caster.owner.id, None )
					if master:
						master.triggerQuestEvent(QuestEventDefine.EVENT_MONSTER_DIE, self.scriptID)
						self.drop( master )
						return
			if caster.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
				owner = caster.getOwnerEntity()
				if owner:
					owner.triggerQuestEvent(QuestEventDefine.EVENT_MONSTER_DIE, self.scriptID)
					self.drop( owner )
					return

			if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				caster.triggerQuestEvent(QuestEventDefine.EVENT_MONSTER_DIE, self.scriptID)
		
			self.drop( caster )
		self.spaceEvent_onMonsterBeKill( killerID )

	def drop( self, killber ):
		"""
		掉落
		"""
		if killber.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killber = killber.getOwnerEntity()

		if killber.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER and killber.getMonsterType() == csdefine.MONSTER_TYPE_MONSTER_EXT_CALL \
				and killber.owner:
			killber = KBEngine.entities.get( killber.owner.id, None )
			
		if killber.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			DropMgr.g_dropMgr.drop( self, killber, {} )

	def resetEnemyList( self ):
		"""
		重置所有敌人信息表
		"""
		CombatInterface.CombatInterface.resetEnemyList( self )
		#self.monsterAISetTarget( 0 )
		self.firstBruise = False
		
	def onSkillInterrupted( self, skillID, reason):
		"""
		virtual method
		当施法被打断时的通知
		"""
		CombatInterface.CombatInterface.onSkillInterrupted(self, skillID, reason)
		self.behOver( csdefine.BEHAVIOUR_TYPE_SPELL)
		#self.triggerEvent(csdefine.ENTITY_EVENT_SKILL_SUCCESSFUL,skillInstance.getID())

	def gangQi_changeState( self, state ):
		"""
		罡气状态改变
		"""
		CombatInterface.CombatInterface.gangQi_changeState( self, state )
		#self.monsterAITriggerEvent( csdefine.ENTITY_EVENT_GANG_QI_CHANGE )

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
		#self.monsterAITriggerEvent( eventType, args, triggerEntity )

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
		CombatInterface.CombatInterface.timerValeDelCB( self, timerArg )

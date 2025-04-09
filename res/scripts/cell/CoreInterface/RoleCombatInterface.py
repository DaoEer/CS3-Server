# -*- coding: utf-8 -*-



#python
import time
import json
import math
#engine
import KBEngine
#common
import csdefine
import csconst
import KBEDebug
import Functions
import ItemTypeEnum
import QuestEventDefine
#cell
import Const
import csstatus
import FightRuleMgr
from StateInterface.RoleStateInterface import RoleStateInterface
from CoreInterface import CombatInterface
import CoreInterface.GangQiInterface as GangQiInterface
from CoreInterface import RoleCompeteInterface
from ImpInterface import XiuweiInterface
import ConfigObject.Skill.SkillBase.CombatSkill as CombatSkill
from ConfigObject.Trade.TradeMgr import g_tradeMgr
import ItemSystemExp
import FightRuleMgr
from XiuweiLoader import g_XiuweiMgr
from ItemSystemExp import g_CombatNormalDamager
from MsgLogger import g_logger
from ConfigObject.Skill.PassiveSkillBarLoader import g_passiveSkillBars

class RoleCombatInterface( RoleStateInterface, CombatInterface.CombatInterface, XiuweiInterface.XiuweiInterface ):
	"""
	玩家战斗接口
	"""
	def __init__( self ):
		RoleStateInterface.__init__(self)
		XiuweiInterface.XiuweiInterface.__init__( self )
		CombatInterface.CombatInterface.__init__( self )
		self.totalEquipDamage = 0
		if self.getLevel() < csconst.PK_PROTECT_LEVEL:	#新手玩家锁定PK模式
			self.lockPkMode()
			self.setPkMode( csdefine.PK_MODE_PEACE )
		if len(self.passiveSkillsBar) <= 0:				#新账号初始化被动技能栏
			self.initPassiveSkillsBar()
		self.updateKvReduceTimer()
		self.timeCallBack = 0

	def doEnterSpace( self ):
		"""
		KBEngine callback
		进入一个空间调用
		"""
		CombatInterface.CombatInterface.doEnterSpace( self )

	def doLeaveSpace( self ):
		"""
		KBEngine callback
		离开一个空间调用（在doEnterSpace之后）
		"""
		CombatInterface.CombatInterface.doLeaveSpace( self )
		
	def onAddEnemy( self, enemyID ):
		"""
		"""
		if self.isTeleporting:
			return
		CombatInterface.CombatInterface.onAddEnemy( self, enemyID )

		self.fight_lastTime_record = KBEngine.time()

	def onRemoveEnemy( self, entityID ):
		"""
		"""
		CombatInterface.CombatInterface.onRemoveEnemy( self, entityID )

	def onEnemyListChange( self, entityID ):
		"""
		战斗信息表有改动通知
		"""
		if len( self.enemyList ) == 0 and self.getState() == csdefine.ENTITY_STATE_FIGHT:
			if not self.isTeleporting:
				self.fightFreeTimer = self.addTimerCallBack( 3, "delayLeaveFightState", (csdefine.ENTITY_STATE_FREE,) )
			else:
				self.changeState( csdefine.ENTITY_STATE_FREE )
		elif len( self.enemyList ) != 0 and self.fightFreeTimer != 0:	#加战斗列表，取消变回自由状态的timer
			self.popTimer( self.fightFreeTimer )
			self.fightFreeTimer = 0
		
		self.updateKvReduceTimer()

	def delayLeaveFightState(self, state):
		"""
		延迟脱离战斗，避免出现当玩家已经死亡时进入自由状态
		"""
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		self.changeState( csdefine.ENTITY_STATE_WARN )
		self.applyEnterWarn(csdefine.ROLE_WARN_REASON_NONE, 3)

	def clearEnemyList( self ):
		"""
		清空敌人列表
		"""
		for id in list( self.enemyList ):
			enemyEntity = KBEngine.entities.get( id, None )
			if enemyEntity:
				FightRuleMgr.g_fightMgr.breakEnemyRelation( self ,enemyEntity )
			else:
				self.removeEnemy(id)

	def setCooldown( self, cooldownDict ):
		"""
		设置冷却时间
		"""
		CombatInterface.CombatInterface.setCooldown( self, cooldownDict )
		self.updateCooldownToClient(cooldownDict)

	def changeCooldown( self, cooldownDict ):
		"""
		增/减CD
		"""
		CombatInterface.CombatInterface.changeCooldown( self, cooldownDict )
		self.updateCooldownToClient(cooldownDict)

	def updateCooldownToClient( self, cooldownDict ):
		"""
		更新冷却时间数据到客户端
		"""
		if len(self.attrCooldowns) == 0:
			return
		
		idList = []
		endTimeList = []
		persistTimeList = []
		for dDict in self.attrCooldowns:
			if dDict["id"] in cooldownDict:
				idList.append( str(dDict["id"]) )
				endTimeList.append( str(dDict["endTime"]) )
				persistTimeList.append( str(dDict["persistTime"]) )
		self.client.SetCooldown( idList, endTimeList, persistTimeList )

	def initCooldownToClient(self):
		"""
		玩家初始化时，更新冷却时间数据到客户端
		"""
		if len(self.attrCooldowns) == 0:
			return
		
		idList = []
		endTimeList = []
		persistTimeList = []
		for dDict in self.attrCooldowns:
			idList.append( str(dDict["id"]) )
			endTimeList.append( str(dDict["endTime"]) )
			persistTimeList.append( str(dDict["persistTime"]) )
		self.client.SetCooldown( idList, endTimeList, persistTimeList )

	def isFightSpell( self, spellInstance ) :
		"""
		是否是战斗技能
		"""
		if isinstance( spellInstance, CombatSkill.CombatSkill ):
			return True
		return False

	def onSkillBegin( self, spellInstance, target ):
		"""
		virtual method.
		技能开始

		@param  spellInstance: 技能实例
		@type   spellInstance: SPELL
		"""
		if self.isFightSpell( spellInstance ) :
			self.fight_lastTime_record = KBEngine.time()
			
		if spellInstance.getCollisionType() != csdefine.COLLISION_DEFAULT and not spellInstance.isInstantSkill():
			self.setCollisionType( spellInstance.getCollisionType() )
			
		# 触发“使用技能”类任务目标完成
		monsterScriptID = ""
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			entity = target.getObject()
			if entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				monsterScriptID = "Role"
			else:
				monsterScriptID = entity.getScriptID()
		self.triggerQuestEvent( QuestEventDefine.EVENT_USE_SKILL, ( spellInstance.getID(), monsterScriptID ) )
		CombatInterface.CombatInterface.onSkillBegin( self, spellInstance, target )
		
	def onSkillEnd( self, skillInstance, castResult ):
		"""
		virtual method.
		技能结束

		@param  skillInstance: 技能实例
		@type   skillInstance: SPELL
		"""
		if skillInstance.getCollisionType() != csdefine.COLLISION_DEFAULT and not skillInstance.isInstantSkill():
			self.setCollisionType( csdefine.COLLISION_DEFAULT )
		
		CombatInterface.CombatInterface.onSkillEnd( self, skillInstance, castResult )

	def receiveDamage( self, casterID, skillID, damageType, damage, isCritical, isParry, deadEffect, actForbid ):
		"""
		Define and virtual method.
		接受伤害。
		@param   casterID: 施法者ID
		@type    casterID: OBJECT_ID
		@param    skillID: 技能ID
		@type     skillID: INT
		@param damageType: 伤害类型；see also csdefine.py/DAMAGE_TYPE_*
		@type  damageType: INT
		@param     damage: 伤害数值
		@type      damage: INT
		@param     deadEffect: 是否播放暴尸（因为暴尸跟技能相关）
		@type      deadEffect: Bool
		"""
		if self.state == csdefine.ENTITY_STATE_DEAD or self.state == csdefine.ENTITY_STATE_PEAD or self.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):
			return

		if self.HP == 0 and self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		oldHP = self.HP
		#切磋中 不能被对手打死 只能被对手打到剩一点血 但是可以被其它第三方单位打死
		caster = KBEngine.entities.get(casterID, None)
		if caster and self.competeState == csdefine.COMPETE_FIRE and \
			(casterID == self.competeTargetID or self.getActivePetCell() and casterID == self.getActivePetCell().id) and int(self.HP - damage)<=1:
				self.setHP(1)
				self.loseCompete()
		else:
			if self.hasEffectState( csdefine.EFFECT_STATE_UNYIELDING ) and int(self.HP - damage ) <= 1:
				self.setHP(1)			
			else:
				self.setHP( self.HP - damage )

		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			self.setMP( 0 )
			self.onBeKill( casterID, deadEffect, actForbid )
		
		finalDamage = oldHP - self.HP
		self.onReceiveDamage( casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )

		

	def onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry ):
		"""
		virtual method
		接受伤害回调
		"""
		CombatInterface.CombatInterface.onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )
		self.addDamageList( casterID, damage )
		self.onRoleRecvieDamage( casterID )

	def onRoleRecvieDamage( self, casterID ):
		"""
		玩家之间脱战
		"""
		#切磋过程中不遵循此脱战规则
		if self.competeState != csdefine.COMPETE_NONE:
			return

		enemy = KBEngine.entities.get( casterID )
		if self.timeCallBack and (enemy.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or enemy.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET):
			self.popTimer(self.timeCallBack)
			self.timeCallBack = 0
		if casterID in self.enemyList and (enemy.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or enemy.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET):
			if self.getState() == csdefine.ENTITY_STATE_DEAD:
				FightRuleMgr.g_fightMgr.breakEnemyRelation( self, enemy )
			else:
				for casterID in self.enemyList:
					self.timeCallBack = self.addTimerCallBack( 8, "onDamageListCompare", ( self.id, casterID, ))	

	def onBeKill( self, killerID, deadEffect, actForbid ):
		"""
		被击杀
		"""
		CombatInterface.CombatInterface.onBeKill( self, killerID, deadEffect, actForbid)
		
		#加杀气值
		killer = KBEngine.entities.get( killerID )
		if killer and killer.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			if killer.getRelationRule() == csdefine.ROLE_RELATION_RULE_PKMODE and killer.pkMode == csdefine.PK_MODE_SLAUGHTER:	#当前关系规则是“pk模式决定”并且pk模式为恶意模式
				#加仇人名单
				self.base.addFoe( killer.getName() )
				#对方加杀气值
				if killer.getLevel() - self.getLevel() < 10:
					killer.addKillingValue( 15 )
				elif killer.getLevel() - self.getLevel() < 20:
					killer.addKillingValue( 20 )
				else:
					killer.addKillingValue( 25 )
			#self.campBeKilled(killer)

		self.spaceEvent_OnRoleBeKill( killerID )

	def onSkillInterrupted( self, skillID, reason ):
		"""
		virtual method
		当施法被打断时的通知
		"""
		CombatInterface.CombatInterface.onSkillInterrupted(self, skillID, reason)


	def changeState(self,newState):
		"""
		<Define method>
		改变状态。
		@param newState	:	新的状态
		@type newState	:	integer
		"""
		state = newState
		if self.isApplyWarn and newState == csdefine.ENTITY_STATE_FREE:
			state = csdefine.ENTITY_STATE_WARN

		RoleStateInterface.changeState(self,state)

	def onHPChanged( self, oldValue ):
		"""
		血量改变回调
		"""
		CombatInterface.CombatInterface.onHPChanged( self, oldValue )
		self.triggerEntityEvent(csdefine.ENTITY_EVENT_HP_CHANGE, {})

	def onEnterFree(self):
		"""
		"""
		RoleStateInterface.onEnterFree(self)
		GangQiInterface.GangQiInterface.onEnterFree( self )

		#尝试开启自愈
		self.startRevertTimer()
		KBEDebug.DEBUG_MSG("onEnterFree")

	def onLeaveFree(self):
		"""
		"""
		RoleStateInterface.onLeaveFree(self)
		#停止自愈
		self.stopRevertTimer()


	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		RoleStateInterface.onEnterDead(self)
		GangQiInterface.GangQiInterface.onEnterDead( self )
		self.setHPAttrValue(0)
		self.setMPAttrValue(0)
		self.spaceEvent_roleDie()
		self.resetEnemyList()
		self.updateKvReduceTimer()
		if self.hasNormalFollowID():
			self._cancelNormalFollowFC(self.id)
		if self.getClient():
			self.client.CLIENT_ClearChasePosInfo()

	def onLeaveFight( self ):
		"""
		virtual method
		离开战斗
		"""
		if self.getClient():
			self.client.CLIENT_ClearChasePosInfo()

	def applyEnterWarn(self, applyWarnReason, delayTime = 0.0):
		"""
		申请进入警戒状态
			@param enterWarnReason：申请警戒的原因
			@Param delayTime ：     持续警戒的时间，0表示配一直
		"""
		self.isApplyWarn |= applyWarnReason
		if self.getState() == csdefine.ENTITY_STATE_FREE:
			self.changeState( csdefine.ENTITY_STATE_WARN )
		if delayTime:
			if self.applyWarnTimer:
				self.popTimer(self.applyWarnTimer)
			self.applyWarnTimer = self.addTimerCallBack( delayTime, "applyLeaveWarn", ( applyWarnReason, ) )

	def applyLeaveWarn(self, applyWarnReason):
		"""
		申请离开警戒状态
		@param leaveWarnReason: 申请警戒的原因
		"""
		if applyWarnReason == csdefine.ROLE_WARN_REASON_NONE:
			self.isApplyWarn = 0
		else:
			self.isApplyWarn &= ~applyWarnReason
			
		if self.applyWarnTimer:
			self.popTimer(self.applyWarnTimer)
			self.applyWarnTimer = 0
		if self.getState() == csdefine.ENTITY_STATE_WARN:
			self.changeState( csdefine.ENTITY_STATE_FREE )

	def isWillDead(self, damage):
		"""
		受术者是否会死亡
		"""
		if self.state == csdefine.ENTITY_STATE_DEAD or self.state == csdefine.ENTITY_STATE_PEAD or self.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):
			return False

		if self.HP == 0 and self.getState() == csdefine.ENTITY_STATE_DEAD:
			return False

		if self.hasEffectState( csdefine.EFFECT_STATE_UNYIELDING ):
			return False

		return damage >= self.HP


#-----------玩家血量相关------------------------------------------------------
	def setHP( self, value ):
		"""
		设置HP
		"""
		CombatInterface.CombatInterface.setHP(self, value)
		self.startRevertTimer()

#-----------玩家蓝量相关------------------------------------------------------
	def setMP( self, value ):
		"""
		设置MP
		"""
		CombatInterface.CombatInterface.setMP(self, value)
		self.startRevertTimer()

#-----------玩家技能相关------------------------------------------------------
	def initSkills( self ):
		"""
		初始化技能列表
		"""
		self.client.InitSkills( self.attrSkills )
		self.client.InitPassiveSkillBar( self.passiveSkillsBar )
		for skillID in self.attrSkills:
			skill = self.getSkill( skillID )

		for i in self.passiveSkillsBar.values():
			if i["skillID"]:
				self.activatePassiveSkill(i["skillID"])

	def addSkill( self, skillID, reason = csdefine.SKILL_ADD_REASON_NORMAL ):
		"""
		增加一个技能
		"""
		if self.hasSkill(skillID):
			KBEDebug.WARNING_MSG( "%s(%i): addSkill %i already exist." % ( self.getName(), self.id, skillID ) )
			return False

		if self.getSkill( skillID ):
			self.attrSkills.append( skillID )
			self.OnAddSkill( skillID )
			return True
	
	def OnAddSkill( self, skillID ):
		"""
		增加一个技能回调
		"""
		skill = self.getSkill( skillID )
		if skill.isPassiveSkill():
			skill.attachToCaster( self )
		skillIDName = skill._name
		self.statusMessage( csstatus.LEARN_SKILL_SUCESS, skillIDName)
		self.client.OnAddSkill( skillID )

	def removeSkill( self, skillID, reason = csdefine.SKILL_REMOVE_REASON_NORMAL ):
		"""
		删除一个技能
		"""
		if skillID not in self.attrSkills:
			KBEDebug.WARNING_MSG( "%s(%i): removeSkill %i not exist." % ( self.getName(), self.id, skillID ) )
			return False

		self.attrSkills.remove( skillID )
		self.OnRemoveSkill( skillID, reason )
		
	def OnRemoveSkill( self, skillID, reason = csdefine.SKILL_REMOVE_REASON_NORMAL ):
		"""
		删除一个技能回调
		"""
		skill = self.getSkill( skillID )
		if skill.isPassiveSkill():
			skill.detachToCaster( self )
		if reason != csdefine.SKILL_REMOVE_REASON_LEARN_SKILL:
			if self.isCurrentPostureSkill(skillID):
				self.onRemovePostureSkill(skill)
			self.client.OnRemoveSkill( skillID )

	def requestSkillLearn( self, srcEntityID, skillID, npcID ):
		"""
		<Exposed method>
		请求学习一个技能

		@param  srcEntityID: 玩家id
		@param   npcID: 导师ID
		@param  skillID: 技能ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		skillID = int( skillID )
		if self.hasSkill(skillID):
			self.statusMessage( csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR )
			return
		skillLearnData = g_tradeMgr.getSkillLearnData(skillID)
		if skillLearnData is None:
			KBEDebug.ERROR_MSG("Cannot find skill(%d) learn config!"%skillID)
			return
		if skillLearnData["ReqSkill"]:
			KBEDebug.ERROR_MSG("Something is err!!learn skill(%d), ReqSkill(%d)"%(skillID,skillLearnData["ReqSkill"]))
			return
		if self.level < skillLearnData["ReqLevel"]:
			self.statusMessage( csstatus.CAN_NOT_LEARN_SKILL_AS_LEVEL_NOT_ENOUGH )
			return
		
		payItems = { csdefine.TRADE_PAY_ITEM_POTENTIAL : skillLearnData["ReqPotential"] }
		payItems.update( self.getSkillLearnCostMoneyDatas(skillLearnData["Money"]) )
		self.requestPay(csdefine.TRADE_TYPE_LEARN_SKILL, int(npcID), payItems, 0, skillID)

	def requestSkillUpgrade( self, srcEntityID, skillID ):
		"""
		<Exposed method>
		请求升级一个技能

		@param  srcEntityID: 玩家id
		@param  skillID: 目标技能ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return	
		if skillID in self.attrSkills:
			return
		skillLearnData = g_tradeMgr.getSkillLearnData(skillID)
		if skillLearnData is None:
			KBEDebug.ERROR_MSG("Cannot find skill(%d) learn config!"%skillID)
			return
		if not skillLearnData["ReqSkill"] in self.attrSkills:
			KBEDebug.ERROR_MSG("Learn skill(%d) err!cannot find reqSkill(%d)"%(skillID,skillLearnData["ReqSkill"]))
			return
		if self.level < skillLearnData["ReqLevel"]:
			self.statusMessage( csstatus.CAN_NOT_LEARN_SKILL_AS_LEVEL_NOT_ENOUGH )
			return
		
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_POTENTIAL] = skillLearnData["ReqPotential"]
		payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = skillLearnData["material"]
		payItems.update( self.getSkillLearnCostMoneyDatas(skillLearnData["Money"]) )
		self.requestPay(csdefine.TRADE_TYPE_LEARN_SKILL, 0, payItems, skillLearnData["ReqSkill"], skillID)

	def requestSkillUpgradeMax( self, srcEntityID, skillID ):
		"""
		<Exposed method>
		请求将一个技能升到最大等级

		@param  srcEntityID: 玩家id
		@param  skillID: 技能ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return	
		if not skillID in self.attrSkills:
			KBEDebug.ERROR_MSG("Can not find skillID(%d)"%skillID)
			return
		maxSkill, potential, money, materials = g_tradeMgr.getMaxLevelSkillLearnDatas(self, skillID)
		if maxSkill:
			payItems = { csdefine.TRADE_PAY_ITEM_POTENTIAL : potential }
			payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = materials
			payItems.update( self.getSkillLearnCostMoneyDatas( money ) )
			self.requestPay(csdefine.TRADE_TYPE_LEARN_SKILL, 0, payItems, skillID, maxSkill)
		else:
			KBEDebug.ERROR_MSG("Upgrade ERR!!maxSkill(%d), potential(%d)"%(maxSkill, potential))

	def getSkillLearnCostMoneyDatas( self, money ):
		"""
		获得技能学习和技能消耗的数据
		"""
		tempCostMoneyDict = {}
		tempCostMoneyDict[ csdefine.TRADE_PAY_ITEM_BIND_MONEY ] = 0
		tempCostMoneyDict[ csdefine.TRADE_PAY_ITEM_MONEY ] = 0
		if self.getBindMoney() + self.getMoney() < money:
			tempCostMoneyDict[ csdefine.TRADE_PAY_ITEM_MONEY ] = money
			return tempCostMoneyDict

		if self.getBindMoney() >= money:
			tempCostMoneyDict[ csdefine.TRADE_PAY_ITEM_BIND_MONEY ] = money
		else:
			remainMoney = money - self.getBindMoney()
			tempCostMoneyDict[ csdefine.TRADE_PAY_ITEM_BIND_MONEY ] = self.getBindMoney()
			tempCostMoneyDict[ csdefine.TRADE_PAY_ITEM_MONEY ] = remainMoney

		return tempCostMoneyDict

	def presentedSkill( self, skillID ):
		"""
		直接学习一个技能
		"""
		oldSkillID = 0
		for getID in self.attrSkills:
			if int(getID/1000) == int(skillID/1000):
				oldSkillID = getID

		self.onSuccessPaySkill( oldSkillID, skillID )

	def onSuccessPaySkill( self, oldSkillID, newSkillID ):
		"""
		学习技能

		@param  oldSkillID: 升级前技能id（如果为激活技能，该变量为0）
		@param   newSkillID: 新技能id
		"""
		if oldSkillID != 0:
			self.removeSkill(oldSkillID, csdefine.SKILL_REMOVE_REASON_LEARN_SKILL)
			self.base.onRoleSkillUpgrade(oldSkillID, newSkillID)

		self.addSkill(newSkillID)

		# 玩家学习某个技能任务目标完成
		self.triggerQuestEvent( QuestEventDefine.EVENT_LEARN_SKILL, newSkillID )
		self.onLearnPostureSkill(oldSkillID, newSkillID )
		
		#添加日志
		skillLearnData = g_tradeMgr.getSkillLearnData(newSkillID)
		if oldSkillID == 0:
			self.client.CLIENT_FirstLearnSkillNotify( newSkillID )
			g_logger.skillLearnLog( self.playerDBID, self.getName(), newSkillID, skillLearnData["UName"], skillLearnData["ReqPotential"], self.potential )
		else:
			g_logger.skillUpgradeLog( self.playerDBID, self.getName(), newSkillID, oldSkillID, skillLearnData["UName"], skillLearnData["ReqPotential"], self.potential )


	def requestOpenSkillLearn( self, teacherID ):
		"""
		由NPC对话请求打开技能学习界面

		@param   teacherID: 导师id
		"""
		self.client.CLIENT_requestOpenSkillLearn( teacherID )

	def hasSkill( self, skillID ):
		"""
		判断玩家是否拥有某技能（包括同一个技能低等级的）
		"""
		if skillID in self.attrSkills:
			return True
		for id in self.attrSkills:
			if (int(math.log10(skillID)) +1) == 9:
				if int(skillID/1000) == int(id/1000) and skillID <= id:
					return True
			elif (int(math.log10(skillID)) +1) == 8:
				if int(skillID/100) == int(id/100) and skillID <= id:
					return True
		return False

	def onLearnPostureSkill(self, oldSkillID, newSkillID):
		"""
		学习心法技能
		"""
		learnData = g_tradeMgr.getSkillLearnData( newSkillID )
		if not learnData:
			return
		skillClass = learnData.get("SkillClass", 0)
		if skillClass != csdefine.SKILL_CLASSS_CHANGE_POSTURE:
			return
		skill = self.getSkill( newSkillID )
		skillPosture = int(learnData["Param1"])
		level = int(learnData["Param2"])
		self.changeSkillPosture(skillPosture, level, skill)

	def isCurrentPostureSkill(self, oldSkillID):
		"""
		移除的技能是否是当前心法技能
		"""
		learnData = g_tradeMgr.getSkillLearnData( oldSkillID )
		if not learnData:
			return False
		skillClass = learnData.get("SkillClass", 0)
		if skillClass != csdefine.SKILL_CLASSS_CHANGE_POSTURE:
			return False
		skillPosture = int(learnData["Param1"])
		level = int(learnData["Param2"])
		if skillPosture == self.skillPosture and level == self.skillPostureLevel:
			return True
		return False

	def onRemovePostureSkill(self, skill):
		"""
		删除心法技能的回调
		"""
		postureSkill = None
		for skillID in self.attrSkills:
			learnData = g_tradeMgr.getSkillLearnData( skillID )
			if not learnData:
				continue
			skillClass = learnData.get("SkillClass", 0)
			if skillClass == csdefine.SKILL_CLASSS_CHANGE_POSTURE:
				postureSkill = learnData

		if postureSkill:
			self.changeSkillPosture(int(postureSkill["Param1"]), int(postureSkill["Param2"]), skill)
		else:
			self.changeSkillPosture(csdefine.SKILL_POSTURE_NONE, 1, skill)

	def requestPassiveSkillLearn( self, srcEntityID, skillID ):
		"""
		<Exposed method>
		请求学习一个被动技能

		@param  srcEntityID: 玩家id
		@param   npcID: 导师ID
		@param  skillID: 技能ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.learnPassiveSkill(skillID)

	def learnPassiveSkill( self, skillID ):
		"""
		学习被动技能
		"""
		if self.hasSkill(skillID):
			self.statusMessage( csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR )
			return
		passiveSkillLearnData = g_tradeMgr.getPassiveSkillLearnData(skillID)
		if passiveSkillLearnData is None:
			KBEDebug.ERROR_MSG("Cannot find passive skill(%d) learn config!"%skillID)
			return
		self.onSuccessPayPassiveSkill(0, skillID)

	def requestPassiveSkillUpgrade( self, srcEntityID, skillID ):
		"""
		<Exposed method>
		请求升级一个被动技能

		@param  srcEntityID: 玩家id
		@param  skillID: 目标技能ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if self.hasSkill(skillID):
			self.statusMessage( csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR )
			return

		passiveSkillLearnData = g_tradeMgr.getPassiveSkillLearnData(skillID)
		if passiveSkillLearnData is None:
			KBEDebug.ERROR_MSG("Cannot find passive skill(%d) learn config!"%skillID)
			return
		if passiveSkillLearnData["SkillBook"] == "":
			return
		SkillBookID = int(passiveSkillLearnData["SkillBook"])

		if self.level < passiveSkillLearnData["ReqLevel"]:
			self.statusMessage( csstatus.CAN_NOT_LEARN_SKILL_AS_LEVEL_NOT_ENOUGH )
			return
		
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_POTENTIAL] = passiveSkillLearnData["ReqPotential"]
		payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = {SkillBookID : 1}
		payItems.update( self.getSkillLearnCostMoneyDatas(passiveSkillLearnData["Money"]) )
		self.requestPay(csdefine.TRADE_TYPE_LEARN_PASSIVE_SKILL, 0, payItems, passiveSkillLearnData["ReqSkill"], skillID)

	def onSuccessPayPassiveSkill( self, oldSkillID, newSkillID ):
		"""
		学习技能

		@param  oldSkillID: 升级前技能id（如果为激活技能，该变量为0）
		@param   newSkillID: 新技能id
		"""
		if oldSkillID != 0:
			self.removeSkill(oldSkillID, csdefine.SKILL_REMOVE_REASON_LEARN_SKILL)

		self.addSkill(newSkillID)

		# 玩家学习某个技能任务目标完成
		self.triggerQuestEvent( QuestEventDefine.EVENT_LEARN_SKILL, newSkillID )

		# 卸掉旧技能和装上新技能
		for index, value in self.passiveSkillsBar.items():
			if oldSkillID != 0 and value["skillID"] == oldSkillID:
				self.requestActivatePassiveSkill(self.id, newSkillID, index)
				break

	def forgetPassiveSkill( self, skillID ):
		"""
		遗忘被动技能
		"""
		passiveSkillLearnData = g_tradeMgr.getPassiveSkillLearnData(skillID)
		if passiveSkillLearnData is None:
			KBEDebug.ERROR_MSG("Cannot find passive skill(%d) learn config!"%skillID)
			return False

		if passiveSkillLearnData["SleepEffectID"]:
			self.addFixIDEffect( self, passiveSkillLearnData["SleepEffectID"])

		for index in self.passiveSkillEffectIndex.pop(skillID, []):
			self.removeFixIDHoldEffect(index)
		self.removeSkill(skillID)
		for index, value in self.passiveSkillsBar.items():
			if value["skillID"] == skillID:
				self.requestCancelUnActivatePassiveSkill(self.id, index)
		return True

	def activatePassiveSkill(self, skillID):
		"""
		激活被动技能
		"""
		# 注册被动技能
		skillInst = self.getSkill(skillID)
		if skillInst == None:
			return
		skillInst.attachToCaster(self)

		amount = 0
		for i in self.passiveSkillsBar.values():
			if i["skillID"]:
				amount += 1
		if amount > csconst.ACT_PASSIVE_SKILL_MAX:
			return
		passiveSkillLearnData = g_tradeMgr.getPassiveSkillLearnData(skillID)
		if passiveSkillLearnData is None:
			KBEDebug.ERROR_MSG("Cannot find passive skill(%d) learn config!"%skillID)
			return

		if passiveSkillLearnData["ActEffectID"]:
			self.addFixIDEffect( self, passiveSkillLearnData["ActEffectID"])

		if passiveSkillLearnData["ActHoldEffectID"]:
			indexList = self.passiveSkillEffectIndex.get(skillID, [])
			index = self.addFixIDHoldEffect(passiveSkillLearnData["ActHoldEffectID"], self)
			indexList.append(index)
			self.passiveSkillEffectIndex[skillID] = indexList

	def sleepPassiveSkill(self, skillID):
		"""
		冻结被动技能
		"""
		# 取消注册被动技能
		skillInst = self.getSkill(skillID)
		if skillInst == None:
			return
		skillInst.detachToCaster(self)

		passiveSkillLearnData = g_tradeMgr.getPassiveSkillLearnData(skillID)
		if passiveSkillLearnData is None:
			KBEDebug.ERROR_MSG("Cannot find passive skill(%d) learn config!"%skillID)
			return
		if passiveSkillLearnData["SleepEffectID"]:
			self.addFixIDEffect( self, passiveSkillLearnData["SleepEffectID"])

		for index in self.passiveSkillEffectIndex.pop(skillID, []):
			self.removeFixIDHoldEffect(index)

	#-----------------------Property-----------------------------------------------------------
	def getBaseProperties(self):
		"""
		通过配置获取基础属性数值
		@return: dict {propertyID: value}
		"""
		profession = self.profession
		level = self.level
		return ItemSystemExp.g_RolePropertyValueCfg.getData(profession, level)

	def calcBaseProperties(self):
		"""
		重新设置基础属性值, xxx_base
		"""
		self.setRoleBaseProperties()

	def calcExtraProperties(self):
		"""
		计算属性的成长值，xxx_extra
		装备只影响属性成长值
		"""
		buffdic = self.getBuffProperties().get("_extra", {})
		dic = ItemSystemExp.combineDict(buffdic, self.getEquipAttachProperties().get("_extra", {}))
		self.setRoleExtraProperties(dic)

	def getXiuweiExtraProperties( self, key ):
		"""
		获得修为的成长值
		"""
		xiuWeiData = g_XiuweiMgr.getRoleXiuWeiData( self.getXiuweiLevel() )
		if xiuWeiData == None:return 0
		if key == ItemTypeEnum.HP:
			return int(xiuWeiData["hp"])
		elif key == ItemTypeEnum.MP:
			return int(xiuWeiData["mp"])
		elif key == ItemTypeEnum.DAMAGE:
			return int(xiuWeiData["damage"])
		elif key == ItemTypeEnum.MAGICDAMAGE:
			return int(xiuWeiData["magic_damage"])
		elif key == ItemTypeEnum.CURE:
			return int(xiuWeiData["cure"])
		elif key == ItemTypeEnum.ARMOR:
			return int(xiuWeiData["armor"])
		elif key == ItemTypeEnum.MAGICARMOR:
			return int(xiuWeiData["magic_armor"])
		elif key == ItemTypeEnum.GANGQI_MAX:
			return int(xiuWeiData["gangQiValue_Max"])
		elif key == ItemTypeEnum.GANGQI_DAMAGE_POINT:
			return int(xiuWeiData["gangQi_damagePoint"])
		elif key == ItemTypeEnum.GANGQI_ARMOR_POINT:
			return int(xiuWeiData["gangQi_armorPoint"])
		elif key == ItemTypeEnum.GANGQI_QIJIE_REVIVE:
			return int(xiuWeiData["gangQi_qiJieRevive"])
		elif key == ItemTypeEnum.GANGQI_QIYING_REVIVE:
			return int(xiuWeiData["gangQi_qiYingRevive"])
		else: return 0

	#----------------------------获取属性数据，重新对属性的4个值进行赋值-----------------------
	def getExchangeTwoPropertyValue(self, propertyID):
		"""
		获取一级属性兑换的二级属性property的值
		@propertyID,二级属性ID
		"""
		return self.getRoleExchangeTwoProperty(propertyID)


	#-----------------装备损耗相关-----------------------------------------------------
	def equipWeaponAbrasion( self,damageValue ):
		"""
		武器损耗
		"""
		self.totalEquipDamage += damageValue
		if self.totalEquipDamage > 10000:
			damageValue = self.totalEquipDamage
			self.totalEquipDamage = 0
		else:
			return
		equipItems = self.getItemListByKBType( ItemTypeEnum.BAG_EQUIP)
		equipItems = [ k for k in equipItems if k.getHardiness() > 0 and k.getEquipPart() in ItemTypeEnum.EQUIP_ALL_WEAPON ]	# 只取武器
		for equip in equipItems:
			self.reduceHardiness( equip, -damageValue )

	def reduceHardiness( self, equip, damageValue ):
		"""
		减少耐久度
		"""
		if damageValue == 0:
			return
		if damageValue < 0:
			damageValue = self.getKvPlusValue( damageValue )	#杀气值影响掉耐久
		srcHardiness = equip.getHardiness()
		hardiness = srcHardiness + damageValue
		if srcHardiness == hardiness:
			return
		if hardiness <= 0:
			hardiness = 0
		equip.setHardiness( int(hardiness),self )

	def equipArmorAbrasion( self, damageValue ):
		"""
		防具损耗
		"""
		if damageValue < 0:
			return
		equipItems = self.getItemListByKBType( ItemTypeEnum.BAG_EQUIP)
		equipItems = [ k for k in equipItems if k.getHardiness() > 0 and k.getEquipPart() in ItemTypeEnum.EQUIP_ARMOR ]	# 只取防具
		if len(equipItems) == 0:
			return
		for equip in equipItems:
			self.reduceHardiness( equip,-int(damageValue/len(equipItems)))
	
	#-----------------------------关系规则---------------------------------
	def setSpaceRelationRule( self, rule ):
		"""
		define method
		设置地图关系规则
		"""
		if self.spaceRelationRule == rule:
			return
		oldRelRule = self.getRelationRule()
		self.spaceRelationRule = rule
		newRelRule = self.getRelationRule()
		if oldRelRule != newRelRule:
			self.onRelationRuleChange( oldRelRule, newRelRule )
	
	def setAreaRelationRuleFC( self, srcEntityID, rule ):
		"""
		exposed method
		设置区域关系规则
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		rule = int(rule)
		if self.areaRelationRule == rule:
			return
		oldRelRule = self.getRelationRule()
		self.areaRelationRule = rule
		newRelRule = self.getRelationRule()
		if oldRelRule != newRelRule:
			self.onRelationRuleChange( oldRelRule, newRelRule )
		KBEDebug.DEBUG_MSG("Player(%s) area relation rule change.newRule:%s."%(self.id, self.areaRelationRule))
	
	def onRelationRuleChange( self, oldRelRule, newRelRule ):
		"""
		关系规则改变
		"""
		if self.getLevel() >= csconst.PK_PROTECT_LEVEL:
			if newRelRule != csdefine.ROLE_RELATION_RULE_PKMODE and not self.pkModeIsLodked():		#解锁pk模式
				self.lockPkMode()
			elif newRelRule == csdefine.ROLE_RELATION_RULE_PKMODE and self.pkModeIsLodked():		#锁定pk模式
				self.unLockPkMode()
		self.updateKvReduceTimer()
		self.updateRelation()
	
	def getRelationRule( self ):
		"""
		获取当前有效的关系规则
		"""
		if self.areaRelationRule != 0:
			return self.areaRelationRule
		return self.spaceRelationRule
	
	#-----------------------------pk模式----------------------------------
	def setPkModeFC( self, srcEntityID, mode ):
		"""
		exposed method
		客户端设置pk模式
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.pkMode == mode:
			return
		if self.getLevel() < csconst.PK_PROTECT_LEVEL:
			return
		if self.pkModeIsLodked():
			return
		if self.getState() == csdefine.ENTITY_STATE_PEAD:
			return
		if self.getState() == csdefine.ENTITY_STATE_FIGHT:
			return
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		self.setPkMode( mode )
	
	def setPkMode( self, mode ):
		"""
		设置pk模式
		"""
		if self.pkMode == mode:
			return
		self.pkMode = mode
		self.updateKvReduceTimer()
		self.updateRelation()
	
	def getPkModeRelation( self, targetPlayer ):
		"""
		pk模式决定的关系
		"""
		if self.id == targetPlayer.id:
			return csdefine.COMBAT_RELATION_NORMAL

		# 如果玩家小于30级时,新手保护
		if targetPlayer.getLevel() < csconst.PK_PROTECT_LEVEL:
			return csdefine.COMBAT_RELATION_NORMAL

		#处于切磋状态
		
		#一对切磋对手 当都处于COMPETE_FIRE(切磋中)状态时，返回战斗关系 否则返回友好关系
		if self.competeTargetID == targetPlayer.id:
			if self.competeState== csdefine.COMPETE_FIRE and targetPlayer.competeState== csdefine.COMPETE_FIRE:
				return csdefine.COMBAT_RELATION_ENEMY
			else:
				return csdefine.COMBAT_RELATION_NORMAL
		
		#接受切磋邀请后 可以被第三方攻击
		if self.competeState != csdefine.COMPETE_NONE:
			if targetPlayer.pkMode == csdefine.PK_MODE_SLAUGHTER:
				return csdefine.COMBAT_RELATION_ENEMY
			if targetPlayer.pkMode == csdefine.PK_MODE_CAMP:
				campRelation = self.getCampRelation( self.getFinalCamp(), targetPlayer.getFinalCamp() )
				if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
					return campRelation
		
		if targetPlayer.competeState != csdefine.COMPETE_NONE:
			if self.pkMode == csdefine.PK_MODE_SLAUGHTER:
				return csdefine.COMBAT_RELATION_ENEMY
			if self.pkMode == csdefine.PK_MODE_CAMP:
				campRelation = self.getCampRelation( self.getFinalCamp(), targetPlayer.getFinalCamp() )
				if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
					return campRelation

		# 和平模式
		if self.pkMode == csdefine.PK_MODE_PEACE:
			if targetPlayer.id in self.damageList:
				return csdefine.COMBAT_RELATION_ENEMY
			return csdefine.COMBAT_RELATION_NORMAL
		
		# 阵营模式
		elif self.pkMode == csdefine.PK_MODE_CAMP:
			if targetPlayer.pkMode == csdefine.PK_MODE_PEACE:
				return csdefine.COMBAT_RELATION_NORMAL
			if targetPlayer.id in self.damageList:
				return csdefine.COMBAT_RELATION_ENEMY
			campRelation = self.getCampRelation( self.getFinalCamp(), targetPlayer.getFinalCamp() )
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
		
		# 正义模式
		elif self.pkMode == csdefine.PK_MODE_RIGHTFUL:
			if targetPlayer.killingValue >= csconst.KV_ORANGE_NAME or targetPlayer.id in self.damageList:
				return csdefine.COMBAT_RELATION_ENEMY
			else:
				return csdefine.COMBAT_RELATION_NORMAL
		
		# 恶意模式
		elif self.pkMode == csdefine.PK_MODE_SLAUGHTER:
			return csdefine.COMBAT_RELATION_ENEMY

		return csdefine.COMBAT_RELATION_DEFAULT
	
	#--------------------------pk模式锁定----------------------------------
	def lockPkMode( self ):
		"""
		锁定pk模式
		"""
		self.isLockPkMode = True
	
	def unLockPkMode( self ):
		"""
		解锁pk模式
		"""
		self.isLockPkMode = False
	
	def pkModeIsLodked( self ):
		"""
		是否锁定pk模式
		"""
		return self.isLockPkMode
	
	def updatePkModeOnLevelChange( self, oldLevel ):
		"""
		等级改变尝试解锁pk模式
		"""
		if oldLevel < csconst.PK_PROTECT_LEVEL and self.getLevel() >= csconst.PK_PROTECT_LEVEL:
			self.unLockPkMode()
		elif oldLevel >= csconst.PK_PROTECT_LEVEL and self.getLevel() < csconst.PK_PROTECT_LEVEL:
			self.lockPkMode()
			self.setPkMode( csdefine.PK_MODE_PEACE )
	
	#---------------------------杀气值-------------------------------------
	def addKillingValue( self, value ):
		"""
		define method
		增加杀气值
		"""
		if value <= 0:
			return
		oldValue = self.killingValue
		self.killingValue += value
		self.updateKvReduceTimer()
		
		if oldValue < csconst.KV_MORE_GO_JAIL and self.killingValue >= csconst.KV_MORE_GO_JAIL:
			self.gotoSpaceUE4( csconst.JAIL_SCRIPTID, csconst.JAIL_ENTER_POS, csconst.JAIL_ENTER_DIR )
		
		#添加日志
		g_logger.roleKillingChangeLog(self.playerDBID, self.getName(), oldValue, self.killingValue)
	
	def reduceKillingValue( self, value ):
		"""
		减少杀气值
		"""
		if value <= 0 or self.killingValue == 0:
			return
		oldValue = self.killingValue
		self.killingValue = max( self.killingValue - value, 0 )
		self.updateKvReduceTimer()
		
		#添加日志
		g_logger.roleKillingChangeLog(self.playerDBID, self.getName(), oldValue, self.killingValue)
	
	def getKvPlusValue( self, srcValue ):
		"""
		计算杀气值掉耐久
		"""
		if self.killingValue >= csconst.KV_RED_NAME:		#红名玩家
			return srcValue * ( 1 + csconst.HARDINESS_VALUE_RED_NAME )
		elif self.killingValue >= csconst.KV_ORANGE_NAME:	#橙名玩家
			return srcValue * ( 1 + csconst.HARDINESS_VALUE_ORANGE_NAME )
		else:
			return srcValue
	
	#---------------------------杀气值衰减Timer-------------------------------------
	def startKvReduceTimer( self ):
		"""
		开启杀气值衰减Timer
		"""
		if not self.kvReduceTimer:
			self.kvReduceTimer = self.addTimerRepeat( csconst.KV_REDUCE_TICK, "kvReduceTimerCB", () )
	
	def stopKvReduceTimer( self ):
		"""
		关闭杀气值衰减Timer
		"""
		if self.kvReduceTimer:
			self.popTimer( self.kvReduceTimer )
			self.kvReduceTimer = 0
	
	def kvReduceTimerCB( self ):
		"""
		杀气值衰减timer回调
		"""
		self.reduceKillingValue( self.kvDecayRate )
	
	def updateKvReduceTimer( self ):
		"""
		重启或停止杀气值衰减Timer
		"""
		if self.killingValue <= 0:
			self.stopKvReduceTimer()
			return
		
		if len( self.findEnemyByEntityType( csdefine.ENTITY_FLAG_ROLE ) ) > 0 and self.getRelationRule() == csdefine.ROLE_RELATION_RULE_PKMODE and self.pkMode == csdefine.PK_MODE_SLAUGHTER:
			self.stopKvReduceTimer()
			return
		
		if self.isState( csdefine.ENTITY_STATE_DEAD ):
			self.stopKvReduceTimer()
			return
		
		self.startKvReduceTimer()

	#---------玩家战斗属性计算------------------------------------------------------------------------
	def calcAttachProperties( self, reason = csdefine.CALC_COMBAT_POWER_REASON_DEFAULT ):
		"""
		重新计算玩家战斗属性
		"""		
		oldHP = self.HP
		oldHP_Max = self.HP_Max
		oldMP = self.MP
		oldMP_Max = self.MP_Max
		oldGangQiValue_Max = self.gangQiValue_Max
		self.calcBasicProperties()
		self.calcLVOneProperties()
		self.calcLVTwoProperties()
		self.calcTempSpeedProperties()
		self.calcResultProperties()		

		#调用对应的RoleCombatInterface和MonsterCombatInterface中的updateBornHPMP方法
		self.updateHPMPByPercent(oldHP,oldHP_Max,oldMP,oldMP_Max)
		self.updateGangQiMaxValue( oldGangQiValue_Max )
		#在重新计算属性之后要设置实际的移动速度
		self.initSpeed()
		self.calcCombatPower()
		
	def onCombatPowerChange(self, oldCombatPower, reason):
		"""
		战斗力改变
		"""
		if oldCombatPower == self.combatPower:
			return
		if self.isShowCombatPowerChange and reason in csconst.COMBAT_POWER_CHANGE_REASONS:
			self.client.CLIENT_ShowCombatPowerChangeTips(self.combatPower, self.combatPower - oldCombatPower)

	def calcTempSpeedProperties(self):
		"""
		重新计算临时速度属性
		"""
		propertystr = ItemTypeEnum.PROPERTYIDTOSTR[ItemTypeEnum.TEMPSPEED]
		basevalue = self.queryTemp("tempSpeedBase",0)
		vvalue = self.tempSpeed_value
		precentvalue = self.tempSpeed_percent
		result = CombatInterface.calcProperty(basevalue, 0, precentvalue, vvalue )
		if self.tempSpeed != int( result ):
			self.tempSpeed = int(result)

	def calcCombatPower(self):
		"""
		重新计算战斗力
		"""
		M1 = self.getRolePropertyFactor()	
		M2 = 0.0
		if self.profession in csconst.PROFESSION_CORRECTION_FACTOR:
			M2 = self.getProfessionCorrectoin().get(self.profession, 0.0)
		self.combatPower = int(round((M1-M2)/50))	

#---------------------- timer --------------------------
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		CombatInterface.CombatInterface.timerValeDelCB( self, timerArg )


#--------------------连击处理---------------------------------
	def onStartDoubleHit(self, times = 1):
		"""
		开始连击
		"""
		if self.doubleHitTimer:
			self.popTimer(self.doubleHitTimer)
			self.doubleHitTimer = 0
		self.doubleHitTimes += times
		doubleHitState = csconst.DOUBLE_HIT_STATE.get(self.doubleHitTimes, 0)
		if doubleHitState:
			self.doubleHitState = doubleHitState
			removeEffectID = csconst.DOUBLE_HIT_EFFECT.get(self.doubleHitState - 1, 0)
			if removeEffectID:
				self.removeFixIDHoldEffectByID( removeEffectID )
			self.addFixIDHoldEffect( csconst.DOUBLE_HIT_EFFECT[self.doubleHitState], self )

		delayTime = csconst.DOUBLE_HIT_TIME.get(self.doubleHitState, 5.0)
		self.doubleHitTimer = self.addTimerCallBack(delayTime, "onEndDoubleHit", ())
		try:
			self.client.CLIENT_OnDoubleHit(self.doubleHitTimes)
		except:
			pass

	def onEndDoubleHit(self):
		"""
		结束连击
		"""
		self.doubleHitTimes = 0
		if self.doubleHitState:
			self.removeFixIDHoldEffectByID( csconst.DOUBLE_HIT_EFFECT[self.doubleHitState])
			self.doubleHitState = 0
			
		try:
			self.client.CLIENT_OnDoubleHit(self.doubleHitTimes)
		except:
			pass

	def onStartBeDoubleHit(self, times = 1):
		"""
		开始被连击
		"""
		if self.beDoubleHitTimer:
			self.popTimer(self.beDoubleHitTimer)
			self.beDoubleHitTimer = 0
		self.beDoubleHitTimes += times
		beDoubleHitState = csconst.DOUBLE_HIT_STATE.get(self.beDoubleHitTimes, 0)
		if beDoubleHitState:
			self.beDoubleHitState = beDoubleHitState
			removeEffectID = csconst.DOUBLE_BE_HIT_EFFECT.get(self.beDoubleHitState - 1, 0)
			if removeEffectID:
				self.removeFixIDHoldEffectByID( removeEffectID )
			self.addFixIDHoldEffect( csconst.DOUBLE_BE_HIT_EFFECT[self.beDoubleHitState], self )

		delayTime = csconst.DOUBLE_HIT_TIME.get(self.beDoubleHitState, 5.0)
		self.beDoubleHitTimer = self.addTimerCallBack(delayTime, "onEndBeDoubleHit", ())

	def onEndBeDoubleHit(self):
		"""
		结束被连击
		"""
		self.beDoubleHitTimes = 0
		if self.beDoubleHitState:
			self.removeFixIDHoldEffectByID( csconst.DOUBLE_BE_HIT_EFFECT[self.beDoubleHitState])
			self.beDoubleHitState = 0

#-------------------------被动技能栏----------------------------------------------
	def initPassiveSkillsBar(self):
		"""
		初始化被动技能栏
		"""
		if len(self.passiveSkillsBar) > 0: return
		datas = g_passiveSkillBars.getDatas()
		for data in datas.values():
			self.passiveSkillsBar.adSkillBarData(data)

	def requestUnlockPassiveSkillBar(self, srcEntityID, index):
		"""
		Exposed method
		解锁被动技能栏栏位
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		#自己前面一个栏位是否已经解锁
		skillBar = self.passiveSkillsBar.get((index-1), None)
		if skillBar and skillBar["isLock"]:return
		
		#当前栏位是否已经解锁
		skillBar = self.passiveSkillsBar.get(index, None)
		if not skillBar or not skillBar["isLock"]:return
		
		data = g_passiveSkillBars.getItem(index)
		if not data:
			KBEDebug.ERROR_MSG("Not found passiveSkillsBar config. id[%d]" %(index))
			return
		
		if self.level < data["level"]:
			self.statusMessage(csstatus.PASSIVESKILLBAR_LEVEL_LOW)
			return
		
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY] = data["money"]
		payItems[csdefine.TRADE_PAY_ITEM_XIANSHI] = data["xianshi"]
		payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = data["material"]
		self.requestPay( csdefine.TRADE_TYPE_UNLOCK_PASSIVESKILLBAR, 0, payItems, index )
		
	def onUnLockPassiveSkillBar( self, order, index ):
		"""
		"""
		self.passiveSkillsBar[index]["isLock"] = 0
		self.client.updatePassiveSkillBar(self.passiveSkillsBar[index])
		
	def requestActivatePassiveSkill(self, srcEntityID, skillID, index):
		"""
		Exposed method
		激活被动技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		dstSkillBar = self.passiveSkillsBar.get(index, None)
		if not dstSkillBar or dstSkillBar["isLock"]: return
		
		#技能本来就在指定的位置上
		dstSkill = dstSkillBar["skillID"]
		if dstSkill == skillID: return
		
		#没有学习该技能或不是被动技能
		if skillID not in self.attrSkills: return
		skillData = self.getSkill(skillID)
		if not skillData.isPassiveSkill(): return
		
		srcIndex = 0
		for i in range(1, len(self.passiveSkillsBar)):
			if i not in self.passiveSkillsBar: break
			#判断当前技能是否已在被动技能栏中（已激活）
			if self.passiveSkillsBar[i]["skillID"] == skillID:
				srcIndex = i
				break
		
		self.passiveSkillsBar[index]["skillID"] = skillID
		self.client.updatePassiveSkillBar(self.passiveSkillsBar[index])
		
		#skillID本来就已经在技能栏中了（已激活）
		if srcIndex:
			self.passiveSkillsBar[srcIndex]["skillID"] = dstSkill
			self.client.updatePassiveSkillBar(self.passiveSkillsBar[srcIndex])
		else:
			if dstSkill: self.sleepPassiveSkill(dstSkill)
			self.activatePassiveSkill(skillID)
			
	def requestCancelUnActivatePassiveSkill(self, srcEntityID, index):
		"""
		Exposed method
		取消被动技能放置
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		skillBar = self.passiveSkillsBar.get(index, None)
		if not skillBar or skillBar["isLock"]: return
		
		#没有技能在指定的位置上
		if not skillBar["skillID"]: return
		skillID = self.passiveSkillsBar[index]["skillID"]
		self.passiveSkillsBar[index]["skillID"] = 0
		self.client.updatePassiveSkillBar(self.passiveSkillsBar[index])
		self.sleepPassiveSkill(skillID)
# -*- coding: utf-8 -*-


#engine
import KBEngine
#script
import traceback
import KST
import csconst
import csstatus
import csdefine
import CoreObject.GameObject as GameObject
import KBEDebug
import time
import random
import json
import Const
import Define
import Functions
import Settings
import ItemTypeEnum
import ECBProximityDefine
import ItemSystemExp
from ItemFactory import ItemFactoryInst
from RoleBornPropertyLoader import g_roleBornProLoader
from ObjectScript.ObjectScriptFactory import g_objFactory
from MsgLogger import g_logger
from ConfigObject.SpaceEntityRelation.SpaceEntityRelationLoader import g_spaceEntityRelationLoader

import ImpInterface.RoleTitleInterface as RoleTitleInterface
import CoreInterface.RoleKitBagInterface as RoleKitBagInterface
import CoreInterface.RoleSpaceInterface as RoleSpaceInterface
import CoreInterface.RoleChatInterface as RoleChatInterface
import CoreInterface.RoleTalkInterface as RoleTalkInterface
import CoreInterface.RoleModelInterface as RoleModelInterface
import CoreInterface.RoleRelationInterface as RoleRelationInterface
import CoreInterface.RoleTeamInterface as RoleTeamInterface
import CoreInterface.RoleQuestInterface as RoleQuestInterface
import CoreInterface.RoleCombatInterface as RoleCombatInterface
import CoreInterface.RoleUpgradeInterface as RoleUpgradeInterface
import CoreInterface.RoleEquipInterface as RoleEquipInterface
import CoreInterface.RoleReviveInterface as RoleReviveInterface
import CoreInterface.RoleBuyNPCShopInterface as RoleBuyNPCShopInterface
import CoreInterface.RoleActRecordInterface as RoleActRecordInterface
import ImpInterface.RoleActivityInterface as RoleActivityInterface
import CoreInterface.RolePerformanceInterface as RolePerformanceInterface
import CoreInterface.RoleTradeInterface as RoleTradeInterface
import CoreInterface.TradeInterface as TradeInterface
import CoreInterface.TestInterface as TestInterface
import CoreInterface.RoleStallInterface as RoleStallInterface
import CoreInterface.RoleMemoirInterface as RoleMemoirInterface
import CoreInterface.RoleShopMallInterface as RoleShopMallInterface
import CoreInterface.RoleFacadeBagInterface as RoleFacadeBagInterface
import CoreInterface.RoleLingShiTradeInterface as RoleLingShiTradeInterface
import CoreInterface.RoleCallEntityInterface as RoleCallEntityInterface
import CoreInterface.RolePetInterface as RolePetInterface
import CoreInterface.RoleAmbulantInterface as RoleAmbulantInterface
import CoreInterface.RoleTeleportInterface as RoleTeleportInterface
import CoreInterface.RoleTutorialInterface as RoleTutorialInterface
import CoreInterface.RoleTutorialInterface as RoleTutorialInterface
import CoreInterface.RoleTongInterface as RoleTongInterface
import CoreInterface.RoleDropBoxInterface as RoleDropBoxInterface
import CoreInterface.RoleDropBoxInterface as RoleDropBoxInterface
import CoreInterface.SkillInterface as SkillInterface

import ImpInterface.EntitySpaceEventInterface as EntitySpaceEventInterface
import ImpInterface.RoleSpaceStageInterface as RoleSpaceStageInterface
import ImpInterface.StatusMessageInterface as StatusMessageInterface
import ImpInterface.RoleStoryInterface as RoleStoryInterface
import ImpInterface.RoleGiftInterface as RoleGiftInterface
import ImpInterface.RoleRankInterface as RoleRankInterface
import ImpInterface.GMToolsInterface as GMToolsInterface

import ImpInterface.RoleSpaceSettlementInterface as RoleSpaceSettlementInterface
import ImpInterface.RoleSpaceStrategyInterface as RoleSpaceStrategyInterface
import CoreInterface.AntiWallow as AntiWallow
import CoreInterface.RoleSpaceContentInterface as RoleSpaceContentInterface
import CoreInterface.RoleMailInterface as RoleMailInterface
import CoreInterface.EntityDataValidateInterface as EntityDataValidateInterface
import CoreInterface.RoleQTEInterface as RoleQTEInterface
import CoreInterface.RoleCompeteInterface as RoleCompeteInterface
import CoreInterface.RoleCampInterface as RoleCampInterface
import CoreInterface.PresentChargeUnite as PresentChargeUnite
import CoreInterface.RolePointCardInterface as RolePointCardInterface
import CoreInterface.SystemSwitchInterface as SystemSwitchInterface
import CoreInterface.RoleShenTongInterface as RoleShenTongInterface
import CoreInterface.RoleStoreInterface as RoleStoreInterface
import CoreInterface.RoleSpellBoxDropItemInterface as RoleSpellBoxDropItemInterface
import ImpInterface.RoleCommanderInterface as RoleCommanderInterface
import ImpInterface.RoleLunHuiMiJinInterface as RoleLunHuiMiJinInterface
import CoreInterface.RoleBarracksInterface as RoleBarracksInterface
import ImpInterface.RoleMilitaryRankInterface as RoleMilitaryRankInterface
import ImpInterface.RoleWorkShopInterface as RoleWorkShopInterface
import ImpInterface.RoleLbcInterface as RoleLbcInterface
import CoreInterface.RoleTrainSoldierGroundInterface as RoleTrainSoldierGroundInterface
import CoreInterface.RoleLBCTaskInterface as RoleLBCTaskInterface
import CoreInterface.RoleFixedUpdateInterface as RoleFixedUpdateInterface
import CoreInterface.RoleChuanChengInterface as RoleChuanChengInterface
import CoreInterface.RoleAutoFightInterface as RoleAutoFightInterface

class Role(
	GameObject.GameObject,
	EntityDataValidateInterface.EntityDataValidateInterface,
	StatusMessageInterface.StatusMessageInterface,
	RoleKitBagInterface.RoleKitBagInterface,
	RoleSpaceInterface.RoleSpaceInterface,
	RoleChatInterface.RoleChatInterface,
	RoleTalkInterface.RoleTalkInterface,
	RoleModelInterface.RoleModelInterface,
	RoleRelationInterface.RoleRelationInterface,
	RoleTeamInterface.RoleTeamInterface,
	RoleQuestInterface.RoleQuestInterface,
	RoleCombatInterface.RoleCombatInterface,
	RoleUpgradeInterface.RoleUpgradeInterface,
	EntitySpaceEventInterface.EntitySpaceEventInterface,
	RoleEquipInterface.RoleEquipInterface,
	RoleReviveInterface.RoleReviveInterface,
	RoleSpaceStageInterface.RoleSpaceStageInterface,
	RoleBuyNPCShopInterface.RoleBuyNPCShopInterface,
	RoleActRecordInterface.RoleActRecordInterface,
	RoleActivityInterface.RoleActivityInterface,
	RolePerformanceInterface.RolePerformanceInterface,
	RoleTradeInterface.RoleTradeInterface,
	TradeInterface.TradeInterface,
	RoleStoryInterface.RoleStoryInterface,
	TestInterface.TestInterface,
	RoleStallInterface.RoleStallInterface,
	RoleMemoirInterface.RoleMemoirInterface,
	RoleShopMallInterface.RoleShopMallInterface,
	RoleFacadeBagInterface.RoleFacadeBagInterface,
	RoleLingShiTradeInterface.RoleLingShiTradeInterface,
	RoleCallEntityInterface.RoleCallEntityInterface,
	RolePetInterface.RolePetInterface,
	RoleAmbulantInterface.RoleAmbulantInterface,
	RoleTitleInterface.RoleTitleInterface,
	RoleSpaceSettlementInterface.RoleSpaceSettlementInterface,
	RoleTeleportInterface.RoleTeleportInterface,
	RoleTutorialInterface.RoleTutorialInterface,
	RoleTongInterface.RoleTongInterface,
	RoleDropBoxInterface.RoleDropBoxInterface,
	RoleSpaceStrategyInterface.RoleSpaceStrategyInterface,
	#AntiWallow.AntiWallow,
	RoleSpaceContentInterface.RoleSpaceContentInterface,
	RoleMailInterface.RoleMailInterface,
	RoleGiftInterface.RoleGiftInterface,
	RoleRankInterface.RoleRankInterface,
	RoleQTEInterface.RoleQTEInterface,
	RoleCompeteInterface.RoleCompeteInterface,
	RoleCampInterface.RoleCampInterface,
	GMToolsInterface.GMToolsInterface,
	PresentChargeUnite.PresentChargeUnite,
	RolePointCardInterface.RolePointCardInterface,
	SystemSwitchInterface.SystemSwitchInterface,
	RoleShenTongInterface.RoleShenTongInterface,
	RoleStoreInterface.RoleStoreInterface,
	RoleSpellBoxDropItemInterface.RoleSpellBoxDropItemInterface,
	RoleCommanderInterface.RoleCommanderInterface,
	RoleLunHuiMiJinInterface.RoleLunHuiMiJinInterface,
	RoleBarracksInterface.RoleBarracksInterface,
	RoleMilitaryRankInterface.RoleMilitaryRankInterface,
	RoleWorkShopInterface.RoleWorkShopInterface,
	RoleLbcInterface.RoleLbcInterface,
	RoleTrainSoldierGroundInterface.RoleTrainSoldierGroundInterface,
	RoleLBCTaskInterface.RoleLBCTaskInterface,
	RoleFixedUpdateInterface.RoleFixedUpdateInterface,
	RoleChuanChengInterface.RoleChuanChengInterface,
	RoleAutoFightInterface.RoleAutoFightInterface
	):
	def __init__( self ):
		GameObject.GameObject.__init__( self )
		EntityDataValidateInterface.EntityDataValidateInterface.__init__( self )
		RoleKitBagInterface.RoleKitBagInterface.__init__( self )
		RoleSpaceInterface.RoleSpaceInterface.__init__( self )
		RoleChatInterface.RoleChatInterface.__init__( self )
		RoleTalkInterface.RoleTalkInterface.__init__( self )
		RoleModelInterface.RoleModelInterface.__init__( self )
		RoleRelationInterface.RoleRelationInterface.__init__( self )
		RoleTeamInterface.RoleTeamInterface.__init__( self )
		RoleQuestInterface.RoleQuestInterface.__init__( self )
		RoleCombatInterface.RoleCombatInterface.__init__( self )
		RoleUpgradeInterface.RoleUpgradeInterface.__init__( self )
		RoleEquipInterface.RoleEquipInterface.__init__( self )
		RoleReviveInterface.RoleReviveInterface.__init__( self )
		StatusMessageInterface.StatusMessageInterface.__init__( self )
		RoleBuyNPCShopInterface.RoleBuyNPCShopInterface.__init__( self )
		RolePerformanceInterface.RolePerformanceInterface.__init__(self)
		RoleTradeInterface.RoleTradeInterface.__init__( self )
		TradeInterface.TradeInterface.__init__( self )
		TestInterface.TestInterface.__init__(self)
		RoleStallInterface.RoleStallInterface.__init__(self)
		RoleMemoirInterface.RoleMemoirInterface.__init__(self)
		RoleShopMallInterface.RoleShopMallInterface.__init__(self)
		RoleFacadeBagInterface.RoleFacadeBagInterface.__init__(self)
		RoleLingShiTradeInterface.RoleLingShiTradeInterface.__init__(self)
		RoleCallEntityInterface.RoleCallEntityInterface.__init__(self)
		RolePetInterface.RolePetInterface.__init__( self )
		RoleAmbulantInterface.RoleAmbulantInterface.__init__( self )
		RoleTitleInterface.RoleTitleInterface.__init__( self )
		RoleTeleportInterface.RoleTeleportInterface.__init__( self )
		RoleTutorialInterface.RoleTutorialInterface.__init__( self )
		RoleTongInterface.RoleTongInterface.__init__( self )
		RoleDropBoxInterface.RoleDropBoxInterface.__init__( self )
		RoleSpaceStrategyInterface.RoleSpaceStrategyInterface.__init__( self )
		#AntiWallow.AntiWallow.__init__( self )
		RoleSpaceContentInterface.RoleSpaceContentInterface.__init__( self )
		RoleMailInterface.RoleMailInterface.__init__( self )
		RoleQTEInterface.RoleQTEInterface.__init__(self)
		RoleCompeteInterface.RoleCompeteInterface.__init__(self)
		RoleCampInterface.RoleCampInterface.__init__(self)
		GMToolsInterface.GMToolsInterface.__init__(self)
		PresentChargeUnite.PresentChargeUnite.__init__(self)
		RolePointCardInterface.RolePointCardInterface.__init__(self)
		SystemSwitchInterface.SystemSwitchInterface.__init__(self)
		RoleShenTongInterface.RoleShenTongInterface.__init__(self)
		RoleStoreInterface.RoleStoreInterface.__init__(self)
		RoleSpellBoxDropItemInterface.RoleSpellBoxDropItemInterface.__init__( self )
		RoleCommanderInterface.RoleCommanderInterface.__init__(self )
		RoleBarracksInterface.RoleBarracksInterface.__init__( self )
		RoleMilitaryRankInterface.RoleMilitaryRankInterface.__init__( self )
		RoleWorkShopInterface.RoleWorkShopInterface.__init__( self )
		RoleLbcInterface.RoleLbcInterface.__init__(self)
		RoleActivityInterface.RoleActivityInterface.__init__( self )
		RoleTrainSoldierGroundInterface.RoleTrainSoldierGroundInterface.__init__( self )
		RoleLBCTaskInterface.RoleLBCTaskInterface.__init__(self)
		RoleFixedUpdateInterface.RoleFixedUpdateInterface.__init__(self)
		RoleChuanChengInterface.RoleChuanChengInterface.__init__(self)
		RoleAutoFightInterface.RoleAutoFightInterface.__init__(self)
		
	def onInit(self):
		"""
		"""
		self.isShowCombatPowerChange = True
			
	def doEnterSpace( self ):
		"""
		KBEngine callback
		进入一个空间调用
		"""
		GameObject.GameObject.doEnterSpace( self )
		RoleSpaceInterface.RoleSpaceInterface.doEnterSpace( self )
		RoleCombatInterface.RoleCombatInterface.doEnterSpace( self )

	def doLeaveSpace( self ):
		"""
		KBEngine callback
		离开一个空间调用（在doEnterSpace之后）
		"""
		GameObject.GameObject.doLeaveSpace( self )
		RoleSpaceInterface.RoleSpaceInterface.doLeaveSpace( self )
		RoleCombatInterface.RoleCombatInterface.doLeaveSpace( self )

	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_ROLE )
		
	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_ROLE)

	def onClientGetCell( self ):
		"""
		<define method>
		"""
		# 阵营气运值
		KBEngine.globalData["CampMgr"].queryCampMorale( self.base, self.getCamp() )
		RoleTrainSoldierGroundInterface.RoleTrainSoldierGroundInterface.onClientGetCell( self )

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		玩家客户端Character Actor已经准备好
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.isClientReady = 1
		if not len(self.findBuffsByBuffID(csconst.TELEPORT_PROTECT_BUFFID)) and self.state == csdefine.ENTITY_STATE_PEAD:
			self.changeState( csdefine.ENTITY_STATE_FREE )
			self.reTriggerNearTrap()
		

	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		try:
			self.onLeaveSpaceNotify( Define.LEAVE_SPACE_REASON_LOGOUT, "", {} )
			RolePetInterface.RolePetInterface.beforeDestroy( self )
			RoleCombatInterface.RoleCombatInterface.beforeDestroy( self )
			RoleTeamInterface.RoleTeamInterface.beforeDestroy( self )
			RoleRankInterface.RoleRankInterface.beforeDestroy( self )
			GameObject.GameObject.beforeDestroy( self )
			RoleSpellBoxDropItemInterface.RoleSpellBoxDropItemInterface.beforeDestroy(self)
			RoleCommanderInterface.RoleCommanderInterface.beforeDestroy(self)
			RoleLunHuiMiJinInterface.RoleLunHuiMiJinInterface.beforeDestroy( self )
			RoleActivityInterface.RoleActivityInterface.beforeDestroy( self )
			RoleSpaceContentInterface.RoleSpaceContentInterface.beforeDestroy( self )
			RoleDropBoxInterface.RoleDropBoxInterface.beforeDestroy( self )
			#正在交易的玩家下线后需要取消交易
			self.cancelRoleTradeOnLogoff()
			if self.isState( csdefine.ENTITY_STATE_STALL ):
				self.endStall(self.id)
			GMToolsInterface.GMToolsInterface.beforeDestroy( self )
		except Exception as e:
			KBEDebug.ERROR_MSG(traceback.format_exc())

	def isReady( self ):
		"""
		判断entity是否准备好了，在某些情况下（玩家传送界面还没加载好）不让该entity进行触发陷阱，关系建立，不被AI搜索等等
		"""
		if self.state == csdefine.ENTITY_STATE_PEAD or self.isClientReady == 0 or self.hasEffectState( csdefine.EFFECT_STATE_PROTECT ):
			return False
				
		return True

#------------------玩家首次上线---------------------------------------------------------
	def initRoleInfo( self, roleState ):
		"""
		<define method>
		初始化角色
		"""
		if roleState == csdefine.ROLE_STATE_CREATE:
			self.onFirstCreateRole()
		
		self.initClientData(roleState)
		self.onInit()

	def onFirstCreateRole( self ):
		"""
		define method
		对一个角色而言，仅调用一次，在创建玩家后，首次进入游戏
		主要处理首次创建后给玩家任务，道具事议
		"""
		KBEDebug.INFO_MSG( "cell playerDBID[%d] first create!"%self.playerDBID )
		
		#根据配置表初始化相关出生属性
		questID = g_roleBornProLoader.getQuest( self.camp, self.profession, self.gender )
		if questID:
			self.addQuest( questID )
		
		skills = g_roleBornProLoader.getSkills( self.camp, self.profession, self.gender )
		for skillID in skills:
			self.attrSkills.append(skillID)
		
		items = g_roleBornProLoader.getItems( self.camp, self.profession, self.gender )
		for itemInfo in items:
			itemInst = ItemFactoryInst.createDynamicItem( itemInfo[0], itemInfo[1] )
			if not itemInst:
				KBEDebug.ERROR_MSG( "Born item config error!", itemInfo[0], itemInfo[1] )
				continue
			statusID = self.addItem( itemInst, csdefine.ITEM_ADD_BY_BORN_GAIN )
			if statusID == csstatus.ITEM_GO_ON and itemInst.isEquip():
				self.CELL_swapItem( self.id, itemInst.order, itemInst.getEquipPart() )

		#策划要求首次创建的角色进入游戏是满血满蓝
		self.setHP( self.HP_Max )
		self.setMP( self.MP_Max )
		self.base.onFirstCreateRoleCB()

	def initClientData( self, roleState):
		# 玩家成功登陆后，把任务事件注册到任务事件管理器
		RoleLunHuiMiJinInterface.RoleLunHuiMiJinInterface.initClientData( self )
		self.initQuest()
		# 发送任务数据
		self.sendQuestDataToClient()
		# 初始化技能列表
		self.initSkills()
		# 初始化神通技能列表
		self.initShenTongSKill()
		# 初始化传承技能列表
		self.initChuanChengSKill()
		# 更新技能冷却时间数据到客户端
		self.initCooldownToClient()
		# 初始化背包物品
		self.initKitBagItems(roleState)
		#初始化快捷栏
		self.base.initClientData()
		#初始化聊天数据
		self.initChatDatas()
		#初始化回购数据
		self.initBuyBackItemList()
		#上线重新计算buff数据
		self.roleCalculateBuffsOnInit()
		#上线重新发送称号数据
		self.sendAvailableTitleData()
		self.sendTitleData()
		#初始化心法状态并通知客户端显示
		self.initSkillPosture()
		#初始化商城外观通知客户端显示
		self.initStoreAppearance()
		#玩家登录相关
		self.roleLbcLogin()
#----------------------基础属性--------------------------------------------------
	def getName( self ):
		"""
		virtual method
		获取名称
		"""
		return self.playerName
		
	def getGender( self ):
		"""
		获取性别
		"""
		return self.gender
		
	def getProfession( self ):
		"""
		获取职业
		"""
		return self.profession

#----------------------阵营----------------------------------------------------
	def getCamp( self ):
		"""
		获取阵营
		"""
		return self.camp

	def setTempCamp( self, newCamp ):
		"""
		设置临时阵营
		改变阵营玩法 CST-2129
		"""
		oldCamp = self.tempCamp
		self.tempCamp = newCamp
		self.onTempCampChange( oldCamp, self.tempCamp )

	def onTempCampChange(  self, oldCamp, newCamp ):
		"""
		临时阵营改变
		"""
		self.updateRelation()

	def getFinalCamp( self ):
		"""
		获取最终阵营：有临时阵营则返回临时阵营，否则返回原阵营
		"""
		if self.tempCamp:
			return self.tempCamp
		return self.camp

#---------------------------------------------------------------------------
	def onPlayerUnderArea( self, srcEntityID ):
		"""
		<Expose method>
		玩家跌落到死亡深度后的通知
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if self.state == csdefine.ENTITY_STATE_DEAD:
			return

		spaceScriptID = self.getCurrentSpaceScriptID()
		if spaceScriptID in Const.MAZE_SPACE_SCRIPTID:
			self.onMagicMazeFallDown()
			return
		self.changeState(csdefine.ENTITY_STATE_DEAD)
		KBEDebug.DEBUG_MSG( "Player(%s) die when reaching death depth!"%self.id )
	
	def onEnterDead( self ):
		"""
		死亡
		"""
		RoleCombatInterface.RoleCombatInterface.onEnterDead( self )
		RoleReviveInterface.RoleReviveInterface.onEnterDead( self )
		RoleTeamInterface.RoleTeamInterface.onEnterDead( self )
		RolePetInterface.RolePetInterface.onEnterDead( self )
		RoleTradeInterface.RoleTradeInterface.onEnterDead( self )
		RoleCommanderInterface.RoleCommanderInterface.onEnterDead(self)
		RoleSpaceContentInterface.RoleSpaceContentInterface.onEnterDead(self)
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.remoteScriptCall( "onPlayerDie", ( self.id, self.base ) )

	
	def onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry ):
		"""
		virtual method
		接受伤害回调
		"""
		RoleCombatInterface.RoleCombatInterface.onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )
		RoleCompeteInterface.RoleCompeteInterface.onReceiveDamage(self)
		RoleSpaceSettlementInterface.RoleSpaceSettlementInterface.onReceiveDamage( self, finalDamage )
		RoleSpaceStrategyInterface.RoleSpaceStrategyInterface.spaceStrategy_onReceiveDamage( self, casterID )
	
	def effectStateChanged( self, estate, disabled ):
		"""
		效果改变.
			@param estate		:	效果标识(非组合)
			@type estate		:	integer
			@param disabled		:	效果是否生效
			@param disabled		:	bool
		"""
		RoleCombatInterface.RoleCombatInterface.effectStateChanged( self, estate, disabled )
		RoleTeamInterface.RoleTeamInterface.effectStateChanged( self, estate, disabled )
		
	def onActionForbid( self, actForbid ):
		"""
		行为禁止时
		"""
		RoleCombatInterface.RoleCombatInterface.onActionForbid( self, actForbid )
		RolePetInterface.RolePetInterface.onActionForbid(self, actForbid )
	
	def onFlagChange( self, oldFlags, newFlags ):
		"""
		virtual method
		标志位改变
		"""
		GameObject.GameObject.onFlagChange( self, oldFlags, newFlags )
		self.updateRelation()
	
#----------------------关系-----------------------------------------------
	def getEntityRelationIns( self ):
		"""
		virtual method
		获取关系判断实例
		"""
		if not self.getRelationRule():
			return None
		clsStr = csconst.ROLE_RELATION_RULE_TO_REL_CLS[ self.getRelationRule() ]	#根据关系规则获取关系判断实例
		return g_spaceEntityRelationLoader.getRelationInsByCls( clsStr )
	
	def updateRelation( self ):
		"""
		virtual method
		关系改变
		"""
		GameObject.GameObject.updateRelation( self )
		RoleCombatInterface.RoleCombatInterface.updateRelation(self)

#-------------------敌人列表改动----------------------------------------------------------------------------------
	def onAddEnemy( self, enemyID ):
		"""
		"""
		RoleCombatInterface.RoleCombatInterface.onAddEnemy( self, enemyID )
		RoleCallEntityInterface.RoleCallEntityInterface.onAddEnemy( self, enemyID )
		RolePetInterface.RolePetInterface.onAddEnemy( self, enemyID )

	def onRemoveEnemy( self, enemyID ):
		"""
		"""
		RoleCombatInterface.RoleCombatInterface.onRemoveEnemy( self, enemyID )
		RoleCallEntityInterface.RoleCallEntityInterface.onRemoveEnemy( self, enemyID )

#--------------------------空间传送相关方法及时刻-----------------------------------------------------------------
	def loadSpaceCompleted( self, srcEntityID, isFirst ):
		"""
		<Exposed method>
		玩家进入游戏场景，客户端角色和Actor已经创建成功
		isFirst: 1  首次，0非首次
		"""
		KBEDebug.DEBUG_MSG("------------------loadSpaceCompleted-------%d-------------"%isFirst)
		RoleSpaceInterface.RoleSpaceInterface.onTeleportCompleted( self )
		RoleTeamInterface.RoleTeamInterface.onTeleportCompleted( self, isFirst )
		RolePetInterface.RolePetInterface.onTeleportCompleted( self )
		RoleReviveInterface.RoleReviveInterface.onTeleportCompleted( self, isFirst )
		RoleCallEntityInterface.RoleCallEntityInterface.onTeleportCompleted(self)
		RoleDropBoxInterface.RoleDropBoxInterface.onTeleportCompleted(self, isFirst)
		if isFirst:
			self.initMemoirList()
		self.isInPending = 0

#----------------------金币接口---------------------------
	def getMoney( self ):
		"""
		返回金币
		"""
		return self.money

	def isAddMoney( self, amount ):
		"""
		判断能否增加金币
		"""
		if csconst.MONEY_MAX_AMOUNT < self.money + amount:
			return False

		return True

	def addMoney( self, amount, reason, order = "" ):
		"""
		增加金币
		"""
		if amount == 0:
			return
		if not self.isAddMoney( amount ):
			self.statusMessage( csstatus.ACCOUNT_CANT_GAIN_MONEY,"")
			return False
			
		self.money += amount
		self.statusMessage( csstatus.ACCOUNT_STATE_GAIN_MONEY, Functions.moneyToStr(amount) )
		#添加日志
		g_logger.moneyChangeLog( self.accountDBID, self.playerDBID, self.getName(), self.money - amount, self.money, reason, order)
		return True

	def subMoney( self, amount, reason, order = "" ):
		"""
		减少金币
		"""
		if amount == 0:
			return True
		if self.money < amount:
			return False
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		self.money -= amount
		self.statusMessage( csstatus.ACCOUNT_STATE_LOSE_MONEY, Functions.moneyToStr(amount) )
		#添加日志
		g_logger.moneyChangeLog(self.accountDBID, self.playerDBID, self.getName(), self.money + amount, self.money, reason, order)
		return True

	def getBindMoney(self):
		return self.bindMoney

	def isAddBindMoney(self, amount):
		if csconst.MONEY_MAX_AMOUNT < self.bindMoney + amount:
			return False

		return True

	def addBindMoney(self, amount, reason, order = ""):
		if amount == 0:
			return
		if not self.isAddBindMoney(amount):
			self.statusMessage(csstatus.ACCOUNT_CANT_GAIN_BIND_MONEY, "")
			return False

		self.bindMoney += amount
		self.statusMessage(csstatus.ACCOUNT_STATE_GAIN_BIND_MONEY, Functions.bindMoneyToStr(amount))
		# 添加日志
		g_logger.bindMoneyChangeLog(self.accountDBID, self.playerDBID, self.getName(), self.bindMoney - amount, self.bindMoney, reason, order)
		return True

	def subBindMoney(self, amount, reason, order = ""):
		if amount == 0:
			return True
		if self.bindMoney < amount:
			return False
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		self.bindMoney -= amount
		self.statusMessage( csstatus.ACCOUNT_STATE_LOSE_BIND_MONEY, Functions.bindMoneyToStr(amount) )
		#添加日志
		g_logger.bindMoneyChangeLog(self.accountDBID, self.playerDBID, self.getName(), self.bindMoney + amount, self.bindMoney, reason, order)
		return True
		
	def subBindMoneyAndMoney(self, amount, reason, order = ""):
		"""
		混合支付,绑金优先
		"""
		if amount <= 0:
			return True
			
		if self.bindMoney + self.money < amount:
			return False
			
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		
		if self.bindMoney >= amount:
			self.subBindMoney( amount, reason, order)
			return True
			
		amount -= self.bindMoney
		self.subBindMoney(self.bindMoney, reason, order)
		self.subMoney(amount, reason, order)
		return True

#----------------------潜能接口---------------------------
	def addPotential( self, potential, reason = csdefine.POTENTIAL_ADD_REASON_NORMAL ):
		"""
		<define method>
		增加潜能点
		"""
		if self.potential > csconst.ROLE_POTENTIAL_UPPER:
			self.statusMessage( csstatus.ACCOUNT_CANT_GAIN_POTENTIAL, "" )
			return False

		if self.potential + potential > csconst.ROLE_POTENTIAL_UPPER:
			potential = csconst.ROLE_POTENTIAL_UPPER - self.potential
			self.statusMessage( csstatus.ACCOUNT_CANT_GAIN_POTENTIAL, "" )
			
		self.potential += potential
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.remoteScriptCall( "onAddPotential", ( self, potential, reason ) )
			
		self.statusMessage( csstatus.ACCOUNT_STATE_GAIN_POTENTIAL, potential )
		#添加日志
		g_logger.potentialChangeLog( self.playerDBID, self.getName(), self.potential - potential, self.potential, reason )
		return True
		
	def subPotential( self, potential, reason = csdefine.POTENTIAL_REMOVE_REASON_NORMAL, order = "" ):
		"""
		<define method>
		减少潜能点
		"""
		if self.potential < potential:
			return False
		self.potential -= potential
		self.statusMessage( csstatus.ACCOUNT_STATE_SUB_POTENTIAL, potential )
		#添加日志
		g_logger.potentialChangeLog( self.playerDBID, self.getName(), self.potential + potential, self.potential, reason, order )
		return True

#----------------------功勋接口---------------------------
	def addFeats( self, value, reason = csdefine.FEATS_ADD_REASON_NORMAL ):
		"""
		添加功勋
		"""
		value = int(value)
		self.feats += value
		self.statusMessage(csstatus.CAMP_FEATS_ADD, value)
		return True
		
		#添加日志
		g_logger.roleCreditChangeLog( self.playerDBID, self.playerName, self.feats - value, self.feats, reason)
		
	def subFeats( self, value, reason = csdefine.FEATS_REMOVE_REASON_NORMAL, order = "" ):
		"""
		减少功勋
		"""
		if self.feats < value:
			return False
		self.feats -= value
		return True
		
		#添加日志
		g_logger.roleCreditChangeLog( self.playerDBID, self.playerName, self.feats + value, self.feats, reason, order)

	def getFeatsRecord(self):
		return self.featsRecord

	def addFeatsRecord(self, value, reason):
		"""
		添加每日击杀功勋上限
		:param value:
		:return:
		"""
		if self.featsRecord >= csconst.FEAT_MAX_AMOUNT:
			if self.isShowedFeatRecord:
				self.statusMessage(csstatus.CAMP_FEATS_IS_MAX, "")
				return False
			else:
				self.statusMessage(csstatus.CAMP_FEATS_IS_MAX_FIRST_TIME, "")
				self.isShowedFeatRecord = True
				return False
		value = max(0, min(value,csconst.FEAT_MAX_AMOUNT-self.featsRecord))
		self.featsRecord += value
		self.addFeats(value, reason)
		return True

	def addExploitRecord(self, value):
		"""
		添加每日击杀军功上限
		:param value:
		:return:
		"""
		if self.exploitRecord >= csconst.EXPLOIT_MAX_AMOUNT:
			if self.isShowedExploitRecord:
				self.statusMessage(csstatus.EXPLOIT_IS_MAX, "")
				return False
			else:
				self.statusMessage(csstatus.EXPLOIT_IS_MAX_FIRST_TIME, "")
				self.isShowedExploitRecord  = True
				return False
		value = max(0, min(value, csconst.EXPLOIT_MAX_AMOUNT-self.exploitRecord))
		self.exploitRecord += value
		self.addExploit(value)
		return True

#----------------------AOI---------------------------
	def onClientSetAoi( self, srcEntityID, radius ):
		"""
		<Expose method>
		客户端通知服务器设置AOI半径
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if self.getViewRadius() == radius:
			return
		
		self.setViewRadius( float(radius), Const.DEFAULT_AOI_EXTRA_RADIUS )
		KBEDebug.INFO_MSG( "onClientSetAoi ->%s "%radius )
	
	def onClientResetAoi( self, srcEntityID ):
		"""
		exposed method
		客户端通知重置AOI半径
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		radius = Const.DEFAULT_AOI_RADIUS
		spaceObject = self.getCurrentSpaceObject()
		if spaceObject:
			radius = spaceObject.getSpaceAoi()
		
		if self.getViewRadius() == radius:
			return
		
		self.setViewRadius( radius, Const.DEFAULT_AOI_EXTRA_RADIUS )
		KBEDebug.INFO_MSG( "onClientResetAoi ->%s "%radius )

#----------------------玩家掉落相关--------------------------
	def startFalling( self, srcEntityID):
		"""
		<Expose method>
		玩家客户端开始掉落
		"""
		return
		if not self.validateClientCall( srcEntityID ):
			return
		if self.startFallingHeight == 0.0:
			self.startFallingHeight = self.position.y
		
	def endFalling( self, srcEntityID):
		"""
		<Expose method>
		玩家客户端结束掉落
		"""
		return
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ROLE_END_FALL, self.id, {} )
		damage = int( self.HP_Max * ( self.startFallingHeight - self.position.y - Const.ROLE_DROP_DAMAGE_HEIGHT ) / 50 )
		self.startFallingHeight = 0.0
		if len(self.findBuffsByBuffID(csconst.TELEPORT_PROTECT_BUFFID)):
			return
		if damage < 0:
			return
		if self.HP < damage:
			self.setHP( 0 )
		else:
			self.setHP( self.HP - damage )

	def breakFalling(self):
		"""
		中断掉落
		"""
		return
		self.startFallingHeight = 0.0
		self.client.CLIENT_BreakFalling()

	def LandEndFalling( self, srcEntityID, fallSpeed):
		"""
		<Expose method>
		玩家客户端掉落
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ROLE_END_FALL, self.id, {} )
		if self.HP == 0 and self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		if self.actionForbidSign( csdefine.ACTION_FORBID_BE_ATTACK):
			return

		divide = int(Const.ROLE_DROP_DEAD_SPEED - Const.ROLE_DROP_DAMAGE_SPEED)
		damage = int( self.HP_Max * (fallSpeed - Const.ROLE_DROP_DAMAGE_SPEED ) / divide)
		if damage < 0:
			damage = 0
		isUnyielding = 0
		if self.hasEffectState( csdefine.EFFECT_STATE_UNYIELDING ):
			if int(self.HP - damage ) <= 1:
				isUnyielding = 1

		if isUnyielding:
			self.setHP(1)
		else:
			self.setHP( self.HP - damage )

#----------------------水域相关--------------------------
	def enterWaterArea( self, srcEntityID ):
		"""
		<Expose method>
		玩家进入水域
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.onWaterArea = 1

		buff = self.findBuffsByBuffID( Const.ENTER_WATER_BUFF )
		if not len(buff):
			self.addBuff(self, Const.ENTER_WATER_BUFF)
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:		# 添加进入水域副本通知
			if self.isInSpaceCopy() or self.isInSpacePlane():
				spaceEntity.getScript().onConditionChange( spaceEntity, "WATER", spaceEntity.id, "ENTER", str(self.id) )

	def leaveWaterArea( self, srcEntityID ):
		"""
		<Expose method>
		玩家离开水域
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.onWaterArea = 0

		buff = self.findBuffsByBuffID( Const.ENTER_WATER_BUFF )
		if len(buff):
			self.removeBuffByID(Const.ENTER_WATER_BUFF)

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:		# 添加离开水域副本通知
			if self.isInSpaceCopy() or self.isInSpacePlane():
				spaceEntity.getScript().onConditionChange( spaceEntity, "WATER", spaceEntity.id, "LEAVE", str(self.id) )

#---------------------进入岩浆范围----------------------------
	def enterMaterialArea( self, srcEntityID, materialName ):
		"""
		<Expose method>
		玩家进入有伤害材质范围
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		import MaterialDamage.MaterialDamage
		self.materialAreaSpaceScriptID = self.getCurrentSpaceScriptID()
		if materialName not in MaterialDamage.MaterialDamage.Datas:
			return
		if self.materialAreaSpaceScriptID in MaterialDamage.MaterialDamage.Datas[materialName]:	
			buffId = MaterialDamage.MaterialDamage.Datas[materialName][self.materialAreaSpaceScriptID].get("BuffID",0)
		else:
			buffId = 0
		if buffId:
			self.addBuff( self, buffId )
		else:
			self.setHP( 0 )

	def leaveMaterialArea( self, srcEntityID, materialName ):
		"""
		<Expose method>
		玩家离开有伤害材范围
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		import MaterialDamage.MaterialDamage
		if materialName not in MaterialDamage.MaterialDamage.Datas:
			return
		if self.materialAreaSpaceScriptID not in MaterialDamage.MaterialDamage.Datas[materialName]:
			return
		buffId = MaterialDamage.MaterialDamage.Datas[materialName][self.materialAreaSpaceScriptID].get("BuffID",0)
		buff = self.findBuffsByBuffID( buffId )
		if len(buff):
			self.removeBuffByID( buffId )


#----------------------技能/buff相关--------------------------
	def beforeUseSkill( self, skill, target ):
		"""
		在使用技能之前要做的事情
		"""
		RoleCombatInterface.RoleCombatInterface.beforeUseSkill( self, skill, target )
		# 如果在骑乘状态，需要下马
		if skill.getActForbid() in Const.ACRION_FORBID_OTHER_ACTION:
			if self.isMountOnPet():
				self.transformPet( self.id )
			
	def notifyClientAddBuff( self, buffData, buffTotalTime, buffTime ):
		"""
		添加buff
		"""
		RoleCombatInterface.RoleCombatInterface.notifyClientAddBuff( self, buffData, buffTotalTime, buffTime )
		RoleTeamInterface.RoleTeamInterface.notifyClientAddBuff( self, buffData, buffTotalTime, buffTime )
	
	def notifyClientRemoveBuff( self, buffData ) :
		"""
		删除buff
		"""
		#rolecombatinterface没有notifyclientremovebuff方法 暂时注释
		#RoleCombatInterface.RoleCombatInterface.notifyClientRemoveBuff( self, buffData )
		RoleTeamInterface.RoleTeamInterface.notifyClientRemoveBuff( self, buffData )
	
	def onResetBuffEndTime( self, buffIndex, buffTime ):
		"""
		重置buff持续时间回调
		"""
		RoleCombatInterface.RoleCombatInterface.onResetBuffEndTime( self, buffIndex, buffTime )
		RoleTeamInterface.RoleTeamInterface.onResetBuffEndTime( self, buffIndex, buffTime )
		

#-------------碰撞类型-------------------------------------------------------------
	def setCollisionType( self, collisionType ):
		self.CollisionType = collisionType

	def getCollisionType( self ):
		return self.CollisionType
#----------------------提供给base调用的GM工具接口--------------------------		
	def gm_getPlayerPositionInfo( self, fileno ):
		"""
		<define method>
		"""
		spaceScriptID = self.getCurrentSpaceScriptID()
		line = 1	#暂时
		position = self.position
		name = self.getName()
		datas = {"name": name, "DBID": self.playerDBID, "spaceScriptID": spaceScriptID, "line": line, "position": tuple(position)}
		msg = json.dumps( datas )
		self.base.gm_onSendMsg( msg, fileno )
		
	def gm_getPlayerEquipInfo( self, fileno ):
		"""
		<define method>
		"""
		items = self.getItemListByKBType( ItemTypeEnum.BAG_EQUIP)
		datas = []
		for item in items:
			datas.append({"name": item.getItemDir("ItemName"), "id":item.id, "uid": item.getUid(), "level": item.getLevel(), "quality": item.getQuality()})
		msg = json.dumps( datas )
		self.base.gm_onSendMsg( msg, fileno )
		
	def gm_getPlayerMoneyInfo( self, fileno ):
		"""
		<define method>
		"""
		#暂时只有金币数据，没有金银元宝数据
		money = self.getMoney()
		datas = []
		datas.append( {"type": 3, "value": money, "name": self.getName()} )
		msg = json.dumps( datas )
		self.base.gm_onSendMsg( msg, fileno )
		
	def gm_getPlayerAttributeInfo( self, fileno ):
		"""
		<define method>
		"""
		#暂时只有金币数据，没有金银元宝数据
		money = self.getMoney()
		datas = {}
		datas.update( {"HP": self.HP, "HP_Max": self.HP_Max, "corporeity": self.corporeity, "strength": self.strength, "intellect": self.intellect, "discern": self.discern, "dexterity": self.dexterity, "level": self.getLevel(), "camp": self.getCamp()} )
		datas.update( {"MP": self.MP, "MP_Max": self.MP_Max, "damage": self.damage, "magic_damage": self.magic_damage, "armor": self.armor, "magic_armor": self.magic_armor, "criticalstrike": self.criticalstrike / 100} )
		datas.update( {"xiuwei": self.xiuwei, "potential": self.potential, "parry": self.parry, "speed": self.speed / 100, "hitrate": self.hitrate / 100, "dodgerate": self.dodgerate / 100, "healingrate": self.healingrate / 100} )
		msg = json.dumps( datas )
		self.base.gm_onSendMsg( msg, fileno )

	def gm_getPlayGagInfo( self, fileno ):
		"""
		<define method>
		获取玩家禁言信息
		"""
		datas = {}
		datas.update( {"name": self.getName(), "dbid": self.playerDBID} )
		datas.update( {"chat": {}} )
		for key, value in self.gagData.items():
			if value >= time.time():
				datas["chat"][ key ] = value
		msg = json.dumps( datas )
		self.base.gm_onSendMsg( msg, fileno )

	def gm_gagForPlayer( self, gagList, longTime, reason, GMUser, accountName, fileno ):
		"""
		<define method>
		玩家禁言
		"""
		datas = {}
		datas.update( {"state": "success"} )
		for type in gagList:
			self.gagForPlayer( int( type ), longTime * 60,csdefine.CHAT_FORBID_GM )
			g_logger.roleGagLog(self.playerDBID, self.playerName, self.accountDBID, accountName, type, time.time() + longTime * 60, reason, GMUser)
		msg = json.dumps( datas )
		self.base.gm_onSendMsg( msg, fileno )
		
	def gm_unLockGagForPlayer( self, gagList, reason, GMUser, accountName, fileno ):
		"""
		<define method>
		解除禁言
		"""
		datas = {}
		datas.update( {"state": "success"} )
		for type in gagList:
			self.unlockForPlayerGag( int( type ) )
			g_logger.roleUnGagLog(self.playerDBID, self.playerName, self.accountDBID, accountName, type, reason, GMUser)
		msg = json.dumps( datas )
		self.base.gm_onSendMsg( msg, fileno )
		
	def gm_getPlayerLineNumber(self, fileno):
		"""
		<Define method>
		获取玩家所在分线
		"""
		datas = {}
		datas.update( {"state": "success", "lineNumber": self.lineNumber} )
		msg = json.dumps( datas )
		self.base.gm_onSendMsg( msg, fileno )
		
#--------------------战斗属性相关---------------------------------------
	def getEquipAttachProperties(self):
		"""
		获取装备的附加属性统计
		"""
		dict1 = RoleTitleInterface.RoleTitleInterface.getEquipAttachProperties(self)
		dict2 = RoleKitBagInterface.RoleKitBagInterface.getEquipAttachProperties(self)
		dict3 = SkillInterface.SkillInterface.getEquipAttachProperties(self)
		result = ItemSystemExp.combineEquipAttachProperties(dict1, dict2)
		return ItemSystemExp.combineEquipAttachProperties(result, dict3)


#--------------------播放随机动作---------------------------------------
	def RequestPlayRandomAction( self, srcEntityID ):
		"""
		<Expose method>
		玩家播放随机动作
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		RandomNumber = random.randint( 0, pow( 2, 16 ) ) #服务器随机动作种子的范围在0到2的16次方之间
		self.allClients.PlayRandomAction( RandomNumber )

#------------------重新触发周围陷阱---------------------------------
	def reTriggerNearTrap( self ):
		"""
		复活,保护Buff移除后重新触发周围陷阱
		"""
		if not self.isReady() or self.inDestroying():
			return
		
		entityList = self.entitiesInRangeExt( csdefine.RE_TRIGGER_NEAR_TRAP_RANGE, "Monster" )
		for entity in entityList:
			if not entity.isReal() or entity.inDestroying() or not entity.monsterAIIsStart(): #被传送/被销毁/AI没启动 都不需要触发陷阱
				continue
			
			entity.beReTriggerTrap( self, ECBProximityDefine.PROXIMITY_AI_ATTACK_1 )
			entity.beReTriggerTrap( self, ECBProximityDefine.PROXIMITY_AI_INITIATIVE_1 )
			
		if self.getClient():
			self.client.ReTriggerNearTrap( csdefine.RE_TRIGGER_NEAR_TRAP_RANGE )		# 触发客户端陷阱

	def addCallEntityProtect( self ):
		"""
		添加玩家召唤物（召唤怪，幻兽）保护
		"""
		self.addRolecallMonsterProtect()
		self.base.addRolePetProtect()

	def removeCallEntityProtect( self ):
		"""
		移除玩家召唤物（召唤怪，幻兽）保护
		"""
		self.removeRoleCallMonsterProtect()
		self.base.removeRolePetProtect()
		
#--------------------------移动平台相关-----------------------------------------------------------------
	def onLandMovingPlatform( self, srcEntityID, eid ):
		"""
		<Exposed method>
		玩家跳上移动平台
		eid: 进入移动平台的ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		parentEntity = KBEngine.entities.get( eid, None )
		if parentEntity:
			self.parent = parentEntity
	
	def onDeviateMovingPlatform( self, srcEntityID ):
		"""
		<Exposed method>
		玩家跳下移动平台
		eid: 离开移动平台的ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.parent = None

#--------------------------玩家动作表相关-----------------------------------------------------------------
	def setActionNumber( self, actionNumber ):
		"""
		<define method>
		设置动作表
		"""
		self.actionNumber = actionNumber     #由于动作表是在客户端通过模型ID获取的，所以该属性存的是模型ID

	def getActionNumber( self ):
		"""
		获取模型编号
		"""
		return self.actionNumber

	def setPositionFromClient(self, srcEntityID, pos):
		"""
		define method
		pos:客户端位置
		"""

		if not self.validateClientCall( srcEntityID ):
			return

		self.position = pos
		
	def SetBlendDir(self, srcEntityID, dir):
		if not self.validateClientCall( srcEntityID ):
			return
		self.otherClients.OnSetBlendDir(dir)

	def verifyClientTime(self, srcEntityID, severIndex ):
		"""
		<Exposed method>
		客户端时间验证
		"""	
		if not self.validateClientCall( srcEntityID ):
			return

		self.client.OnSetClientTime(str(Functions.getTime()), severIndex)

#---------------------- timer --------------------------
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		RoleCombatInterface.RoleCombatInterface.timerValeDelCB( self, timerArg )

#---------------------- 移动类型 --------------------------
	def updateMoveType(self, srcEntityID, moveType):
		"""
		<Exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.roleMoveType = moveType
		self.otherClients.OnUpdateMoveType( moveType )


	def onStateChanged( self, old, new ):
		"""
		状态切换。
			@param old	:	更改以前的状态
			@type old	:	integer
			@param new	:	更改以后的状态
			@type new	:	integer
		"""
		# 先通知底层
		RoleCombatInterface.RoleCombatInterface.onStateChanged(self, old, new)
		self.updateRelation()
		self.spaceEvent_OnRoleStateChange()

	def onActionForbid( self, actForbid ):
		"""
		行为禁止时
		"""
		if actForbid == csdefine.ACTION_FORBID_MOVE:
			self.stopMovingForType(csdefine.SYSTEM_MOVE)
			
		if actForbid == csdefine.ACTION_FORBID_CONJURE_PET:
			self.withdrawPetByReason( csdefine.PET_WITHDRAW_COMMON )

	def onActWordChangedTrigger(self, params):
		"""
		"""
		RoleCombatInterface.RoleCombatInterface.onActWordChangedTrigger(self, params)
		act, disabled =  params
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ACT_WORD_CHANGE, self.id, {"actWord":act, "disabled": disabled})

	def triggerSpaceEvent_roleChangeHP(self, eventType, notifierID, args=[]):
		"""
		override method
		接收订阅事件消息回调
		"""
		#触发副本玩家血量改变事件
		self.spaceEvent_roleChangeHP()

#---------------------------------------------- 射击模式 ---------------------------------------------------------------------
	def SetAimOffsetBlendData(self, srcEntityID, YawValue, PitchValue):
		"""
		Exposed method
		同步其他客户端瞄准偏移混合空间方向
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.otherClients:
			self.otherClients.CLIENT_OnSetAimOffsetBlend(YawValue, PitchValue)

	def RequestChangeYCJMDCopyState(self, srcEntityID, ShootState):
		"""
		Exposed method
		服务器通知更新是否射击状态(勇闯绝命岛（远程))
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.otherClients:
			self.otherClients.CLIENT_OnRepYCJMDCopyState( ShootState )

	def RequestYCJMDAimOffsetState(self, srcEntityID, AimOffsetState):
		"""
		Exposed method
		服务器通知更新偏移状态(勇闯绝命岛（远程))
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.otherClients:
			self.otherClients.CLIENT_OnRepYCJMDAimOffsetState( AimOffsetState )

		
#-----------------------------------测试代码（QRN）---------------------------------------------------------------------
	def syncEntityPos(self, srcEntityID, positions, directions):
		"""
		Exposed method
		同步entity坐标和朝向（CST-9224）
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if not Settings.test_flag:
			return
		
		for data in positions:
			id = data["id"]
			position = data["pos"]
			entity = KBEngine.entities.get(id, None)
			if not entity: continue
			
			if entity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_FOLLOW_ROLE:
				entity.setSyncPos(position)
		
		for data in directions:
			id = data["id"]
			direction = data["pos"]
			entity = KBEngine.entities.get(id, None)
			if not entity: continue
			
			if entity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_FOLLOW_ROLE:
				entity.setSyncDire(direction)

#--------------------------------每天更新限制数据---------------------------------------------------------------------------
	def onNewDayLogin(self):
		self.resetExploitRecord()
		self.resetFeatsRecord()


	def resetExploitRecord(self):
		#重置副本军功奖励记录
		self.exploitRecord = 0	
		self.isShowedFeatRecord = False

	def resetFeatsRecord(self):
		#重置副本功勋奖励记录
		self.featsRecord = 0	#重置功勋记录
		self.isShowedexploitRecord = False
		
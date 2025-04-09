# -*- coding: utf-8 -*-


import KBEngine
import KST
import csconst
import Const
import csdefine
import KBEDebug
import time
import Functions

import CoreObject.HasCellOjbect as HasCellOjbect
import CoreInterface.RoleSpaceInterface as RoleSpaceInterface
import CoreInterface.RoleKitBagInterface as RoleKitBagInterface
import CoreInterface.RoleRelationInterface as RoleRelationInterface
import CoreInterface.RoleTeamInterface as RoleTeamInterface
import ImpInterface.StatusMessageInterface as StatusMessageInterface
import CoreInterface.RoleCrondInterface as RoleCrondInterface
import CoreInterface.QuickBarInterface as QuickBarInterface
import CoreInterface.TestInterface as TestInterface
import CoreInterface.RoleShopMallInterface as RoleShopMallInterface
import CoreInterface.RoleLingShiTradeInterface as RoleLingShiTradeInterface
import CoreInterface.RolePetInterface as RolePetInterface
import CoreInterface.TradeInterface as TradeInterface
import CoreInterface.RoleAutoFightInterface as RoleAutoFightInterface
import CoreInterface.RoleTongInterface as RoleTongInterface
import CoreInterface.RoleEquipInterface as RoleEquipInterface
import CoreInterface.AntiWallow as AntiWallow
import ImpInterface.RoleActivityInterface as RoleActivityInterface
import CoreInterface.RoleMailInterface as RoleMailInterface
import ImpInterface.RoleGiftInterface as RoleGiftInterface
import ImpInterface.RoleRankInterface as RoleRankInterface
import ImpInterface.RoleCampInterface as RoleCampInterface
import CoreInterface.EntityDataValidateInterface as EntityDataValidateInterface
import CoreInterface.PresentChargeUnite as PresentChargeUnite
import CoreInterface.RolePointCardInterface as RolePointCardInterface
import CoreInterface.RoleStoreInterface as RoleStoreInterface
import ImpInterface.RoleLunHuiMiJinInterface as RoleLunHuiMiJinInterface
import ImpInterface.RoleTitleInterface as RoleTitleInterface
import ImpInterface.RoleMilitaryRankInterface as RoleMilitaryRankInterface
import CoreInterface.RoleCrossServiceInterface as RoleCrossServiceInterface
import CoreInterface.RoleFixedUpdateInterface as RoleFixedUpdateInterface
import CoreInterface.RoleGameTimeInterface as RoleGameTimeInterface
import CoreInterface.RoleShenTongInterface as RoleShenTongInterface
from MsgLogger import g_logger


class Role(
	KBEngine.Proxy,
	EntityDataValidateInterface.EntityDataValidateInterface,
	HasCellOjbect.HasCellOjbect,
	RoleSpaceInterface.RoleSpaceInterface,
	RoleKitBagInterface.RoleKitBagInterface,
	RoleRelationInterface.RoleRelationInterface,
	RoleTeamInterface.RoleTeamInterface,
	StatusMessageInterface.StatusMessageInterface,
	RoleCrondInterface.RoleCrondInterface,
	QuickBarInterface.QuickBarInterface,
	TestInterface.TestInterface,
	RoleShopMallInterface.RoleShopMallInterface,
	RoleLingShiTradeInterface.RoleLingShiTradeInterface,
	RolePetInterface.RolePetInterface,
	RoleTitleInterface.RoleTitleInterface,
	RoleMilitaryRankInterface.RoleMilitaryRankInterface,
	TradeInterface.TradeInterface,
	RoleAutoFightInterface.RoleAutoFightInterface,
	RoleTongInterface.RoleTongInterface,
	RoleEquipInterface.RoleEquipInterface,
	#AntiWallow.AntiWallow,
	RoleActivityInterface.RoleActivityInterface,
	RoleMailInterface.RoleMailInterface,
	RoleGiftInterface.RoleGiftInterface,
	RoleRankInterface.RoleRankInterface,
	RoleCampInterface.RoleCampInterface,
	PresentChargeUnite.PresentChargeUnite,
	RolePointCardInterface.RolePointCardInterface,
	RoleStoreInterface.RoleStoreInterface,
	RoleLunHuiMiJinInterface.RoleLunHuiMiJinInterface,
	RoleCrossServiceInterface.RoleCrossServiceInterface,
	RoleFixedUpdateInterface.RoleFixedUpdateInterface,
	RoleGameTimeInterface.RoleGameTimeInterface,
	RoleShenTongInterface.RoleShenTongInterface,
	):

	def __init__( self ):
		#基本模块
		KBEngine.Proxy.__init__( self )
		EntityDataValidateInterface.EntityDataValidateInterface.__init__( self )
		HasCellOjbect.HasCellOjbect.__init__( self )
		RoleSpaceInterface.RoleSpaceInterface.__init__( self )
		RoleKitBagInterface.RoleKitBagInterface.__init__( self )
		RoleRelationInterface.RoleRelationInterface.__init__( self )
		RoleTeamInterface.RoleTeamInterface.__init__( self )
		StatusMessageInterface.StatusMessageInterface.__init__( self )
		RoleCrondInterface.RoleCrondInterface.__init__( self )
		QuickBarInterface.QuickBarInterface.__init__( self )
		TestInterface.TestInterface.__init__(self)
		RoleShopMallInterface.RoleShopMallInterface.__init__( self )
		RoleLingShiTradeInterface.RoleLingShiTradeInterface.__init__( self )
		RolePetInterface.RolePetInterface.__init__( self )
		RoleTitleInterface.RoleTitleInterface.__init__( self )
		RoleMilitaryRankInterface.RoleMilitaryRankInterface.__init__( self )
		TradeInterface.TradeInterface.__init__( self )
		RoleAutoFightInterface.RoleAutoFightInterface.__init__( self )
		RoleTongInterface.RoleTongInterface.__init__( self )
		RoleEquipInterface.RoleEquipInterface.__init__( self )
		#AntiWallow.AntiWallow.__init__( self )
		RoleActivityInterface.RoleActivityInterface.__init__( self )
		RoleMailInterface.RoleMailInterface.__init__( self )
		RoleRankInterface.RoleRankInterface.__init__( self )
		RoleGiftInterface.RoleGiftInterface.__init__( self )
		RoleCampInterface.RoleCampInterface.__init__( self )
		PresentChargeUnite.PresentChargeUnite.__init__(self)
		RolePointCardInterface.RolePointCardInterface.__init__(self)
		RoleStoreInterface.RoleStoreInterface.__init__(self)
		RoleLunHuiMiJinInterface.RoleLunHuiMiJinInterface.__init__( self )
		RoleCrossServiceInterface.RoleCrossServiceInterface.__init__( self )
		RoleFixedUpdateInterface.RoleFixedUpdateInterface.__init__(self)
		RoleGameTimeInterface.RoleGameTimeInterface.__init__(self)
		RoleShenTongInterface.RoleShenTongInterface.__init__(self)
	
		
		#系统初始化相关数据
		self.initSystemProgress = 0
		self.waitInitRepeatNum = 0
		self.waitInitSystems = set()
		self.destroyMe = False
		self.waitDestroyTimerID = 0
		self.hasJoinDestroyQueue = False
		
		# 临时数据
		self.isLogouting = False
		self.accountName = ""
		self.playerName = self.cellData["playerName"]	# undefine variable; 角色名称
		self.level = self.cellData["level"]				# undefine variable; 等级
		self.camp =  self.cellData["camp"]				# undefine variable; 阵营
		self.profession = self.cellData["profession"]	# undefine variable; 职业
		self.modelNumber = self.cellData["modelNumber"] # undefine variable; 模型
		self.gender = self.cellData["gender"]			# undefine variable; 性别
		self.cellData["playerDBID"] = self.databaseID	# 把自己的dbid同步到cell上的一个变量里面，以让cell上需要dbid的功能使用
		self.lastLoginTime = int(time.time())
		if not self.fastLoginTime:
			self.fastLoginTime = self.lastLoginTime
		self.cellData["loginTime"] = time.time()
		
		
	def initEntityFlag( self ):
		self.entityFlag = csdefine.ENTITY_FLAG_ROLE
		
	def initRoleInfo(self):
		"""
		对一个角色而言，仅调用一次，在创建玩家后，首次进入游戏
		主要处理首次创建后给玩家任务，道具事议		
		"""
		KBEDebug.INFO_MSG("base playerDBID[%d] first create!"%self.databaseID)
		#根据配置表初始化相关出生属性
		if self.roleState == csdefine.ROLE_STATE_CREATE:
			self.qb_initializeOnCreateRole()

		self.cell.initRoleInfo( self.roleState )

	def onFirstCreateRoleCB(self):
		"""
		<Define method>
		cell 处理完onFirstCreateRole的回调
		"""
		self.roleState = csdefine.ROLE_STATE_ACTIVE
		self.writeToDB()	# 保存属性

	def getName(self):
		"""
		virtual method.
		@return: the name of entity
		@rtype:  STRING
		"""
		return self.playerName
		
	def onLevelUp( self, newLevel ):
		"""
		Define method
		"""
		oldLevel = self.level 
		self.level = newLevel
		
		if hasattr(self, "client") and self.client and oldLevel < Const.SIGN_IN_MIN_LEVEL <= self.level :
			self.initSignInGift()
		RoleGameTimeInterface.RoleGameTimeInterface.onLevelUp(self)

	def getLevel(self):
		"""
		virtual method.
		@return: the name of entity
		@rtype:  uint16
		"""
		return self.level

	def getCamp(self):
		"""
		virtual method.
		@return: the name of entity
		@rtype:  uint16
		"""
		return self.camp

	def getProfession(self):
		"""
		virtual method.
		@return: the name of entity
		@rtype:  uint16
		"""
		return self.profession

	def onClientEnabled( self ):
		"""
		引擎机制，详情请看引擎相关文档
		我们在这个时候建玩家cell实体，并把玩家送到指定地图。
		"""
		if hasattr( self, "cellData" ) and self.cellData != None:
			if self.cell is not None:
				return

			self.logonSpace()
			
	def kickFromAccount(self):
		"""
		account通知销毁
		"""
		if self.destroyMe:
			return
		
		KBEDebug.INFO_MSG("role[%d:%d:%s] kickFromAccount..............."  %(self.databaseID, self.id, self.playerName))
		self._logoff()
		self.disconnect()

	def logoff(self):
		"""
		<Exposed method>
		玩家下线
		"""
		if self.destroyMe:
			return
			
		RoleGameTimeInterface.RoleGameTimeInterface.logoff(self)

		KBEDebug.INFO_MSG("role[%d:%d]%s logoff..............."  %(self.databaseID, self.id, self.playerName))
		self.lifetime += int(time.time() - self.lastLoginTime)
		
		self._logoff()
		self.disconnect()
			
	def logout( self ):
		"""
		<Exposed method>
		注销到角色选择界面
		"""
		if self.destroyMe:
			return

		RoleGameTimeInterface.RoleGameTimeInterface.logout(self)
		
		KBEDebug.INFO_MSG("role[%d:%d]%s logout..............."  %(self.databaseID, self.id, self.playerName))
		self.lifetime += int(time.time() - self.lastLoginTime)
		self.isLogouting = True
		self._logoff()
		self.transferClientToAccount()

	def kickAction( self, kickerMB ):
		"""
		define method
		玩家entitiy踢下线
		"""
		self.logoff()

	def onGetCell( self ):
		"""
		cell 实体创建完成。
		"""
		KBEDebug.INFO_MSG("role [%d:%d]%s get cell..............."  % (self.databaseID, self.id, self.playerName) )
		KST.g_baseAppEntity.registerRole( self )
		KST.g_baseAppEntity.registerRoleByName( self )
		
		RoleSpaceInterface.RoleSpaceInterface.onGetCell( self )
		RoleTongInterface.RoleTongInterface.onGetCell( self )
		RoleRelationInterface.RoleRelationInterface.onGetCell( self )
		RoleShopMallInterface.RoleShopMallInterface.onGetCell( self )
		RoleMilitaryRankInterface.RoleMilitaryRankInterface.onGetCell( self )
		#AntiWallow.AntiWallow.onGetCell( self )
		PresentChargeUnite.PresentChargeUnite.onGetCell( self )
		RoleFixedUpdateInterface.RoleFixedUpdateInterface.onGetCell( self )
		RoleKitBagInterface.RoleKitBagInterface.onGetCell( self )
		RoleGameTimeInterface.RoleGameTimeInterface.onGetCell(self)
		
	
	def onCreateCellFailure( self ):
		"""
		cell创建失败
		"""
		RoleSpaceInterface.RoleSpaceInterface.onCreateCellFailure( self )
	
	def onClientGetCell( self ):
		self.initRoleInfo()
		RoleSpaceInterface.RoleSpaceInterface.onClientGetCell( self )
#		RolePetInterface.RolePetInterface.onClientGetCell( self )
		self.cell.onClientGetCell()

	def onLoseCell( self ):
		"""
		cell死亡
		"""
		KBEDebug.INFO_MSG("role[%d:%d]%s lose cell..............."  % (self.databaseID, self.id, self.playerName) )
		RoleTongInterface.RoleTongInterface.onLoseCell( self )
		RoleRelationInterface.RoleRelationInterface.onLoseCell( self )
		RolePetInterface.RolePetInterface.onLoseCell( self )
		#AntiWallow.AntiWallow.onLoseCell( self )
		RoleActivityInterface.RoleActivityInterface.onLoseCell( self )
		RoleTeamInterface.RoleTeamInterface.onLoseCell( self )
		RoleCrossServiceInterface.RoleCrossServiceInterface.onLoseCell( self )
		if self.isOnCrossService:
			return
		#注意：这个必须放在最后面，因为这里面有destroy的动作
		#调用destroy后，意味着entity也就无法使用了
		HasCellOjbect.HasCellOjbect.onLoseCell( self )
		
	def doDestroyClean( self ):
		"""
		做销毁前的清理
		"""
		#if self.isLogouting:
		#	self.transferClientToAccount()
		
		KBEDebug.INFO_MSG("role[%d:%d]%s doDestroyClean..............."  % (self.databaseID, self.id, self.playerName) )
		#这里加一个判断，防止角色在登录的过程中，客户端断线导致出现CST-5205的错误
		if self.accountEntity:
			self.accountEntity.onAvatarDeath()
		
		HasCellOjbect.HasCellOjbect.doDestroyClean( self )
		self.offlineTime = int( time.time() )
		KST.g_baseAppEntity.deregisterRole( self )
		KST.g_baseAppEntity.deregisterRoleByName( self )
		RoleTeamInterface.RoleTeamInterface.destroySelf( self )
		
	def transferClientToAccount( self ):
		"""
		把客户端转给账号
		"""
		if self.accountEntity is not None:
			if self.hasClient and not self.accountEntity.hasClient:
				self.giveClientTo( self.accountEntity )		# 把控制权交到account中
			
	def logonSpace( self ):
		"""
		玩家上线时触发，请求登录到指定的地图
		玩家登录向SpaceDomain请求登录 -> SpaceDomain通知Space玩家要登录 -> 玩家在空间创建cell在这个位置
		"""
		RoleSpaceInterface.RoleSpaceInterface.logon( self )
		RoleCrossServiceInterface.RoleCrossServiceInterface.logon(self)
		self.currLoginMacAddr = self.accountEntity.currLoginMacAddr
		if not self.fastLoginMacAddr:
			self.fastLoginMacAddr = self.currLoginMacAddr
		
		KBEngine.globalData["MsgLogMgr"].onRoleLogin(self.currLoginMacAddr)
		
		lastClientIpAddr = self.accountEntity.lastClientIpAddr
		lastIP = "%i.%i.%i.%i" % ( lastClientIpAddr & 0xff, ( lastClientIpAddr >> 8 ) & 0xff, ( lastClientIpAddr >> 16 ) & 0xff, ( lastClientIpAddr >> 24 ) & 0xff )
		#添加日志
		g_logger.roleLogonLog( self.databaseID, self.getName(), self.accountEntity.databaseID, self.accountEntity.__ACCOUNT_NAME__, 1, \
			self.getLevel() , int(time.time()) - self.lastLoginTime, lastIP, self.currLoginMacAddr )
			
	def onClientDeath( self ):
		"""
		客户端断开连接通报，销毁自身即下线操作。
		"""
		if self.destroyMe:
			return
		
		KBEDebug.INFO_MSG("role[%d:%d]%s onClientDeath..............."  %(self.databaseID, self.id, self.playerName))
		self._logoff()
	
	def initClientData(self):
		"""
		<Define method>
		初始化客户端数据
		"""
		RolePetInterface.RolePetInterface.initClientData( self )
		QuickBarInterface.QuickBarInterface.initClientData( self )
		RoleMailInterface.RoleMailInterface.initClientData( self )
		RoleGiftInterface.RoleGiftInterface.initClientData( self )
		RoleStoreInterface.RoleStoreInterface.initClientData( self )

	def initRoleAttribute( self, accountEntity ):
		self.xianshi = accountEntity.xianshi
		self.xuanshi = accountEntity.xuanshi
		
		self.cellData["accountDBID"] = self.accountEntity.databaseID
		
	#---------------------提供个cell调用的GM工具接口----------------------------
	
	def gm_onSendMsg( self, msg, fileno ):
		"""
		<define method>
		cell回调接口
		"""
		KST.g_baseAppEntity.gm_doActionCallback( msg, fileno )
	
	#------------------CST-4487 主要解决玩家下线过程中出现各种异常的情况---------
	def registerSystemForInit( self, systemName ):
		"""
		注册需要等待初始化的系统
		注册需放在各个系统的开始初始化的地方
		"""
		if systemName in self.waitInitSystems:
			KBEDebug.ERROR_MSG("Role:registerSystemForInit, %s has exists" %(systemName))
			return
		
		self.initSystemProgress += 1
		self.waitInitSystems.add(systemName)
		
	def onSystemInit( self, systemName ):
		"""
		相应系统初始化回调到这里
		"""
		if systemName not in self.waitInitSystems:
			return
	
		self.initSystemProgress -= 1
		self.waitInitSystems.remove(systemName)
		
	def _destroySelf( self ):
		"""
		"""
		#注意 如果DBID还没有的话，也是无法销毁的
		if self.destroyMe or not self.databaseID:
			return
		
		KBEDebug.INFO_MSG("role[%d:%d]%s _destroySelf..............."  %(self.databaseID, self.id, self.playerName))
		self.destroyMe = True
		#1、所有系统已经初始化完毕
		#2、当前cell已经创建或还未开始创建
		if self.initSystemProgress <= 0 and not self.isCreatingCell():
			self.destroySelf()
		else:
			#延时进行销毁的操作,防止角色上线不久即掉线销毁的话可能导致部分系统出错
			self.waitDestroyTimerID = self.addTimerRepeat(1, "onDelayDestroy", ())
			
	def onDelayDestroy( self ):
		"""
		"""
		if self.initSystemProgress <= 0 and not self.isCreatingCell():
			self.destroySelf()
			self.popTimer(self.waitDestroyTimerID)
			self.waitDestroyTimerID = 0
		else:
			self.waitInitRepeatNum += 1
			if self.waitInitRepeatNum < 5:
				return
		
			KBEDebug.ERROR_MSG("Role:onDelayDestroy, wait times over 5s")
			if not self.isCreatingCell():
				KBEDebug.ERROR_MSG("Role(%d):waitInitSystems[%s]" %(self.id, self.waitInitSystems))
				self.destroySelf()
				self.popTimer(self.waitDestroyTimerID)
				self.waitDestroyTimerID = 0
				return
		
			#cell正在创建过程中，想销毁也销毁不了
			if self.isCreatingCell():
				KBEDebug.ERROR_MSG("Role(%d):onDelayDestroy, cell is creating" %(self.id))
				return
		
			self.destroySelf()
			self.popTimer(self.waitDestroyTimerID)
			self.waitDestroyTimerID = 0
			
	def _logoff(self):
		"""
		"""
		#加入下线列表
		loginAttemperMgr = KBEngine.globalData.get("LoginAttemperMgr", None)
		if loginAttemperMgr is None:
			KBEDebug.ERROR_MSG("not found LoginAttemperMgr!")
			self._destroySelf()
			return
		
		self.hasJoinDestroyQueue = True
		loginAttemperMgr.requestLogoutRole(self.databaseID, self)
		
	def destroyRole(self):
		"""
		define method
		下线
		"""
		self.hasJoinDestroyQueue = False
		self._destroySelf()
		
		KBEngine.globalData["MsgLogMgr"].onRoleLogoff(self.currLoginMacAddr)
		
		lastClientIpAddr = self.accountEntity.lastClientIpAddr
		lastIP = "%i.%i.%i.%i" % ( lastClientIpAddr & 0xff, ( lastClientIpAddr >> 8 ) & 0xff, ( lastClientIpAddr >> 16 ) & 0xff, ( lastClientIpAddr >> 24 ) & 0xff )
		g_logger.roleLogoutLog( self.databaseID, self.getName(), self.accountEntity.databaseID, self.accountEntity.__ACCOUNT_NAME__, 1, \
			self.getLevel(), int(time.time()) - self.lastLoginTime, lastIP, self.currLoginMacAddr )
			
	
	#--------------------------------GM命令----------------------------------------------
	def showBaseAppAllRole(self):
		"""
		显示当前服务器玩家数目
		"""
		#存在客户端才有通知的意义
		if hasattr(self, "client") and self.client:
			KST.g_baseAppEntity.showBaseAppAllRole(self)
			
	def setAccountVIP(self, value):
		"""
		设置账号为VIP
		"""
		if self.accountEntity:
			self.accountEntity.isVIP = True if value else False

	def freezeRole(self, time):
		"""
		冻结当前角色
		"""
		self.roleState = csdefine.ROLE_STATE_FROZEN
		self.unFreezeTime = time
		self.writeToDB()
		
	def onWriteToDB(self, cellData):
		"""
		KBEngine method，调用writeToDB的回调(在存入数据库之前调用)
		"""
		self.recordTime = int(time.time())
	
	#---------------------------------------------------------------------------------------
	
	def networkTest( self ):
		"""
		define method
		网络延迟测试
		"""
		self.client.OnNetworkTest()

	#---------------------------------------------------------------------------------------
	def onRoleSkillUpgrade(self, oldSkill, newSkill):
		"""
		玩家技能升级回调
		"""
		self.updateItemByUpgradeSkillID(oldSkill, newSkill)
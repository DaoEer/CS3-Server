#-*-coding:utf-8-*-
import json, os
import time
import KBEDebug
import Const
import csdefine
import csstatus
import KBEngine
import Functions
import MysqlUtility
from Functions import Functor
from KBEDebug import *
from MsgLogger import g_logger

from CoreObject.EntityObject import EntityObject

class BaseAppEntity( KBEngine.Entity, EntityObject ):
	def __init__( self ):
		KBEngine.Entity.__init__( self )
		EntityObject.__init__( self )
		self.isFirst = False #是否为第一个启动的base
		self._allBaseApps = []
		self._localAllPlayers = {}
		self.localAllRoles = {}
		self._localCampPlayers = {}
		self._allBaseApps.append( self )
		KBEngine.baseAppData[ Const.GLOBAL_BASEDATA_REGISTER_BASEAPP ] = self
		
		self.maxRelationUID = 0
		self.currentRelationUID = 0
		self._tmpSearchCache = {}
		self._tmpSearchCurrentID = 0
		
		try:
			KBEngine.globalData["RelationManager"].assignedRelationUID( self )
		except KeyError:
			KBEDebug.INFO_MSG( "RelationMgr has not been ready yet." )
		
	def setIsFirst( self ):
		self.isFirst = True
	
	def registerBaseAppEntity( self, baseAppEntityMB ):
		"""
		up BaseAppEntity list
		"""
		if self.id == baseAppEntityMB.id:
			return
			
		flag = False
		for app in self._allBaseApps:
			if app.id == baseAppEntityMB.id:
				flag = True
				break
		
		if not flag:
			self._allBaseApps.append( baseAppEntityMB )
			
		if self.isFirst:
			baseAppEntityMB.upAllBaseApps( self._allBaseApps )
	
	def upAllBaseApps( self, baseApps ):
		"""
		<define method>
		更新baseapp entity列表
		"""
		for bMB in baseApps:
			self.registerBaseAppEntity( bMB )
		
	def registerRole( self, roleBase ):
		self.localAllRoles[ roleBase.id ] = roleBase
		camp = roleBase.getCamp()
		if camp in self._localCampPlayers:
			self._localCampPlayers[ camp ].append( roleBase )
		else:
			self._localCampPlayers[ camp ] = [ roleBase ]
	
	def deregisterRole( self, roleBase ):
		"""
		删除注册角色
		"""
		self.localAllRoles.pop( roleBase.id, None )

		camp = roleBase.getCamp()
		if camp not in self._localCampPlayers:
			return
		
		for e in self._localCampPlayers[ camp ]:
			if e.id == roleBase.id:
				self._localCampPlayers[ camp ].remove(e)
				break
	
	def registerRoleByName( self, roleBase ):
		self._localAllPlayers[ roleBase.playerName ] = roleBase

	def deregisterRoleByName( self, roleBase ):
		"""
		删除注册角色
		"""
		self._localAllPlayers.pop( roleBase.playerName, None )
		
	def getAllBaseApps(self):
		return self._allBaseApps
	
#---------------------------------notify world--------------------------------------------------------

	def broadcastChat( self, chatData ):
		"""
		<Define method>
		广播发言内容到当前BaseApp中的所有玩家
		"""
		for e in self.localAllRoles.values():
			e.cell.onReceiveChatMessage( chatData )

	def globalChat( self, chatData ):
		"""
		<Define method>
		广播发言到所有baseApp
		"""
		# ͨ通知每个baseApp，包括自己
		for e in self._allBaseApps:
			e.broadcastChat( chatData )

#-------------------------------广播消息--------------------------------------------------------------
	def globalWold( self, messageType, messageArg ):
		"""
		消息到所有baseApp
		"""
		for e in self._allBaseApps:
			e.broadCastWoldMsg( messageType, messageArg )

	def broadCastWoldMsg( self, messageType, messageArg ):
		"""
		消息到当前BaseApp中的所有玩家
		"""
		for e in self.localAllRoles.values():
			if e.getClient():
				e.client.statusMessage( messageType, messageArg )
			
#-------------------------------更新排行榜--------------------------------------------------------------
	def broadUpdateRank( self, rankType ):
		"""
		消息到所有baseApp
		"""
		for e in self._allBaseApps:
			e.broadAllPlayerUpdateRank( rankType )

	def broadAllPlayerUpdateRank( self, rankType ):
		"""
		define method
		广播玩家更新排行榜
		"""
		for e in self.localAllRoles.values():
			if hasattr(e, "cell") and e.cell:
				e.cell.updateGameRank( rankType )

	def broadRankUpdateMessage(self, rankType):
		"""通知所有baseApp排行榜已更新"""
		for e in self._allBaseApps:
			e.broadAllPlayerRankUpdateMsg(rankType)

	def broadAllPlayerRankUpdateMsg(self, rankType):
		"""通知玩家客户端排行榜已更新"""
		for e in self.localAllRoles.values():
			if e.getClient():
				e.client.Client_updateRankData(rankType)
			
#---------------------------------relationship--------------------------------------------------------
	def requestAllBaseRelationUID( self ):
		"""
		给所有的base分配relationuid
		"""
		for baseAppMB in self._allBaseApps:
			KBEngine.globalData["RelationManager"].assignedRelationUID( baseAppMB )
	
	def receiveRelationUID( self, startUID ):
		"""
		<define method>
		接收玩家关系uid
		"""
		self .currentRelationUID = startUID
		self.maxRelationUID = startUID + Const.RELATION_UID_SAND_MAX_COUNT
		
	def getRelationUID( self ):
		"""
		请求玩家关系UID
		relationUID个数小于10时向mgr申请新的uid资源
		"""
		uid = self.currentRelationUID
		if uid >= self.maxRelationUID:
			uid = -1
		else:
			self.currentRelationUID += 1
		if self.maxRelationUID - self.currentRelationUID < 100:	#这里多分配一点
			KBEngine.globalData["RelationManager"].assignedRelationUID( self )
		return uid
		
#---------------------------------lookupRoleBaseByName---------------------------------------------------
	def lookupRoleBaseByName( self, name, callback ):
		"""
		根据名字查找在线主角的base mailbox。
		先在本进程中查找。如果无法找到目标，再远程查找。
		
		@param name: string; 要查找的在线主角的名字。
		@param callback: function; 该回调函数必须有一个参数，用于给回调者提供查找到的在线主角的base mailbox，如果未找到则参数值为None。
		@return: None
		"""
		for id, roleBase in self.localAllRoles.items():
			if roleBase.getName() == name:
				callback( roleBase )
				return
		if len( self._allBaseApps ) == 1:
			callback( None )
			return
		
		searachID = self._getLookupSearchID()
		self._tmpSearchCache[searachID] = [ len( self._allBaseApps ) - 1, callback ]
		for baseAppMB in self._allBaseApps:
			if baseAppMB.id == self.id:continue
			baseAppMB.remoteLookupRoleBaseByName( self, searachID, name )
		
	def remoteLookupRoleBaseByName( self, baseAppMB, searachID, name ):
		"""
		<define method>
		
		@param baseAppMB: mailbox
		@param searachID: int32
		@param name: string
		@return: 查找的role，如果没有则为None
		"""
		resultBase = None
		for id, roleBase in self.localAllRoles.items():
			if roleBase.getName() == name:
				resultBase = roleBase
		baseAppMB.remoteLookupRoleBaseByNameCB( resultBase, searachID )
		
	def remoteLookupRoleBaseByNameCB( self, resultBaseMB, searachID ):
		"""
		<define method>
		remoteLookupRoleBaseByName回调功能
		
		如果resultBaseMB为None，则表示没有找到，等待其他baseAPP回复；
		如果resultBaseMB为None，切所有baseAPP已回复，表示玩家不在线；
		如果resultBaseMB不为None，则表示找到此玩家。
		"""
		if not self._tmpSearchCache.get( searachID ):return
		
		searachNum, callback = self._tmpSearchCache[searachID]
		if resultBaseMB is None:
			searachNum -= 1
			if searachNum == 0:
				callback( None )
				del self._tmpSearchCache[searachID]
				return
			else:
				self._tmpSearchCache[searachID] = [ searachNum, callback ]
		else:
			callback( resultBaseMB )
			del self._tmpSearchCache[searachID]
			
	def _getLookupSearchID( self ):
		"""
		获得一个用于广播lookupRoleBaseByName()的唯一的id值
		@return: INT32
		"""
		self._tmpSearchCurrentID += 1
		if self._tmpSearchCurrentID >= 0x7FFFFFFF:
			self._tmpSearchCurrentID = 1

		# 循环判断并获取一个不在_tmpSearchCache中存在的ID值
		while self._tmpSearchCurrentID in self._tmpSearchCache:
			self._tmpSearchCurrentID += 1
			if self._tmpSearchCurrentID >= 0x7FFFFFFF:
				self._tmpSearchCurrentID = 1
		return self._tmpSearchCurrentID
		
	def kickRole( self, playerName ):
		"""
		define method
		将玩家踢下线
		"""
		for baseAppMB in self._allBaseApps:
			baseAppMB.kickAction( playerName )

	def kickAction ( self, playerName ):
		"""
		define method
		"""
		if playerName in self._localAllPlayers.keys():
			playBase = self._localAllPlayers[playerName]
			playBase.kickAction( playBase )
	
	def globalCallBaseMethod(self, methodName, args):
		"""
		调用baseApp的指定方法
		"""
		for baseApp in self._allBaseApps:
			baseApp.callBaseMethod(methodName, args)
		
	def callBaseMethod(self, methodName, args):
		"""
		define method
		调用当前baseapp的指定方法
		"""
		method = getattr(self, methodName, "")
		if not method:
			KBEDebug.ERROR_MSG( "BaseApp has no this attribut(%s).%s" % methodName)
			return
		method(*args)
		
	def checkRoleByNameFromDB(self, playerName, callback):
		"""
		根据玩家名字查询玩家是否存在
		"""
		def queryCallback(result, rows, insertid, errstr):
			if errstr:
				KBEDebug.ERROR_MSG( "checkRoleByNameFromDB error:%s." % errstr)
				return
			if len(result) > 0:
				callback(True)
			else:
				callback(False)
		sql = "select id from tbl_Role where sm_playerName = '%s'" % playerName
		KBEngine.executeRawDatabaseCommand(sql, queryCallback)
		
		
	#---------------------------
	#GM使用接口（从GMTools过来）
	#---------------------------
	def gm_doAction(self, msg, fileno):
		"""
		GMToolsManager调用接口
		"""
		for baseAppMB in self._allBaseApps:
			baseAppMB.gm_doActionForPlayer( msg, fileno )
		
	def gm_doActionForPlayer(self, msg, fileno):
		"""
		define method
		"""
		datas = json.loads( msg )
		name = datas.get("roleName", None)
		playerMail = None
		if name:
			for key, value in self.localAllRoles.items():
				if value.getName() == name:
					playerMail = value
					break
		else:
			KBEDebug.ERROR_MSG("Please provide full information")
		if KBEngine.globalData.get("GMToolsManager", None):
			KBEngine.globalData["GMToolsManager"].doActionCallback(msg, fileno, playerMail)
			
	def gm_doActionCallback(self, msg, fileno):
		"""
		"""
		g_GMMgr = KBEngine.globalData.get("GMToolsManager", None)
		if g_GMMgr:
			g_GMMgr.onSendMsg( msg, fileno )
		
	def gm_sendMailForOnlineRole(self, senderMB, senderType, senderName, title, content, money, bindMoney, itemDatas):
		"""
		给当前baseapp所有在线玩家发送邮件
		"""
		for playerName in self._localAllPlayers.keys():
			KBEngine.globalData["MailManager"].send(senderMB, playerName, senderType, senderName, title, content, money, bindMoney, itemDatas, 0, 0)
		
	#---------------------------
	#GM命令使用接口(从客户端GM命令过来)
	#---------------------------
	def showBaseAppAllRole(self, roleBase):
		"""
		显示当前服务器总玩家数目
		"""
		for baseAppMB in self._allBaseApps:
			baseAppMB.showCurBaseAppRole(roleBase)
		
	def showCurBaseAppRole(self, roleBase):
		"""
		显示当前BASEAPP中玩家数目
		"""
		roleBase.client.statusMessage( csstatus.GM_SHOW_BASEAPP_ROLE, "BASEAPP_{}|{}".format( str(os.getenv("KBE_BOOTIDX_GROUP")), str(len(self.localAllRoles))) )
		
	#---------------------------
	#阵营
	#---------------------------
	def globalRemoteCallCampMoraleCell( self, camp, value, oldValue, otherCampMorale, skillID ):
		"""
		阵营气运改变回调baseapp
		"""
		for e in self._allBaseApps:
			e.remoteCallCampPlayerMoraleCell( camp, value, oldValue, otherCampMorale, skillID )
	
	def remoteCallCampPlayerMoraleCell( self, camp, value, oldValue, otherCampMorale, skillID ):
		"""
		Define method.
		阵营气运改变回调player
		"""
		for e in self._localCampPlayers.get( camp, [] ):
			if not e.cell: continue
			e.cell.onCampMoraleChange(value, oldValue, otherCampMorale, skillID)

	def clearCampKillerList(self):
		"""
		清除阵营击杀列表回调baseapp
		"""
		for e in self._allBaseApps:
			e.playerClearCampKillerList()

	def playerClearCampKillerList(self):
		"""
		Define method.
		清除阵营击杀列表回调player
		"""
		for e in self.localAllRoles.values():
			e.cell.onClearCampKillerList()

	def resetCampData(self):
		"""
		重置阵营奖励
		"""
		for e in self._allBaseApps:
			e.playerResetCampData()

	def playerResetCampData(self):
		"""
		Define method.
		重置阵营奖励回调player
		"""
		for e in self.localAllRoles.values():
			e.cell.onResetCampData()

	def globalRemoteCampVenOline(self, venName, title, camp):
		"""
		阵营尊者上线
		"""
		for e in self._allBaseApps:
			e.remoteCallCampVenOline( venName, title, camp )

	def remoteCallCampVenOline(self, venName, title, camp ):
		"""
		Define method.
		阵营尊者上线回调player
		"""
		if title == csdefine.CAMP_FENG_MING_VEV_TITLE:
			for e in self.localAllRoles.values():
				e.cell.onCampVenOlineMessage(venName, title)
			return	
		for e in self._localCampPlayers.get( camp, [] ):
			if not e.cell: continue
			e.cell.onCampVenOlineMessage(venName, title)
		
	def globalOnSetCampSwitch(self, campSwitch):
		"""
		设置阵营开关
		"""
		for e in self._allBaseApps:
			e.remoteCallOnSetCampSwitch( campSwitch )

	def remoteCallOnSetCampSwitch(self,campSwitch):
		"""
		Define method.
		设置阵营开关
		"""
		for e in self.localAllRoles.values():
			e.cell.setClientCampSwitch(campSwitch )

#---------------------------------聊天频道--------------------------------------------------------------
	def broadcastChatCamp( self, chatData ,camp , playerName ):
		"""
		<Define method>
		广播发言内容到所有baseApp的所有同阵营玩家
		"""
		if camp in self._localCampPlayers.keys():
			for e in self._localCampPlayers[camp]:
				if not e.hadBlacklist(playerName):
					e.cell.onReceiveChatMessage( chatData )

	def globalChatCamp(self, chatData , camp , playerName ):
		"""
		<Define method>
		广播发言到所有baseApp
		"""
		# ͨ通知每个baseApp，包括自己
		for e in self._allBaseApps:
			e.broadcastChatCamp( chatData , camp, playerName )

	def broadcastChatSchool( self, chatData ,camp ,profession , playerName ):
		"""
		<Define method>
		广播发言内容到所有baseApp的所有同门派玩家
		"""
		if camp in self._localCampPlayers.keys():
			for e in self._localCampPlayers[camp]:
				if e.profession == profession and not e.hadBlacklist(playerName):
					e.cell.onReceiveChatMessage( chatData )

	def globalChatSchool(self, chatData , camp, profession , playerName ):
		"""
		<Define method>
		广播发言到所有baseApp
		"""
		# ͨ通知每个baseApp，包括自己
		for e in self._allBaseApps:
			e.broadcastChatSchool( chatData , camp, profession, playerName )

	def updateCellChatNum(self):
		"""
		刷新发言条数
		"""
		for e in self.localAllRoles.values():
			e.cell.updateChatNum()
		
	def globalUpdateChatNum(self ):
		"""
		<Define method>
		广播到所有baseApp
		"""
		# ͨ通知每个baseApp，包括自己
		for e in self._allBaseApps:
			e.updateCellChatNum()

	#---------------------------------------  充值通知 --------------------------------------------------------------
	def pickUpChargeOrder( self, accountName ):
		"""
		某个账号提取充值订单物品
		"""
		INFO_MSG( "Account(%s) pick up things!" % accountName )
		
		def _lookUpAccountCallBack(accountMB):
			if accountMB is False:
				return
			if accountMB is True:
				return
			else:
				accountMB.pickUpChargeOrder()
		
		def _SelectAccontCallback(sql, results, rows, insertid, errstr):
			if errstr:
				ERROR_MSG(sql)
				ERROR_MSG(errstr)
				return
			elif len(results) <= 0:
				ERROR_MSG("not found Account(%s)" %(accountName))
				return
			else:
				accountDBID = int(results[0][0])
				KBEngine.lookUpEntityByDBID("Account", accountDBID, _lookUpAccountCallBack)
				
		sql = "select entityDBID from kbe_accountinfos where accountName = %s"
		sql = MysqlUtility.makeSafeSql( sql, (accountName,) )
		KBEngine.executeRawDatabaseCommand(sql, Functor(_SelectAccontCallback, sql))
		
	#-----------------------------------  活动提醒  --------------------------------------------------------------
	def globalBroadcastActivityRemind(self, scriptID, remindType):
		"""
		"""
		# ͨ通知每个baseApp，包括自己
		for e in self._allBaseApps:
			e.broadcastActivityRemind(scriptID, remindType)
		
	def broadcastActivityRemind(self, scriptID, remindType):
		"""
		"""
		for e in self.localAllRoles.values():
			e.remindRoleCrond(scriptID, remindType)
			
	#---------------------------------------- 跨服相关 ---------------------------------------------------------
	def requestCrossServiceResult(self, roleName, result):
		"""
		请求跨服结果
		"""
		for app in self.getAllBaseApps():
			app.onRequestCrossServiceResult(roleName, result)
		
	def onRequestCrossServiceResult(self, roleName, result):
		"""
		define method
		"""      
		playBase = self._localAllPlayers.get(roleName, None)
		if playBase:
			playBase.onRequestCrossServiceResult(result)
			
	def requestReturnServerResult(self, roleName, result):
		"""
		请求返回原服务器结果
		"""
		for app in self.getAllBaseApps():
			app.onRequestReturnServerResult(roleName, result)
		
	def onRequestReturnServerResult(self, roleName, result):
		"""
		define method
		"""
		playBase = self._localAllPlayers.get(roleName, None)
		if playBase: 
			playBase.onRequestReturnServerResult(result)

	#-----------------------------------  通天塔  --------------------------------------------------------------
	def globalResetTongTianDaData(self):
		"""
		通知每个baseApp，包括自己
		"""
		for e in self._allBaseApps:
			e.playerResetTongTianDaData()
		
	def playerResetTongTianDaData(self):
		"""
		define method
		"""
		for e in self.localAllRoles.values():
			e.cell.clearAbandonQuest()
	
	#-----------------------------   定点更新  ------------------------------------------------------------------
	def broadcastFixedTime(self, fixedTimeType, timeUID):
		# 通知每个baseApp, 包括自己
		for e in self._allBaseApps:
			e.fixedTimeUpdate( fixedTimeType, timeUID )	
	
	def fixedTimeUpdate( self, fixedTimeType, timeUID):
		for e in self.localAllRoles.values():
			e.fixedTimeUpdate(fixedTimeType, timeUID)


	#------------------------------练兵场---------------------------------------
	def globalBroadcastLbcStatus(self, line, index, status):
		"""
		广播练兵场状态
		"""
		for e in self._allBaseApps:
			e.broadcastLbcStatus(line, index, status)

	def broadcastLbcStatus(self, line, index, status):
		"""
		"""
		for e in self.localAllRoles.values():
			e.cell.updateLbcStatus(line, index, status)

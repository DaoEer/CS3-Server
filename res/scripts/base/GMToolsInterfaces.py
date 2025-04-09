# -*- coding: utf-8 -*-
import socket
import struct
import json
import time
import pickle

import KBEngine
import KST
import ItemFactory
import csdefine
import LoadModule
import MysqlUtility
from MsgLogger import g_logger
from Functions import Functor
from KBEDebug import *
from ConfigObject.Crond.CrondDatas import CrondDatas
import ItemFactory
from VehiclePetFormulas import formulas

from EntityPool import EntityPool
g_entityPool = EntityPool( "GMToolsInterfaces" )


#entity类型在entities.xml的序号
ENTITY_TYPE_ACCOUNT = 3
ENTITY_TYPE_ROLE = 4

g_CrondDatas = CrondDatas.instance()


class Acceptor:
	"""
	连接器
	"""
	LISTEN_PORT_BASE = 39000
	LISTEN_TRY_MAX = 3
	
	def __init__( self ):
		"""
		"""
		self._socket = None
		self._clients = {}
		
	def start( self, addr = "0.0.0.0", port = LISTEN_PORT_BASE ):
		"""
		开始服务
		"""
		self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		if not port:
			port = self.LISTEN_PORT_BASE
		
		for i in range( self.LISTEN_TRY_MAX ):
			try:
				self._socket.bind( ( addr, port + i ) )
			except Exception as err:
				if i < self.LISTEN_TRY_MAX - 1:
					WARNING_MSG( "bind port '%s' fault, I will try to '%s'" % (port + i, port + i + 1) )
					continue
				else:
					WARNING_MSG( "bind port '%s' fault, break bind." % (port + i) )
					self._socket.close()
					self._socket = None
					return
					
			self._socket.listen( 10 )
			break # 成功绑定后需要停止尝试
		
		KBEngine.registerReadFileDescriptor( self._socket.fileno(), self.onRecv )

	def stop( self ):
		"""
		停止服务
		"""
		if self._socket:
			KBEngine.deregisterReadFileDescriptor( self._socket.fileno() )
			self._socket.close()
			self._socket = None
		
		for processor in list( self._clients.values() ):
			processor.shutdown()
		
		self._clients.clear()
		g_entityPool.releaseAll()
		
	def onRecv( self, fileno ):
		"""
		有新的连接进来了
		"""
		sock, addr = self._socket.accept()
		entity = g_entityPool.get()
		fileno = sock.fileno()
		self._clients[fileno] = entity
		entity.init( self, sock, addr, fileno )
		DEBUG_MSG("new channel[%s/%i]" % (addr, sock.fileno()))
		
	def socketClosed( self, fileno ):
		"""
		socket关闭了，需要反注册一些东东
		"""
		self._clients.pop( fileno )
		
	def getClient( self, fileno ):
		return self._clients.get( fileno, None )
	
class GMToolsInterfaces( KBEngine.Entity ):
	"""
	GM工具消息处理器。
	使用entity的目的是为了使其能获得结果回调
	"""
	
	MSG_HEAD_LEN = struct.calcsize( "!H" )
	
	def onDestroy( self ):
		"""
		"""
		self.shutdown()
	
	def init( self, manager, connectedSocket, addr, fileno ):
		"""
		"""
		self._manager = manager
		self._receivedDatas = b""
		self._addr = addr
		self._socket = connectedSocket
		self._fileno = fileno
		KBEngine.registerReadFileDescriptor( self._socket.fileno(), self.onRecv )

	def shutdown( self ):
		"""
		"""
		if self._socket:
			KBEngine.deregisterReadFileDescriptor( self._socket.fileno() )
			self._socket.close()

		self._socket = None
		self._addr = ""
		self._receivedDatas = ""
		self._manager = None
		g_entityPool.put( self )

	def sendMsg( self, msg, isSpecialMsg = False ):
		"""
		<defined method>
		向socket发送消息
		"""
		if isSpecialMsg:
			self._socket.send(msg)
			return
		msgStr = json.dumps(msg)
		if isinstance( msgStr, str ):
			msgStr = msgStr.encode( "utf-8" )
		sendData = struct.pack("!I", len(msgStr)) + msgStr
		self._socket.send(sendData)

	def onRecv( self, fileno ):
		"""
		有新的消息可读取
		"""
		try:
			data = self._socket.recv(2048)
		except Exception as err:
			WARNING_MSG("socket error. %s/%s; %s" % (self._addr, fileno, err))
			self._manager.socketClosed( fileno )
			self.shutdown()
			return
			
		DEBUG_MSG("%s/%i get data, size=%i" % ( self._addr, self._socket.fileno(), len(data)) )
		
		if len( data ) == 0:
			DEBUG_MSG("get 0 data, close socket. %s/%s" % (self._addr, fileno))
			self._manager.socketClosed( fileno )
			self.shutdown()
			return
		
		self._receivedDatas += data
		(msgLen, ) = struct.unpack( "!H", self._receivedDatas[:2] )
		msgLen += self.MSG_HEAD_LEN
		if len( self._receivedDatas ) < msgLen:
			return
		
		recvData = self._receivedDatas[self.MSG_HEAD_LEN:msgLen]
		self._receivedDatas = self._receivedDatas[msgLen:]
		self.onHandleMsg(recvData)
	
	def onHandleMsg( self, datas ):
		"""
		处理消息
		"""
		d = json.loads( datas.decode( "utf-8" ) )
		cmd = d.get( "cmd" )
		func = getattr( self, "cmd_" + cmd, None )
		
		if func:
			try:
				func( d["info"] )
			except:
				err = {"state" : "fault", "message" : "game server throw exception! see game server log please."}
				self.sendMsg( err )
				EXCEHOOK_MSG( "cmd = %s" % cmd )
		else:
			ERROR_MSG( "UNKNWON MESSAGE: %s " % datas )
			self.sendMsg( {"state" : "fault", "message" : "unknown message"} ) # 结果通知

	def cmd_ping( self, datas ):
		"""
		ping
		"""
		self.sendMsg( {"ping_state" : "success", "message" : ""} )

	def cmd_doActionForPlayer( self, datas ):
		"""
		玩家操作统一接口，该接口一般用于需要通过BaseAppEntity操作的功能
		"""
		g_GMMgr = KBEngine.globalData.get("GMToolsManager", None)
		if g_GMMgr:
			msg = json.dumps( datas )
			g_GMMgr.onRecvMsg( msg, self._fileno )
		else:
			message = {"state" : "fault", "message" : "action error: GMToolsManager is None"}
			self.sendMsg( message )
		
		
	def cmd_queryItemInfoById( self, datas ):
		"""
		通过id获取道具信息
		"""
		itemList = []
		for data in datas:
			itemID = data
			itemData = ItemFactory.ItemFactoryInst.getItemData(itemID)
			if itemData:
				itemList.append({"itemName": itemData["ItemName"], "level":itemData["Level"], "quality": itemData["Quality"]})
		message = {"datas": itemList}
		self.sendMsg(message)
	
	def cmd_queryActivityScheme(self, datas):
		"""
		查询活动日程
		"""
		activityList = []
		crondMgr = KBEngine.globalData["CrondManager"]
		for scheme in crondMgr._schemes:
			if scheme.nextTime < time.time() or scheme.activeTimes != 1 or scheme.key.startswith("GMNotice_"):
				continue
			data = {"key":scheme.key, "startTime":scheme.nextTime, "schemeString":scheme.schemeString, "callbackName":scheme.callbackName}
			activityList.append( data )
		message = {"datas": activityList}
		self.sendMsg( message )
		
	def cmd_startActivity(self, datas):
		"""
		开启活动
		"""
		actType = datas.get("type")
		hasActivityMgr = bool(datas.get("hasActivityMgr"))
		actMgr = datas.get("actMgr")
		startMethod = datas.get("startMethod")
		callbackArgs = tuple(eval(datas.get("callbackArgs")))
		if actType == 1:#现在开启
			if KBEngine.globalData.get(actMgr, None):
					try:
						if hasActivityMgr:
							getattr(KBEngine.globalData.get(actMgr), "GMCommand")(startMethod)
							message = {"state": "success"}
						else:#某些活动或者副本是没有活动管理器的，需要直接调用开始方法，比如ActivityCrondManager
							t = datas.get("time")
							key = datas.get("key")
							year, month, day, hour, minute = time.localtime(t)[:5]
							cmd = "%s %s %s %s *" % ( minute, hour, day, month )
							getattr(KBEngine.globalData.get(actMgr), startMethod)(cmd, *callbackArgs)
							message = {"state": "success"}
					except Exception as err:
						message = {"state": "fault", "message" : "%s" % err}
			else:
				message = {"state": "fault", "message" : "the activity manager [%s] is not exist" % actMgr}
		elif actType == 2:#指定某个时间开启
			t = datas.get("time")
			key = datas.get("key")
			year, month, day, hour, minute = time.localtime(t)[:5]
			cmd = "%s %s %s %s *" % ( minute, hour, day, month )
			try:
				KBEngine.globalData["CrondManager"].addScheme(key, cmd, KBEngine.globalData.get(actMgr), startMethod, 1, callbackArgs)
				message = {"state": "success"}
			except Exception as err:
				message = {"state": "fault", "message" : "%s" % err}
		else:
			message = {"state": "fault", "message": "start scheme send data error"}
		self.sendMsg(message)
			
	def cmd_endActivity(self, datas):
		"""
		结束活动
		"""
		actMgr = datas.get("actMgr")
		endMethod = datas.get("endMethod")
		if KBEngine.globalData.get(actMgr, None):
			try:
				getattr(KBEngine.globalData.get(actMgr), "GMCommand")(endMethod)
				message = {"state": "success"}
			except:
				message = {"state": "fault", "message" : "the activity manager [%s] has no attribute [%s]" % (actMgr, endMethod)}
		else:
			message = {"state": "fault", "message" : "the activity manager [%s] is not exist" % actMgr}
		self.sendMsg(message)
		
	def cmd_cancelActivity(self, datas):
		"""
		取消活动
		"""
		key = datas.get("key")
		schemeString = datas.get("schemeString")
		callbackName = datas.get("callbackName")
		actMgr = datas.get("actMgr")
		if KBEngine.globalData.get(actMgr, None):
			KBEngine.globalData["CrondManager"].removeScheme( key, schemeString, KBEngine.globalData.get(actMgr), callbackName )
			message = {"state": "success"}
		else:
			message = {"state": "fault", "message" : "the activity manager [%s] is not exist" % actMgr}
		self.sendMsg(message)
		
	def cmd_noticeInstant(self, datas):
		"""
		发布即时公告
		"""
		noticeMgr = KBEngine.globalData["GMNoticeManager"]
		intervalTime=datas.get("timeInterval")
		count=datas.get("sendNumber")
		msg=datas.get("noticeContent")
		if noticeMgr:
			noticeMgr.addGMNotice(intervalTime, count, msg, self._fileno)
		else:
			message = {"state" : "fault", "message" : "action error: GMNoticeManager is None"}
			self.sendMsg( message )
	
	def cmd_noticeTiming(self, datas):
		"""
		发布定时公告
		"""
		noticeMgr = KBEngine.globalData["GMNoticeManager"]
		schemeName=datas.get("noticeName")
		sendDate=datas.get("sendDate")
		sendTime=datas.get("sendTime")
		if datas.get("sendDate")=="":
			sendDate="*-*-*"
		if datas.get("sendTime")=="":
			sendTime="*:*:*"
		sendDate=sendDate.split("-")
		sendTime=sendTime.split(":")
		triggerTime=sendTime[1]+" "+sendTime[0]+" "+sendDate[2]+" "+sendDate[1]+" *"
		intervalTime=datas.get("timeInterval")
		count=datas.get("sendNumber")
		msg=datas.get("noticeContent")
		if noticeMgr:
			noticeMgr.addGMSchemeNotice(schemeName ,triggerTime, intervalTime, count, msg, self._fileno)
		else:
			message = {"state" : "fault", "message" : "action error: GMNoticeManager is None"}
			self.sendMsg( message )
	
	def cmd_sendMultipleNotice(self, datas):
		"""
		发布多条公告
		"""
		noticeMgr = KBEngine.globalData["GMNoticeManager"]
		schemeName=datas.get("noticeName")
		sendDateTemple=datas.get("sendDate", "")
		sendTimeTemple=datas.get("sendTime", "")
		if not sendDateTemple.strip() and not sendTimeTemple.strip():
			triggerTime=""
		else:
			sendDate=sendDateTemple.split("-")
			sendTime=sendTimeTemple.split(":")
			triggerTime=sendTime[1]+" "+sendTime[0]+" "+sendDate[2]+" "+sendDate[1]+" *"
		singleTime=datas.get("itemInterval")
		groupTime=datas.get("groupInterval")
		count=datas.get("sendNumber")
		noticeContent=datas.get("noticeContent")
		msgList=[]
		for notice in noticeContent:
			msgList.append(notice.get("content"))
		if noticeMgr:
			noticeMgr.addGMSchemeGroupNotice(schemeName,triggerTime, singleTime, groupTime,count, msgList, self._fileno)
		else:
			message = {"state" : "fault", "message" : "action error: GMNoticeManager is None"}
			self.sendMsg( message )
	
	def cmd_queryNoticeSchemes(self, datas):
		"""
		查询定时公告
		"""
		noticeMgr = KBEngine.globalData["GMNoticeManager"]
		if noticeMgr:
			noticeMgr.GMQueryAllNotices( self._fileno )
		else:
			message = {"state" : "fault", "message" : "action error: GMNoticeManager is None"}
			self.sendMsg( message )
		
	def cmd_deleteNotice(self, datas):
		"""
		删除定时公告
		"""
		schemeName=datas.get("schemeName")
		triggerTime=datas.get("triggerTime")
		timerNoticeID=datas.get("timerNoticeID")
		noticeMgr = KBEngine.globalData["GMNoticeManager"]
		if noticeMgr:
			noticeMgr.delGMSchemeNotice(triggerTime, timerNoticeID, self._fileno)
		else:
			message = {"state" : "fault", "message" : "action error: GMNoticeManager is None"}
			self.sendMsg( message )
		
	def cmd_lockAccount(self, datas):
		"""
		封锁账号
		"""
		##封锁时长功能暂时没有
		accountName = datas.get("account_name", "")
		lockTime = datas.get("lock_time", "")
		reason = datas.get("reason", "")
		GMUser = datas.get("GMUser", "")
		
		def _lookUpAccountCallBack(dbid, mailbox):
			if mailbox is False:
				return
			if mailbox is True:
				return
			else:
				mailbox.kickAction(self)
		
		def _selectCallback(results, rows, insertid, errstr):
			if errstr:
				pass
			
			if len(results) > 0:
				KBEngine.lookUpEntityByDBID("Account", int(results[0][0]), Functor(_lookUpAccountCallBack, results[0][0]))
				
				#添加日志
				g_logger.accountLockLog(int(results[0][0]), accountName, lockTime, reason, GMUser)
		
		def _updateCallback(accountName, results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
				return
			if rows == 0:
				sql = "insert into tbl_GameSeccion(sm_accountName, sm_lockEndTime, sm_lockReason, sm_lockGMUser) value('%s', %i, '%s', '%s' )" \
					% (accountName, time.time() + lockTime, reason, GMUser)
				KBEngine.executeRawDatabaseCommand(sql, Functor(_updateCallback, accountName))
				
			message = {"state" : "success", "message": ""}
			self.sendMsg(message)
			
			sql = "select entityDBID from kbe_accountinfos where accountName = %s"
			sql = MysqlUtility.makeSafeSql( sql, (accountName,) )
			KBEngine.executeRawDatabaseCommand(sql, _selectCallback)
		
		sql = "update tbl_GameSeccion set sm_lockEndTime = %s, sm_lockReason = %s, sm_lockGMUser = %s where sm_accountName = %s"
		sql = MysqlUtility.makeSafeSql( sql, (time.time() + lockTime, reason, GMUser, accountName,) )
		KBEngine.executeRawDatabaseCommand(sql, Functor(_updateCallback, accountName))
		
	def cmd_unLockAccount(self, datas):
		"""
		解封账号
		"""
		accountName = datas.get("account_name", "")
		reason = datas.get("reason", "")
		GMUser = datas.get("GMUser", "")
		
		def _selectCallback(results, rows, insertid, errstr):
			if errstr:
				pass
			if len(results) > 0:
				#添加日志
				g_logger.accountUnLockLog(int(results[0][0]), accountName, reason, GMUser)
				
		def _updateCallback(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
				return
			
			message = {"state" : "success", "message" : ""}
			self.sendMsg(message)
			
			sql = "select entityDBID from kbe_accountinfos where accountName = %s"
			sql = MysqlUtility.makeSafeSql( sql, (accountName,) )
			KBEngine.executeRawDatabaseCommand(sql, _selectCallback)
			
		sql = "update tbl_GameSeccion set sm_lockEndTime = %s, sm_lockReason = %s, sm_lockGMUser = %s where sm_accountName = %s"
		sql = MysqlUtility.makeSafeSql( sql, (0, reason, GMUser, accountName,) )
		KBEngine.executeRawDatabaseCommand(sql, _updateCallback)
		
	def cmd_sendMail(self, datas):
		"""
		发送邮件
		"""
		def queryAllRoleCallback(senderMB, senderType, senderName, title, content, money, bindMoney, itemDatas, results, rows, insertid, errstr):
			if errstr :
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
				return
			for infos in results:
				KBEngine.globalData["MailManager"].send(senderMB, infos[0].decode("utf-8"), senderType, senderName, title, content, money, bindMoney, itemDatas, 0, 0)
			message = {"result_datas": {"errorItemList": []}}
			self.sendMsg(message)
			
		sendTarget = datas.get("send_target")       #发送对象：指定玩家，所以玩家或者所以在线玩家
		roleInfos = datas.get("mail_role_infos", "")       #玩家信息
		title = datas.get("mail_title", "")       #邮件标题
		content = datas.get("mail_content", "")       #邮件内容
		itemInfos = datas.get("mail_item_infos", "")       #物品数据信息
		money = datas.get("mail_money", 0)       #金钱数
		sendType = datas.get("send_type")
		senderName = datas.get("senderName")
		
		errorItemList = []
		itemDatas = []
		if itemInfos:
			for itemInfo in itemInfos.split("|"):
				bindType = -1
				itemStr = itemInfo.split(":")
				if len(itemStr) == 2:
					itemID, amount = itemStr
				elif len(itemStr) == 3:
					itemID, amount, bindType = itemStr
				else:
					message = {"result_datas": {"params error": itemInfo}}
					self.sendMsg(message)
					return
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(int(itemID), int(amount))
				if itemInst:
					if int(bindType) != -1:
						itemInst.setBindType(None, int(bindType))
					itemDatas.append(itemInst)
				else:
					errorItemList .append(itemID)
		
		if len(errorItemList) > 0:	#如果有一个物品ID不正确，则不发送
			message = {"result_datas": {"errorItemList": errorItemList}}
			self.sendMsg(message)
			return
			
		if sendTarget == "target_specify":	#给指定玩家发邮件
			if not roleInfos:
				message = {"state": "fault", "message": "mail_role_infos can't None!"}
				self.sendMsg(message)
				return
			for playerName in roleInfos.split("|"):
				KBEngine.globalData["MailManager"].send(None, playerName, sendType, senderName, title, content, money, 0, itemDatas, 0, 0)
			message = {"result_datas": {"errorItemList": []}}
			self.sendMsg(message)
		elif sendTarget == "target_all":	#给所有玩家发邮件
			sql = "select sm_playerName from tbl_Role"
			KBEngine.executeRawDatabaseCommand(sql, Functor(queryAllRoleCallback, None, sendType, senderName, title, content, money, 0, itemDatas))
		elif sendTarget == "target_online":	#给所有在线玩家发邮件
			KST.g_baseAppEntity.globalCallBaseMethod("gm_sendMailForOnlineRole", (None, sendType, senderName, title, content, money, 0, itemDatas))
			message = {"result_datas": {"errorItemList": []}}
			self.sendMsg(message)	
			
	def cmd_itemIssue(self, datas):
		"""
		发放物品
		"""
		def queryAllRoleCallback(senderMB, senderType, senderName, title, content, money, bindMoney, itemDatas, results, rows, insertid, errstr):
			if errstr :
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
				return
			for infos in results:
				KBEngine.globalData["MailManager"].send(senderMB, infos[0].decode("utf-8"), senderType, senderName, title, content, money, bindMoney, itemDatas, 0, 0)
			message = {"result_datas": {"errorItemList": []}}
			self.sendMsg(message)
			
		itemDatas = datas["item_datas"]
		issueTarget = itemDatas["issue_target"]
		roleInfos = itemDatas["role_infos"]
		issueReason = itemDatas["issue_reason"]
		itemInfos = itemDatas["item_info"]
		issueTitle = itemDatas["issue_title"]
		sendType = itemDatas["send_type"]
		senderName = datas["senderName"]
		errorItemList = []
		itemDatas = []
		if itemInfos:
			for itemInfo in itemInfos.split("|"):
				itemID, amount = itemInfo.split(":")
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(int(itemID), int(amount))
				if not itemInst:
					errorItemList.append(itemID)
				else:
					itemDatas.append(itemInst)
		if len(errorItemList) > 0:	#如果有一个物品ID不正确，则不发放物品
			message = {"result_datas": {"errorItemList": errorItemList}}
			self.sendMsg(message)
			return
		
		if issueTarget == "target_specify":	#给指定玩家发物品
			if not roleInfos:
				message = {"state": "fault", "message": "mail_role_infos can't None!"}
				self.sendMsg(message)
				return
			for playerName in roleInfos.split("|"):
				KBEngine.globalData["MailManager"].send(None, playerName, sendType, senderName, issueTitle, issueReason, 0, 0, itemDatas, 0, 0)
			message = {"result_datas": {"errorItemList": []}}
			self.sendMsg(message)
			
		elif issueTarget == "target_all":	#给所有玩家发物品
			sql = "select sm_playerName from tbl_Role"
			KBEngine.executeRawDatabaseCommand(sql, Functor(queryAllRoleCallback, None, sendType, senderName, issueTitle, issueReason, 0, 0, itemDatas))
		elif issueTarget == "target_online":	#给所有在线玩家发物品
			KST.g_baseAppEntity.globalCallBaseMethod("gm_sendMailForOnlineRole", (None, sendType, senderName, issueTitle, issueReason, 0, 0, itemDatas))
			message = {"result_datas": {"errorItemList": []}}
			self.sendMsg(message)
		
	def cmd_accountTrusteeship(self, datas):
		"""
		账号托管
		"""
		accountName = datas["account_name"]
		longTime = int(datas["long_time"])
		password = datas["password"]
		
		def queryAccountMailboxCallback(dbid, mailbox):
			if mailbox is False:
				return
			if mailbox is True:
				return
			else:
				mailbox.kickAction(self)
		
		def queryAllRoleCallback(results, rows, insertid, errstr):
			if errstr:
				pass
			elif len(results) > 0:
				KBEngine.lookUpEntityByDBID("Account", int(results[0][0]), Functor(queryAccountMailboxCallback, results[0][0]))
				
		def updateGameSeccionCallback(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			else:
				message = {"state": "success", "message": ""}
				self.sendMsg(message)
				sql = "select entityDBID from kbe_accountinfos where accountName = '%s'" % accountName
				KBEngine.executeRawDatabaseCommand(sql, queryAllRoleCallback)
		
		def queryAccountFromGameSeccionCallback(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			elif len(results) > 0:
				sql = "update tbl_GameSeccion set sm_trusteeshipTime = %i, sm_trusteeshipPasswd = md5('%s') \
					where sm_accountName = '%s'" % (time.time() + longTime * 60, password, accountName)
				KBEngine.executeRawDatabaseCommand(sql, updateGameSeccionCallback)
			else:
				sql = "insert into tbl_GameSeccion(sm_accountName, sm_trusteeshipTime, sm_trusteeshipPasswd) value('%s', %i, md5('%s') )" \
					% (accountName, time.time() + longTime * 60, password)
				KBEngine.executeRawDatabaseCommand(sql, updateGameSeccionCallback)
		
		sql = "select sm_accountName from tbl_GameSeccion where sm_accountName = '%s'" % accountName
		KBEngine.executeRawDatabaseCommand(sql, queryAccountFromGameSeccionCallback)
		
	def cmd_accountTrusteeship_cancel(self, datas):
		"""
		取消账号托管
		"""
		pass
		
	def cmd_gag(self ,datas):
		"""
		禁言
		"""
		roleName = datas["roleName"]
		reason = datas["reason"]
		longTime = datas["long_time"]
		gagList = datas["gag_list"]
		GMUser = datas["GMUser"]
		def gagActionCallback(isLast, roleDBID, accountDBID, accountName, gagType, results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			else:
				g_logger.roleGagLog(roleDBID, roleName, accountDBID, accountName, gagType, time.time() + longTime * 60, reason, GMUser)
				if isLast:
					message = {"state": "success"}
					self.sendMsg(message)
				
		def queryGagInfoCallback(isLast, roleDBID, accountDBID, accountName, gagType, results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			elif len(results) > 0:	
				sql = "update tbl_Role_gagData_items set sm_time = %s where parentID= %s and sm_type = %s" % (time.time() + longTime * 60, roleDBID, gagType)
			else:
				sql = "insert into tbl_Role_gagData_items(parentID, sm_type, sm_time) values(%s, %s, %s)" % (roleDBID, gagType, time.time() + longTime * 60)
			KBEngine.executeRawDatabaseCommand(sql, Functor(gagActionCallback, isLast, roleDBID, accountDBID, accountName, gagType))
		
		def queryRoleIsOnlineCallback(roleDBID, accountDBID, accountName, results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			elif len(results) > 0:	#玩家在线
				datas["account_name"] = accountName
				self.cmd_doActionForPlayer(datas)
			else:	#玩家不在线
				sql = "select sm_type from tbl_Role_gagData_items where parentID = %s and sm_type = %s"
				isLast = False
				for gagType in gagList:
					if gagType == gagList[-1]:
						isLast = True
					KBEngine.executeRawDatabaseCommand(sql % (roleDBID, gagType), Functor(queryGagInfoCallback, isLast, roleDBID, accountDBID, accountName, gagType))
			
		def queryRoleCallback(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			elif len(results) <= 0:
				message = {"state": "fault", "message": "the RoleName '%s' is not exist" % roleName}
				self.sendMsg(message)
			else:
				roleDBID = int(results[0][0])
				accountDBID = int(results[0][1])
				accountName = results[0][2].decode("utf-8")
				sql = "select entityDBID from kbe_entitylog where entityDBID = %s and entityType = %s" % (roleDBID, ENTITY_TYPE_ROLE)
				KBEngine.executeRawDatabaseCommand(sql, Functor(queryRoleIsOnlineCallback, roleDBID, accountDBID, accountName))
		sql = "select tbl_Role.id, kbe_accountinfos.entityDBID, kbe_accountinfos.accountName from tbl_Role, kbe_accountinfos \
				where tbl_Role.sm_parentDBID = kbe_accountinfos.entityDBID and tbl_Role.sm_playerName = '%s'" % roleName
		KBEngine.executeRawDatabaseCommand(sql, queryRoleCallback)
		
	def cmd_unGag(self, datas):
		"""
		解除禁言
		"""
		roleName = datas["roleName"]
		reason = datas["reason"]
		gagList = datas["gag_list"]
		GMUser = datas["GMUser"]
		
		def unGagActionCallback(isLast, roleDBID, accountDBID, accountName, gagType, results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			else:
				g_logger.roleUnGagLog(roleDBID, roleName, accountDBID, accountName, gagType, reason, GMUser)
				if isLast:
					message = {"state": "success"}
					self.sendMsg(message)
					
		def queryGagInfoCallback(isLast, roleDBID, accountDBID, accountName, gagType, results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			else:
				sql = "delete from tbl_Role_gagData_items where parentID= %s and sm_type = %s" % (roleDBID, gagType)
			KBEngine.executeRawDatabaseCommand(sql, Functor(unGagActionCallback, isLast, roleDBID, accountDBID, accountName, gagType))
		
		def queryRoleIsOnlineCallback(roleDBID, accountDBID, accountName, results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			elif len(results) > 0:	#玩家在线
				datas["account_name"] = accountName
				self.cmd_doActionForPlayer(datas)
			else:	#玩家不在线
				sql = "select sm_type from tbl_Role_gagData_items where parentID = %s and sm_type = %s"
				isLast = False
				for gagType in gagList:
					if gagType == gagList[-1]:
						isLast = True
					KBEngine.executeRawDatabaseCommand(sql % (roleDBID, gagType), Functor(queryGagInfoCallback, isLast, roleDBID, accountDBID, accountName, gagType))
			
		def queryRoleCallback(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			elif len(results) <= 0:
				message = {"state": "fault", "message": "the RoleName '%s' is not exist" % roleName}
				self.sendMsg(message)
			else:
				roleDBID = int(results[0][0])
				accountDBID = int(results[0][1])
				accountName = results[0][2].decode("utf-8")
				sql = "select entityDBID from kbe_entitylog where entityDBID = %s and entityType = %s" % (roleDBID, ENTITY_TYPE_ROLE)
				KBEngine.executeRawDatabaseCommand(sql, Functor(queryRoleIsOnlineCallback, roleDBID, accountDBID, accountName))
		sql = "select tbl_Role.id, kbe_accountinfos.entityDBID, kbe_accountinfos.accountName from tbl_Role, kbe_accountinfos \
				where tbl_Role.sm_parentDBID = kbe_accountinfos.entityDBID and tbl_Role.sm_playerName = '%s'" % roleName
		KBEngine.executeRawDatabaseCommand(sql, queryRoleCallback)
		
	def cmd_queryRolePositionInfo(self, datas):
		"""
		查询角色登录信息（位置地图）
		"""
		roleName = datas["role_name"]
		def queryRoleCallback(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			elif len(results) <= 0:
				message = {"state": "fault", "message": "the RoleName '%s' is not exist" % roleName}
				self.sendMsg(message)
			else:
				spaceName = results[0][0].decode("utf-8")
				position0 = float(results[0][1])
				position1 = float(results[0][2])
				position2 = float(results[0][1])
				loginData = {"space": spaceName, "position": (position0, position1, position2)}
				message = {"datas": loginData}
				self.sendMsg(message)
				
		sql = "select sm_spaceEventLastSpace, sm_0_position, sm_1_position, sm_2_position from tbl_Role where sm_playerName = '%s'" % roleName  
		KBEngine.executeRawDatabaseCommand(sql, queryRoleCallback)
	
	
	def cmd_queryRolePetInfos(self, datas):
		"""
		查看玩家幻兽信息
		"""
		roleName = datas["roleName"]
		def queryPetInfoCallback(activePetUID, results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			else:
				petInfoList = []
				petCfg = LoadModule.openJsonCfg( r"GameObject/Pet.json" )
				for data in results:
					uid, step, scriptID, name, quality = data
					tempDict = {"name": name.decode("utf-8"), "uid": int(uid), "quality": int(quality), "level": formulas.getLevelByStep(int(step)), "uname": "", "isActive": False}
					if str(int(scriptID)) in petCfg:
						tempDict["uname"] = petCfg[str(int(scriptID))]["Uname"]
					if int(uid) == activePetUID:
						tempDict["isActive"] = True
					petInfoList.append(tempDict)
				message = {"datas": petInfoList}
				self.sendMsg(message)
		
		def queryRoleCallback(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			elif len(results) <= 0:
				message = {"state": "fault", "message": "the RoleName '%s' is not exist" % roleName}
				self.sendMsg(message)
			else:
				roleDBID = int(results[0][0])
				activePetUID = int(results[0][1])
				sql = "select sm_uid, sm_step, sm_scriptID, sm_name, sm_quality from tbl_Role_petPersistentDatas_pets where parentID = %s" % roleDBID
				KBEngine.executeRawDatabaseCommand(sql, Functor(queryPetInfoCallback, activePetUID))
		sql = "select id, sm__activePetUID from tbl_Role where sm_playerName = '%s'" % roleName
		KBEngine.executeRawDatabaseCommand(sql, queryRoleCallback)

	def cmd_chargeOrder(self, datas):
		"""
		充值
		"""
		accountName = datas["accountName"]
		KST.g_baseAppEntity.pickUpChargeOrder(accountName)
		
		message = message = {"state": "success", "message": ""}
		self.sendMsg(message)
		
	def cmd_tranToRevivePos(self, datas):
		"""
		将玩家拉到绑定复活点（为了解决角色卡在异常地图中而无法上线的情况）
		"""
		def setRolePosition(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "tranToRevivePos setRolePosition error: %s" % errstr}
				self.sendMsg(message)
			else:
				message = {"state": "success", "message": ""}
				self.sendMsg(message)
			
		def queryRoleCallback(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "tranToRevivePos queryRoleCallback error: %s" % errstr}
				self.sendMsg(message)
			elif len(results) < 0:
				message = {"state": "fault", "message": "role '%s' is not exist" % datas["roleName"]}
				self.sendMsg(message)
			else:
				#先将玩家踢下线
				KST.g_baseAppEntity.kickRole(datas["roleName"])
				valueStr = "sm_spaceScriptID = '%s', sm_0_position = %s, sm_1_position= %s, sm_2_position = %s, sm_0_direction = %s, sm_1_direction = %s, sm_2_direction = %s" % \
					(results[0][0].decode("utf-8"), float(results[0][1]), float(results[0][2]), float(results[0][3]), float(results[0][4]), float(results[0][5]), float(results[0][6]))
				sql = "UPDATE tbl_Role set %s where sm_playerName = '%s'" % (valueStr, datas["roleName"])
				KBEngine.executeRawDatabaseCommand(sql, setRolePosition)
		roleName = datas.get("roleName", "")	
		if not roleName:
			message = {"state": "fault", "message": "tranToRevivePos error: %s" % errstr}
			self.sendMsg(message)
		else:
			sql = "select sm_reviveSpaceScriptID, sm_0_revivePosition, sm_1_revivePosition, sm_2_revivePosition, sm_0_reviveDirection, sm_1_reviveDirection, sm_2_reviveDirection" + \
				" from tbl_Role where sm_playerName = '%s'" % roleName
			KBEngine.executeRawDatabaseCommand(sql, queryRoleCallback)

	def cmd_freezeRole(self, datas):
		"""
		冻结角色
		"""
		def freezeRoleCallBack(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "freezeRole error: %s" % errstr}
				self.sendMsg(message)
			else:
				message = {"state": "success", "message": ""}
				self.sendMsg(message)
		def freezeRole(roleBase):
			if not isinstance(roleBase, bool):
				roleBase.freezeRole(int(time.time())+int(datas["time"]))
				KST.g_baseAppEntity.kickRole(datas["roleName"])
				message = {"state": "success", "message": ""}
				self.sendMsg(message)
			else:
				sql = "UPDATE tbl_Role SET sm_roleState = %i, sm_unFreezeTime = %s where sm_playerName = '%s'" %(csdefine.ROLE_STATE_FROZEN, int(time.time())+int(datas["time"]), datas["roleName"])
				KBEngine.executeRawDatabaseCommand(sql, freezeRoleCallBack)
		def queryRoleCallback(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "%s" % errstr}
				self.sendMsg(message)
			elif len(results) <= 0:
				message = {"state": "fault", "message": "the RoleName '%s' is not exist" % datas["roleName"]}
				self.sendMsg(message)
			else:
				roleDBID = int(results[0][0])
				KBEngine.lookUpEntityByDBID("Role", roleDBID, freezeRole)
		sql = "select id from tbl_Role where sm_playerName = '%s'" % datas["roleName"]
		KBEngine.executeRawDatabaseCommand(sql, queryRoleCallback)
	
	def cmd_unFreezeRole(self, datas):
		"""
		解除冻结
		"""
		def unFreezeRole(results, rows, insertid, errstr):
			if errstr:
				message = {"state": "fault", "message": "unFreezeRole error: %s" % errstr}
				self.sendMsg(message)
			else:
				message = {"state": "success", "message": ""}
				self.sendMsg(message)
		sql = "UPDATE tbl_Role SET sm_roleState = %i, sm_unFreezeTime = %s where sm_playerName = '%s'" %(csdefine.ROLE_STATE_ACTIVE, 0, datas["roleName"])
		KBEngine.executeRawDatabaseCommand(sql, unFreezeRole)
		
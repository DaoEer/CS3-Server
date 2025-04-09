# -*- coding: utf-8 -*-
import json

import KBEngine
import GMToolsInterfaces
import KBEDebug 
import KST

from CoreObject.MgrPersistentObject import MgrPersistentObject

class GMToolsManager( MgrPersistentObject ):
	def __init__( self ):
		MgrPersistentObject.__init__( self )
		self._acceptor = GMToolsInterfaces.Acceptor()
		self._acceptor.start()
		self._filenoDatas = {}	#用于记录查询base进程的个数
		self._sendFlagDatas = {}
		self.onCompleteInit()
		
	def _sendMsg( self, msg, fileno ):
		"""
		"""
		client = self._acceptor.getClient( fileno )
		if client:
			client.sendMsg( msg )
		else:
			KBEDebug.INFO_MSG(" GM socket fileno: '%s' not exist!" % fileno)
		
	def doActionCallback(self, msg, fileno, playerMail):
		"""
		define method
		"""
		self._filenoDatas[fileno] -= 1	#每回调一次doActionCallback表示查询一个base
		if not playerMail:
			if self._filenoDatas[fileno] == 0 and self._sendFlagDatas[fileno] == 0:	#如果查询完所有的base，palyerMail都为空，表示查询的玩家不存在或者不在线
				err = {"state" : "fault", "message" : "指定玩家不存在或者不在线"}
				self._sendMsg( err, fileno )
			return
		datas = json.loads( msg )
		callback = datas.get("cmd_interface")
		try:
			getattr(self, callback)(datas, fileno, playerMail)
			self._sendFlagDatas[fileno] = 1
		except Exception as e:
			err = {"state" : "fault", "message" : "doActionCallback error: %s" % e}
			self._sendMsg( err, fileno )
				
	def getPlayerPositionInfo( self, datas, fileno, playerMail ):
		"""
		获取玩家位置信息
		"""
		if playerMail:
			playerMail.cell.gm_getPlayerPositionInfo( fileno )
		
	def getPlayerEquipInfo( self, datas, fileno, playerMail ):
		"""
		获取玩家装备信息
		"""
		if playerMail:
			playerMail.cell.gm_getPlayerEquipInfo( fileno )
			
	def getPlayerMoneyInfo( self, datas, fileno, playerMail ):
		"""
		获取玩家金钱信息
		"""
		if playerMail:
			playerMail.cell.gm_getPlayerMoneyInfo( fileno )
		
	def getPlayerAttributeInfo( self, datas, fileno, playerMail ):
		"""
		获取玩家属性信息
		"""
		if playerMail:
			playerMail.cell.gm_getPlayerAttributeInfo( fileno )
	
	def getPlayerGagInfo( self, datas, fileno, playerMail ):
		"""
		获取玩家禁言信息
		"""
		if playerMail:
			playerMail.cell.gm_getPlayGagInfo( fileno )
	
	def gagForPlayer( self, datas, fileno, playerMail ):
		"""
		禁言
		"""
		if playerMail:
			playerMail.cell.gm_gagForPlayer(datas["gag_list"], datas["long_time"], datas["reason"], datas["GMUser"], datas["account_name"], fileno)
			
	def unLockGagForPlayer( self, datas, fileno, playerMail ):
		"""
		解除禁言
		"""
		if playerMail:
			playerMail.cell.gm_unLockGagForPlayer(datas["gag_list"], datas["reason"], datas["GMUser"], datas["account_name"], fileno)
		
	def kickPlayer( self, datas, fileno, playerMail ):
		"""
		踢人
		"""
		if playerMail:
			KST.g_baseAppEntity.kickRole(datas["roleName"])
			message = {"state": "success"}
			self._sendMsg(message, fileno)
			
	def getPlayerLineNumber(self, datas, fileno, playerMail):
		"""
		获取玩家所在分线
		"""
		if playerMail:
			playerMail.cell.gm_getPlayerLineNumber(fileno)
		
	
	def onSendMsg( self, msg, fileno ):
		"""
		<define method>
		发送消息
		"""
		datas = json.loads( msg )
		msg = {"datas": datas}
		self._sendMsg( msg, fileno )
	
	def onRecvMsg( self, msg, fileno ):
		"""
		<define method>
		接收消息
		"""
		self._filenoDatas[fileno] = len(KST.g_baseAppEntity.getAllBaseApps())
		self._sendFlagDatas[fileno] = 0
		datas = json.loads( msg )
		cmd = datas.get("cmd_interface")
		func = getattr( self, cmd, None )
		if func:
			KST.g_baseAppEntity.gm_doAction( msg, fileno )
		else:
			err = {"state" : "fault", "message" : "the cmd interface: '%s' is error" % cmd}
			self._sendMsg( err, fileno )

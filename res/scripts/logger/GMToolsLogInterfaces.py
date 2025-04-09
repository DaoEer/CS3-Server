# -*- coding: utf-8 -*-
import socket
import struct
import json

import KBEngine
import KST
import Define
from KBEDebug import *
import DBConnect


_ACCEPTOR_LIST_ = []

class GMToolsLogInterfaces:
	"""
	GM工具消息处理器。
	使用entity的目的是为了使其能获得结果回调
	"""
	
	MSG_HEAD_LEN = struct.calcsize( "!H" )
	
	def onDestroy( self ):
		"""
		"""
		self.shutdown()
	
	def init( self, manager, connectedSocket, addr ):
		"""
		"""
		self._manager = manager
		self._receivedDatas = b""
		self._addr = addr
		self._socket = connectedSocket
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

	def sendMsg( self, msg ):
		"""
		defined method.
		向socket发送消息
		"""
		msgStr = json.dumps( msg )
		if isinstance( msgStr, str ):
			msgStr = msgStr.encode( "utf-8" )
		sendData = struct.pack( "!d", len(msgStr) ) + msgStr
		self._socket.send( sendData )

	def onRecv( self, fileno ):
		"""
		有新的消息可读取
		"""
		try:
			data = self._socket.recv(2048)
		except Exception as err:
			ERROR_MSG("socket error. %s/%s; %s" % (self._addr, fileno, err))
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
		
		datas = self._receivedDatas[self.MSG_HEAD_LEN:msgLen]
		self._receivedDatas = self._receivedDatas[msgLen:]
		self.onHandleMsg( datas )
	
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
	
	def formatBlobData(self, datas, hasBlobData, blobIndexList):
		"""
		处理数据中的blob类型的数据
		"""
		tempDatas = []
		if not hasBlobData:
			return datas
		for data in datas:
			tempData = list(data)
			for blobIndex in blobIndexList:
				tempData[blobIndex] = tempData[blobIndex].decode("utf-8")
			tempDatas.append(tuple(tempData))
		return tempDatas
	
	def cmd_ping( self, datas ):
		"""
		ping
		"""
		self.sendMsg( {"state" : "success", "message" : ""} )
		
	def cmd_query( self, datas ):
		"""
		查询信息
		"""
		db = DBConnect.getCsol3LogDB()
		sql = datas["sql"]
		hasBlobData = datas.get("hasBlobData", None)
		blobIndexList = datas.get("blobIndexList", [])
		totalNumSql = ""
		if "limit" in sql:
			totalNumSql = "select count(*) " + sql[sql.find("from"): sql.find("limit")]
		else:
			totalNumSql = "select count(*) " + sql[sql.find("from"): ]
		
		totalNum = 0
		totalNumResult = db.select( totalNumSql )
		if len(totalNumResult) > 0:
			totalNum = totalNumResult[0][0]
		
		results = db.select( sql )
		
		msg = {"totalNum": totalNum, "datas": self.formatBlobData(results, hasBlobData, blobIndexList) } 
		
		self.sendMsg( msg )
		
	def cmd_query_item( self, datas ):
		"""
		查询玩家物品流向
		"""
		#查看玩家物品流向，由于不知道玩家具体有哪些物品，所以从玩家添加物品的日志里查找玩家所以的物品
		
		LT_ITEM_ADD			= 1	#添加物品
		LT_TRADE_SWAP_ITEM		= 1	#与玩家交易物品
		LT_TRADE_NPC_SELL		= 5	#卖东西给NPC
		queryData = {}
		condition = datas.get("condition", "")
		
		#玩家添加物品日志
		sql = "select uid, updateTime from %s where action = %s " % ( Define._LOG_TABLES[Define.LOG_TYPE_ITEM], LT_ITEM_ADD )
		if condition:
			sql += "and " + condition
			
		db = DBConnect.getCsol3LogDB()
		results = db.select( sql )
		
		for i in range( len( results ) ):
			data = results[i]
			tempData = []
			sql = "select roleDBID, roleName, param3, param4, updateTime, param1, param2 from %s where action = %s and updateTime > '%s' and param3 = '%s' " % ( 
				Define._LOG_TABLES[Define.LOG_TYPE_TRADE], LT_TRADE_SWAP_ITEM, data[1], data[0] )
			swapResults = db.select( sql )
			tempSwapResults = []
			for result in swapResults:
				result = list( result )
				tempSwapResults.append( result )
				
			sql = "select roleDBID, roleName, param1, param2, updateTime, param6 from %s where action = %s and updateTime > '%s' and param1 = '%s' " % ( 
				Define._LOG_TABLES[Define.LOG_TYPE_TRADE], LT_TRADE_NPC_SELL, data[1], data[0] )
			sellResults = db.select( sql )
			tempSellResults = []
			for result in sellResults:
				result = list( result )
				result.insert( 5, "" )
				tempSellResults.append( result )
				
			tempData.extend( swapResults )
			tempData.extend( tempSellResults )
			tempData = sorted( tempData, key = lambda d:d[4] )
			queryData[ i  + 1 ] = tempData
			
		msg = { "datas": queryData } 
		self.sendMsg( msg )

class Acceptor:
	"""
	连接器
	"""
	LISTEN_PORT_BASE = 49000
	LISTEN_TRY_MAX = 10
	
	def __init__( self ):
		"""
		"""
		self._socket = None
		self._clients = {}
		self._entitise = []
		
	def start( self, addr = "0.0.0.0", port = LISTEN_PORT_BASE ):
		"""
		开始服务
		"""
		self._socket = socket.socket()
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
		
	def onRecv( self, fileno ):
		"""
		有新的连接进来了
		"""
		sock, addr = self._socket.accept()
		entity = GMToolsLogInterfaces()
		self._clients[sock.fileno()] = entity.init( self, sock, addr )
		DEBUG_MSG("new channel[%s/%i]" % (addr, sock.fileno()))
		
	def socketClosed( self, fileno ):
		"""
		socket关闭了，需要反注册一些东东
		"""
		self._clients.pop( fileno )

	
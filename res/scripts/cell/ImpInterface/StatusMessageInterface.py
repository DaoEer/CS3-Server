# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug

class StatusMessageInterface:
	def __init__(self):
		self._replyCellDict = {}
		self.cellKey = 0
		
	def getInquireKey( self ):
		self.cellKey += 1
		return self.cellKey
		
	def checkInquireMessage( self, replyMessage, methodArge ):
		"""
		筛选重复的信息
		"""
		tupeValue = ( replyMessage, methodArge )
		if tupeValue in self._replyCellDict.values():
			return False
		key = self.getInquireKey()
		self._replyCellDict[key] = tupeValue
		return True
	
	def getStrByTuple(self, statusMessageArg):
		"""
		将消息列表转换为字符串格式
		"""
		tempArgs = ""
		if statusMessageArg: 
			index = 0
			for arg in statusMessageArg:
				if index != 0:
					tempArgs += "|"
				index +=1
				tempArgs += str(arg)
		return tempArgs
		
	
	def statusMessage(self, statusMessageType, *statusMessageArg):
		"""
		<Define method>
		@param statusMessageType : 消息类型
		@type  statusMessageType : UINT16
		@param statusMessageArg : 消息内容可变参数列表
		@type  statusMessageArg : 元组
		"""
		messageStr = self.getStrByTuple(statusMessageArg)
		if self.getClient():
			self.client.statusMessage( statusMessageType, messageStr )

	def hideStatusMessage(self, statusMessageType):
		"""
		<Define method>
		@param statusMessageType : 消息类型
		@type  statusMessageType : UINT16		
		"""
		self.client.HideStatusMessage(statusMessageType)


	def statusMessageAllClients(self, statusMessageType, *statusMessageArg):
		"""
		<Define method>
		@param statusMessageType : 消息类型
		@type  statusMessageType : UINT16
		@param statusMessageArg : 消息内容可变参数列表
		@type  statusMessageArg : 元组
		"""
		messageStr = self.getStrByTuple(statusMessageArg)
		self.allClients.statusMessage( statusMessageType, messageStr )

	
	def inquireMessage(self, statusMessageType, statusMessageArg, replyMethod, *methodArge ):
		"""
		<Define method>
		@param statusMessageType : 消息类型
		@type  statusMessageType : UINT16
		@param statusMessageArg : 消息内容可变参数列表
		@type  statusMessageArg : 元组
		@param replyMethod     : 客户端回应的回调
		@type  replyMethod     : String
		@param methodArge : 回调的参数
		@type  methodArge : 元组
		"""
		if self.checkInquireMessage( replyMethod, methodArge ):
			messageStr = self.getStrByTuple(statusMessageArg)
			competent = "Cell"
			self.client.inquireMessage( statusMessageType, messageStr, self.cellKey, competent )
		
	def replyMessage( self, srcEntityID, key, reply ):
		"""
		<Exposed method>
		客户端的回应消息
		"""
		if srcEntityID != self.id:return
		if self._replyCellDict.get( int( key ), None ):
			replyMethod, arge = self._replyCellDict.pop(int(key))
			try:
				if arge:
					getattr( self, replyMethod )( bool( reply ), *arge )
				else:
					getattr( self, replyMethod )( bool( reply ) )
			except:
				KBEDebug.ERROR_MSG( "Can not find the method(%s), Please cheack!"%replyMethod )
				
	def ShowCountDown(self, CDTime):
		"""
		倒计时显示
		"""
		self.client.ShowCountDown( CDTime )

	def ShowExtraTime(self, ETime):
		"""
		加时显示
		"""
		self.client.ShowExtraTime( ETime )
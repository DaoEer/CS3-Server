# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug

class StatusMessageInterface:
	def __init__(self):
		self._replyBaseDict = {}
		self.baseKey = 0
		
	def getInquireKey( self ):
		self.baseKey += 1
		return self.baseKey
		
	def checkInquireMessage( self, replyMessage, methodArge ):
		"""
		筛选重复的信息
		"""
		tupeValue = ( replyMessage, methodArge )
		if tupeValue in self._replyBaseDict.values():
			return False
		key = self.getInquireKey()
		self._replyBaseDict[key] = tupeValue
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
		if hasattr(self, "client") and self.client:
			self.client.statusMessage( statusMessageType, messageStr )


	def hideStatusMessage(self, statusMessageType):
		"""
		<Define method>
		@param statusMessageType : 消息类型
		@type  statusMessageType : UINT16		
		"""
		self.client.HideStatusMessage(statusMessageType)

		
	def inquireMessage(self, statusMessageType, statusMessageArg, replyMethod, *methodArge ):
		"""
		<define method>
		@param statusMessageType : 消息类型
		@type  statusMessageType : UINT16
		@param statusMessageArg : 消息内容可变参数列表
		@type  statusMessageArg : 列表
		@param replyMethod     : 客户端回应的回调
		@type  replyMethod     : String
		@param methodArge : 回调的参数
		@type  methodArge : 列表
		"""
		if self.checkInquireMessage( replyMethod, methodArge ):
			messageStr = self.getStrByTuple(statusMessageArg)
			competent = "Base"
			self.client.inquireMessage( statusMessageType, messageStr, self.baseKey, competent )
		
	def replyMessage( self, key, reply ):
		"""
		<Exposed method>
		客户端的回应消息
		"""
		if not self.validateClientCall():
			return
		if self._replyBaseDict.get( int( key ), None ):
			replyMethod, arge = self._replyBaseDict.pop(int(key))
			if arge:
				getattr( self, replyMethod )( bool( reply ), *arge )
			else:
				getattr( self, replyMethod )( bool( reply ) )
	
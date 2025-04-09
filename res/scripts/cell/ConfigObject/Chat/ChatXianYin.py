# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatXianYin( ChatBase ):
	"""
	仙音聊天频道类
	"""
	def __init__( self ):
		"""
		virtual method.
		初始化
		"""
		ChatBase.__init__( self )

	def verify( self, avatar, chatData ):
		"""
		virtual method.
		验证发送
		"""
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_XIANYIN,chatData )

	def send( self, avatar, chatData ):
		"""
		virtual method.
		发送消息
		"""
		ChatBase.send( self, avatar, chatData )
		chatManager = KBEngine.globalData.get( "ChatManager", None )
		if chatManager == None:
			ERROR_MSG( "chatManager none" )
			return
		itemID = self.condition.get("item",0)
		if itemID:
			avatar.removeItemsByItemID( itemID,1,csdefine.ITEM_REMOVE_BY_CHAT )

		avatar.chatTime[csdefine.CHAT_TYPE_XIANYIN] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_XIANYIN] += 1
		chatManager.onBroadcastChat( chatData )
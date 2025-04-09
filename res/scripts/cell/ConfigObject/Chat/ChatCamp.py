# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatCamp( ChatBase ):
	"""
	阵营聊天频道类
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
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_CAMP, chatData )

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
		avatar.chatTime[csdefine.CHAT_TYPE_CAMP] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_CAMP] += 1
		chatManager.onBroadcastChatCamp( chatData , avatar.camp,avatar.playerName)
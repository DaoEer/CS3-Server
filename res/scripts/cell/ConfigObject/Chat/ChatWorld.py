# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatWorld( ChatBase ):
	"""
	世界聊天频道类
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
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_WORLD, chatData )

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
		avatar.chatTime[csdefine.CHAT_TYPE_WORLD] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_WORLD] += 1
		chatManager.onBroadcastChat( chatData )
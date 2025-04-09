# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatSchool( ChatBase ):
	"""
	门派聊天频道类
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
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_SCHOOL, chatData )

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
		avatar.chatTime[csdefine.CHAT_TYPE_SCHOOL] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_SCHOOL] += 1
		chatManager.onBroadcastChatSchool( chatData , avatar.camp, avatar.profession, avatar.playerName)
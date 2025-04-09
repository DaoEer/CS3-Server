# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatSpace( ChatBase ):
	"""
	地图聊天频道类
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
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_SPACE, chatData )

	def send( self, avatar, chatData ):
		"""
		virtual method.
		发送消息
		"""
		ChatBase.send( self, avatar, chatData )
		space = avatar.getCurrentSpace()
		if not space:
			return
		
		avatar.chatTime[csdefine.CHAT_TYPE_SPACE] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_SPACE] += 1
		space.onSendChatMessage(avatar.playerDBID, chatData)
		
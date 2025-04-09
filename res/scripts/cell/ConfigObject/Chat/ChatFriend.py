# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatFriend( ChatBase ):
	"""
	好友聊天
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
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_FRIEND, chatData )

	def send( self, avatar, chatData ):
		"""
		virtual method.
		发送消息
		"""
		ChatBase.send( self, avatar, chatData )
		avatar.chatTime[csdefine.CHAT_TYPE_FRIEND] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_FRIEND] += 1
		avatar.base.onFriendChat( chatData )
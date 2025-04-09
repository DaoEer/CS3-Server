# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatTong( ChatBase ):
	"""
	帮会频道
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
		if not avatar.tongDBID:
			return False
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_GANG,chatData )

	def send( self, avatar, chatData ):
		"""
		virtual method.
		发送消息
		"""
		ChatBase.send( self, avatar, chatData )
		if avatar.tongMB:
			avatar.chatTime[csdefine.CHAT_TYPE_GANG] = time.time()
			avatar.chatNum[csdefine.CHAT_TYPE_GANG] += 1
			avatar.tongMB.onTongChat( avatar, avatar.playerName,chatData )
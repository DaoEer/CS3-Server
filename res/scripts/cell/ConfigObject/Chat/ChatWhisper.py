# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatWhisper( ChatBase ):
	"""
	私密聊天频道类
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
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_WHISPER, chatData )

	def send( self, avatar, chatData ):
		"""
		virtual method.
		发送消息
		"""
		ChatBase.send( self, avatar, chatData )
		receiverName = chatData.name
		chatData.name = avatar.playerName + "|" + receiverName		#密语聊天需要显示发送者和接收者的名字
		avatar.chatTime[csdefine.CHAT_TYPE_WHISPER] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_WHISPER] += 1
		avatar.base.onWhisperChat( chatData )
		
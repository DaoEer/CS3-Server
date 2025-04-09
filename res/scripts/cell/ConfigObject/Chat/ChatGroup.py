# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatGroup( ChatBase ):
	"""
	讨论组频道类
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
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_GROUP, chatData )

	def send( self, avatar, chatData ):
		"""
		virtual method.
		发送消息
		"""
		ChatBase.send( self, avatar, chatData )
		relationManager = KBEngine.globalData.get( "RelationManager", None )
		if relationManager != None:
			avatar.chatTime[csdefine.CHAT_TYPE_GROUP] = time.time()
			avatar.chatNum[csdefine.CHAT_TYPE_GROUP] += 1
			relationManager.onGroupChat( avatar, chatData )
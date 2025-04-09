# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatSystem( ChatBase ):
	"""
	系统聊天频道类
	"""
	def __init__( self ):
		"""
		virtual method.
		初始化
		"""
		ChatBase.__init__( self )

	def worldSend( self, avatar, chatData ):
		"""
		世界系统发言
		"""
		chatManager = KBEngine.globalData.get( "ChatManager", None )
		if chatManager != None:
			chatManager.onBroadcastChat( chatData )

	def spaceSend( self, avatar, chatData ):
		"""
		地图系统发言
		"""
		spaceEntityID = chatData.parms.get( "spaceID", None )
		if spaceEntityID == None:
			return

		space = KBEngine.entitie.get( spaceEntityID, None )
		if space == None:
			return

		for player in space._spaceRoles:
			player.onReceiveChatMessage( chatData )

	def privateSend( self, avatar, chatData ):
		"""
		个人系统发言
		"""
		chatManager = KBEngine.globalData.get( "ChatManager", None )
		if chatManager != None:
			chatManager.onDesignatedChat( avatar, chatData.parms["playerDBID"], chatData )

	g_TYPE_MAP = {
		csdefine.CHAT_SYSTEM_WORLD		:	worldSend,
		csdefine.CHAT_SYSTEM_SPACE		:	spaceSend,
		csdefine.CHAT_SYSTEM_PRIVATE		:	privateSend,
	}

	def verify( self, avatar, chatData ):
		"""
		virtual method.
		验证发送
		"""
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_SYSTEM, chatData )

	def send( self, avatar, chatData ):
		"""
		virtual method.
		发送消息
		"""
		ChatBase.send( self, avatar, chatData )
		type = chatData.parms.get( "type", None )
		if type not in g_TYPE_MAP:
			return
		avatar.chatTime[csdefine.CHAT_TYPE_SYSTEM] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_SYSTEM] += 1
		g_TYPE_MAP[type]( self, avatar, chatData )
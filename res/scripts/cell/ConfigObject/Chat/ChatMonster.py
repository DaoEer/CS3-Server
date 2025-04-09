# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatMonster( ChatBase ):
	"""
	系统聊天频道类
	"""
	def __init__( self ):
		"""
		virtual method.
		初始化
		"""
		ChatBase.__init__( self )

	def spaceSend( self, avatar, chatData ):
		"""
		地图发言
		"""
		spaceEntityID = chatData.parms.get( "spaceID", None )
		if spaceEntityID == None:
			avatar.onSendChatFail( chatData )
			return

		space = KBEngine.entitie.get( spaceEntityID, None )
		if space == None:
			avatar.onSendChatFail( chatData )
			return

		for player in space._spaceRoles:
			player.onReceiveChatMessage( chatData )

		avatar.onSendChatSuccess( chatData )

	def nearbySend( self, avatar, chatData ):
		"""
		附近发言
		"""
		playerList = avatar.entitiesInRangeExt( csdefine.CHAT_NEARBY_RANGE, "Role" )
		for player in playerList:
			player.onReceiveChatMessage( chatData )

		avatar.onSendChatSuccess( chatData )

	def privateSend( self, avatar, chatData ):
		"""
		密聊发言
		"""
		chatManager = KBEngine.globalData.get( "ChatManager", None )
		if chatManager == None:
			avatar.onSendChatFail( chatData )
			return
		
		chatManager.onDesignatedChat( avatar, chatData.parms["playerDBID"], chatData )

	typeMap = {
		csdefine.CHAT_MONSTER_SPACE		:	spaceSend,
		csdefine.CHAT_MONSTER_NEARBY		:	nearbySend,
		csdefine.CHAT_MONSTER_PRIVATE	:	privateSend,
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
		if type not in self.typeMap:
			return
		avatar.chatTime[csdefine.CHAT_TYPE_SYSTEM] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_SYSTEM] += 1
		avatar.typeMap[type]( self, avatar, chatData )
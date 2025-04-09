# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from csdefine import *
from ConfigObject.Chat.ChatBase.ChatMgr import g_chatMgr
from ChatDataType import ChatData

class MonsterChatInterface:
	"""
	怪物发言接口
	"""
	def __init__( self ):
		pass

	def onSendNearbyMessage( self, message, rictText ):
		"""
		define method.
		发送附近广播消息
		"""
		chatData = ChatData()
		parms = { "type":CHAT_MONSTER_NEARBY, "spaceID":self.spaceID }
		chatData.init( 0, "怪物名称", CHAT_TYPE_MONSTER, ENTITY_FLAG_MONSTER, message, rictText, parms )
		g_chatMgr.onSend( self, chatData )

	def onSendSpaceMessage( self, spaceID, message, rictText ):
		"""
		define method.
		发送地图广播消息
		"""
		chatData = ChatData()
		parms = { "type":CHAT_MONSTER_SPACE, "spaceID":spaceID }
		chatData.init( 0, "怪物名称", CHAT_TYPE_MONSTER, ENTITY_FLAG_MONSTER, message, rictText, parms )
		g_chatMgr.onSend( self, chatData )

	def onSendPrivateMessage( self, playerDBID, message, rictText ):
		"""
		define method.
		发送玩家消息
		"""
		chatData = ChatData()
		parms = { "type":CHAT_MONSTER_PRIVATE, "playerDBID":playerDBID }
		chatData.init( 0, "怪物名称", CHAT_TYPE_MONSTER, ENTITY_FLAG_MONSTER, message, rictText, parms )
		g_chatMgr.onSend( self, chatData )

	def onSendChatSuccess( self, chatData ):
		"""
		callback method.
		发送成功
		"""
		pass

	def onSendChatFail( self, chatData ):
		"""
		callback method.
		发送失败
		"""
		ERROR_MSG( "verify fail" )
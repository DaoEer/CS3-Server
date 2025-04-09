# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from csdefine import *
from Singleton import Singleton

from ConfigObject.Chat.ChatNearby import ChatNearby
from ConfigObject.Chat.ChatSpace import ChatSpace
from ConfigObject.Chat.ChatWorld import ChatWorld
from ConfigObject.Chat.ChatWhisper import ChatWhisper
from ConfigObject.Chat.ChatGroup import ChatGroup
from ConfigObject.Chat.ChatTianYin import ChatTianYin
from ConfigObject.Chat.ChatXianYin import ChatXianYin
from ConfigObject.Chat.ChatSystem import ChatSystem
from ConfigObject.Chat.ChatFriend import ChatFriend
from ConfigObject.Chat.ChatTeam import ChatTeam
from ConfigObject.Chat.ChatTong import ChatTong
from ConfigObject.Chat.ChatCamp import ChatCamp
from ConfigObject.Chat.ChatSchool import ChatSchool

g_TYPE_MAPPING = {
	CHAT_TYPE_NEARBY		:	ChatNearby,
	CHAT_TYPE_SPACE			:	ChatSpace,
	CHAT_TYPE_WORLD			:	ChatWorld,
	CHAT_TYPE_WHISPER		:	ChatWhisper,
	CHAT_TYPE_GROUP			:	ChatGroup,
	CHAT_TYPE_TEAM			:	ChatTeam,
	CHAT_TYPE_COLLECTIVE	:	None,
	CHAT_TYPE_GANG			:	ChatTong,
	CHAT_TYPE_ALIANCE		:	None,
	CHAT_TYPE_SCHOOL		:	ChatSchool,
	CHAT_TYPE_CAMP			:	ChatCamp,
	CHAT_TYPE_BATTLESPACE	:	None,
	CHAT_TYPE_TIANYIN		:	ChatTianYin,
	CHAT_TYPE_XIANYIN		:	ChatXianYin,
	CHAT_TYPE_SYSTEM		:	ChatSystem,
	CHAT_TYPE_FRIEND		:	ChatFriend,
}

class ChatMgr( Singleton ):
	"""
	聊天处理类
	"""
	def __init__( self ):
		self.mapping = {}
		self.channelConfig = {}
		self.chatPageConfig = {}
	def getChannelConfig( self ):
		"""
		获取聊天-频道初始化设置
		"""
		return self.channelConfig
	def getPageConfig( self ):
		"""
		获取聊天-页签初始化设置
		"""
		return self.chatPageConfig

	def init( self, channelConfig, pageCongfig ):
		"""
		配置加载
		"""
		for key, value in channelConfig.items():
			key = int( key )
			self.channelConfig[key] = { "type":value["type"], "color":value["color"], "isCanModify":value["isCanModify"], "shortcutKey":value["shortcutKey"] }
			c = g_TYPE_MAPPING.get( key, None )
			if c is not None:
				result = c()
				result.init( value )
				self.mapping[key] = result

		for k, v in pageCongfig.items():
			k = int( k )
			self.chatPageConfig[k] = { "pageType":v["type"], "pageName":v["pageName"], "chanelArg":v["chanelArg"], "isDeletable":v["isDeletable"], "isDraggable":v["isDraggable"] }
	
	def getType( self, chatType ):
		"""
		类型处理
		"""
		channel = self.mapping.get( chatType, None )
		return channel

	def onSend( self, avatar, chatData ):
		"""
		发送消息
		"""
		channel = self.getType( chatData.type )
		if channel == None:
			ERROR_MSG( "no %s type"%(chatData.type) )
			return

		if channel.verify( avatar, chatData ):
			channel.send( avatar, chatData )
			avatar.onSendChatSuccess( chatData )
			return

		avatar.onSendChatFail( chatData )

g_chatMgr = ChatMgr()
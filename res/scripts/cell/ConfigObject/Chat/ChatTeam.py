# -*- coding: utf-8 -*-
import KBEngine
import time
import KBEDebug
import csdefine
from ConfigObject.Chat.ChatBase.ChatBase import ChatBase

class ChatTeam( ChatBase ):
	"""
	队伍频道
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
		if not avatar.isInTeam():
			return False
		return ChatBase.verify( self, avatar, csdefine.CHAT_TYPE_TEAM, chatData )

	def send( self, avatar, chatData ):
		"""
		virtual method.
		发送消息
		"""
		ChatBase.send( self, avatar, chatData )
		avatar.chatTime[csdefine.CHAT_TYPE_TEAM] = time.time()
		avatar.chatNum[csdefine.CHAT_TYPE_TEAM] += 1
		for playerMB in avatar.getAllTeamMemberMB():
			playerMB.cell.onReceiveChatMessage( chatData )
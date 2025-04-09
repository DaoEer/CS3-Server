# -*- coding: utf-8 -*-
import KBEngine
import csdefine
import csstatus
import KBEDebug
from ConfigObject.Chat.ChatCondition.ChatConditionMgr import g_chatConditionMgr

class ChatBase:
	"""
	聊天频道基础类
	"""
	def __init__( self ):
		"""
		virtual method.
		初始化
		"""
		pass

	def init( self, config ):
		"""
		virtual method.
		配置初始化
		"""
		self.condition = config["condition"]

	def verify( self, avatar, channel,chatData ):
		"""
		virtual method.
		验证发送
		"""
		#验证是否被禁言
		if not avatar.checkGagState( chatData.type ):
			
			return False
			
		if avatar.actionForbidSign( csdefine.ACTION_FORBID_CHAT ):
			avatar.statusMessage( csstatus.CHAT_MSG_FORBID_BY_STATE )
			return False

		# 发言条件验证
		for key, value in self.condition.items():
			if not g_chatConditionMgr.condition( avatar, channel,key, value ):
				return False

		return True

	def send( self, avatar, chatData ):
		"""
		virtual method.
		发送消息
		"""
		pass
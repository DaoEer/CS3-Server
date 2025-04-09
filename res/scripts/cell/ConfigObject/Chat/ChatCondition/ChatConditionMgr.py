# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csstatus
import time
import csdefine

class ChatConditionMgr:
	"""
	聊天条件管理类
	"""
	def __init__( self ):
		pass

	def levelCondition( self, avatar, channel, parms ):
		"""
		等级条件验证
		"""
		if avatar.level < parms:
			avatar.statusMessage(csstatus.CHAT_LEVEL_CANNOT_SATISFY,  parms)
			return False
		return True

	def timeCondition( self, avatar, channel, parms ):
		"""
		发言间隔验证
		"""
		if not channel in avatar.chatTime.keys():
			return True
		if time.time() - avatar.chatTime[channel] < parms:
			avatar.statusMessage(csstatus.CHAT_SPEAK_FREQUENTLY, "" )
			return False
		return True

	def itemCondition( self, avatar, channel, parms ):
		"""
		发言道具验证
		"""
		itemInsts = avatar.getItemInstsByID(parms)
		if not len( itemInsts ):
			if channel == csdefine.CHAT_TYPE_TIANYIN:
				avatar.statusMessage( csstatus.CHAT_TIANYIN_FORBID_BY_ITEM,"" )
			elif channel == csdefine.CHAT_TYPE_XIANYIN:
				avatar.statusMessage( csstatus.CHAT_XIANYIN_FORBID_BY_ITEM,"" )
			return False

		return True

	def numCondition(self, avatar, channel, parms):
		"""
		发言条数验证
		"""
		#如果配置为-1 也就是世界频道按照玩家等级
		if parms == -1:
			if avatar.chatNum[channel] >= avatar.level:
				avatar.statusMessage(csstatus.CHAT_OUTOF_NUMBER)
				return False
		elif avatar.chatNum[channel] >= parms:
			avatar.statusMessage(csstatus.CHAT_OUTOF_NUMBER)
			return False
		return True
	mapping = {
		"level"		:	levelCondition,
		"time"		:	timeCondition,
		"item"		:	itemCondition,
		"num"		:	numCondition,
	}

	def condition( self, avatar, channel, type, parms ):
		"""
		验证发言条件
		"""
		func = self.mapping.get( type, None )
		if func == None:
			return False
		
		return func( self, avatar,channel,parms )

g_chatConditionMgr = ChatConditionMgr()
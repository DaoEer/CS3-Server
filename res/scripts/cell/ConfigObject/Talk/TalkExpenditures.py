# -*- coding: utf-8 -*-
#
import Const
import csdefine
import csstatus
import KBEngine
from KBEDebug import *
from ConfigObject.Talk.TalkBase import BaseNPCTalkExpenditure

class TEMoney( BaseNPCTalkExpenditure.BaseNPCTalkExpenditure):
	"""
	金币消耗
	"""
	def __init__( self, expenditureData ):
		"""
		"""
		self.needMoney = int( expenditureData[ "param1" ] )

	def check( self, player, talkEntity, args ):
		"""
		处理npc对话的消耗
		"""
		if not player.subBindMoney( self.needMoney, csdefine.MONEY_SUB_REASON_NPC_TALK ):
			if not player.subMoney( self.needMoney, csdefine.MONEY_SUB_REASON_NPC_TALK ):
				player.statusMessage( csstatus.MONEY_NOT_ENOUGH )
				return False

		return True
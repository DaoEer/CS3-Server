# -*- coding: utf-8 -*-
#
import KBEngine
from KBEDebug import *

class BaseNPCTalkExpenditure:
	"""
	npc对话的消耗
	"""
	def __init__(self, conditionData):
		"""
		"""
		pass

	def check(self, player, talkEntity, args):
		"""
		处理npc对话的消耗
		"""
		return True
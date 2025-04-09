# -*- coding: utf-8 -*-
#
import KBEngine
from KBEDebug import *

class BaseNPCTalkCondition:
	"""
	npc对话的条件
	"""
	def __init__(self, conditionData):
		"""
		"""
		pass

	def check(self, player, talkEntity, args):
		"""
		判断npc对话的条件
		"""
		return True
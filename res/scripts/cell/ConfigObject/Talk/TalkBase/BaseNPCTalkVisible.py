# -*- coding: utf-8 -*-
#
import KBEngine
from KBEDebug import *

class BaseNPCTalkVisible:
	"""
	npc的可见性
	"""
	def __init__(self, visibleData):
		"""
		"""
		pass

	def isVisible(self, player, talkEntity, args):
		"""
		判断npc的可见性
		"""
		return True
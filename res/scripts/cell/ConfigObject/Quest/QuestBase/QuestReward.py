# -*- coding: utf-8 -*-
#


class QuestRewardBase:

	def __init__(self):
		pass

	def init(self, data):
		pass

	def check(self, player, params = {}):
		return False

	def do(self, player, params = {}):
		pass

	def getRewardType(self):
		return 0
		
	def sendClientData( self, player ):
		return {}
# -*- coding: utf-8 -*-
#


class QuestFuncBase:

	def __init__(self):
		pass

	def init(self, data):
		pass

	def check(self, player, params = {}):
		return False

	def do(self, player, params = {}):
		pass
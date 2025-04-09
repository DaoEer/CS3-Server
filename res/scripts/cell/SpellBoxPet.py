# -*- coding: utf-8 -*-

import SpellBox

class SpellBoxPet( SpellBox.SpellBox ):
	"""
	幻兽掉落 专属SpellBox
	"""
	def __init__(self):
		SpellBox.SpellBox.__init__(self)
		self.onInit()


	def onInit(self):
		"""
		"""
		self.addKeepTimer()

	def addKeepTimer(self):
		"""
		"""
		self.addTimerCallBack(self.keepTime, "removeKeeper",())

	def removeKeeper(self):
		"""
		移除持有者
		"""
		self.keeperDBID = 0
# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
import Const
import Math
import Functions
import KBEMath

class ItemActSeed( ItemUse.ItemUse ):
	"""
	种子
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self.seedID = 0
		self.totalDuration = 0
		if srcData["Param1"]:
			self.seedID = int(srcData["Param1"])
		if srcData["Param2"]:
			self.totalDuration = int(srcData["Param2"])

	def getSeedIDAndTotalDuration( self ):
		"""
		获取种子ID
		"""
		return self.seedID, self.totalDuration

# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import csstatus

class ItemActTJP( ItemUse.ItemUse ):
	"""
	天机盘
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._rewardList = srcData["Param1"]
		self._spaceStr = srcData["Param2"]

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		owner.client.CLIENT_beginTJP(self._rewardList, str(self.uid), self._spaceStr)
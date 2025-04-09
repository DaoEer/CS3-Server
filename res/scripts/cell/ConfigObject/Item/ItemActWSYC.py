# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import csstatus

class ItemActWSYC( ItemUse.ItemUse ):
	"""
	五色鱼叉
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._rewardList = srcData["Param1"]
		self._spaceStr = srcData["Param2"]

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		owner.client.CLIENT_beginJXLC(self._rewardList, str(self.uid), self._spaceStr)
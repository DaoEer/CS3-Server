# -*- coding: utf-8 -*-
import csstatus
import csdefine
import ConfigObject.Item.ItemUse as ItemUse

class ItemActLLBZ( ItemUse.ItemUse ):
	"""
	玲珑宝珠
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._rewardList = srcData["Param1"]
		self._spaceStr = srcData["Param2"]

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		owner.client.CLIENT_beginLLBZ(self._rewardList, str(self.uid), self._spaceStr)
	
# -*- coding: utf-8 -*-
import csstatus
import random
import csdefine
import ConfigObject.Item.ItemUse as ItemUse

class ItemActZBN( ItemUse.ItemUse ):
	"""
	珍宝囊
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._itemID = srcData["Param1"]
		self._buffIDList = [int(i) for i in srcData["Param2"].split("|")]
		self._greyBuff = int(srcData["Param3"])

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		random.shuffle(self._buffIDList)
		param = getAreaParam(self.randomList[0])	
		owner.beginUseZBN(self._itemID, str(self.uid), str(self.id), self._greyBuff, self._buffIDList[0])





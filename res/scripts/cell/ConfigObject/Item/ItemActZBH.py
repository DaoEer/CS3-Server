# -*- coding: utf-8 -*-
import random
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import csstatus

class ItemActZBH( ItemUse.ItemUse ):
	"""
	珍宝盒
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._itemID = srcData["Param1"]
		self._randomList = srcData["Param2"].split("|")	#地图名:x y z:半径 标识:半径 标识...|地图名:x y z:半径 标识:半径 标识...
		self._greyBuff = int(srcData["Param3"])

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		random.shuffle(self._randomList)
		param = self.getAreaParam(self._randomList[0])
		owner.beginUseZBH(self._itemID, str(self.uid),self._greyBuff, param)
		return csstatus.ITEM_USE_GO_ON_MSG

	def getAreaParam(self, string):
		List = string.split(":")
		temp = []
		temp.append(List[0])
		temp.append(Functions.vector3TypeConvert( List[1] ))
		for i in List[2:]:
			i.split()
			temp.append(float(i[0]), int(i[1]))
		return temp

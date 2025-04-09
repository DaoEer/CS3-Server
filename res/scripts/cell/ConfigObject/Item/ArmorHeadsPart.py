# -*- coding: utf-8 -*-
import KBEDebug
import ConfigObject.Item.EquipPartBase as EquipPartBase
import ItemTypeEnum

class ArmorHeadsPart(EquipPartBase.EquipPartBase):
	"""
	头部护甲 半成品
	"""
	def __init__(self, srcData):
		EquipPartBase.EquipPartBase.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,头盔
		"""
		return ItemTypeEnum.EQUIP_HAT



# -*- coding: utf-8 -*-
import KBEDebug
import ConfigObject.Item.Armor as Armor
import ItemTypeEnum

class ArmorHeads(Armor.Armor):
	"""
	头部护甲
	"""
	def __init__(self, srcData):
		Armor.Armor.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,头盔
		"""
		return ItemTypeEnum.EQUIP_HAT



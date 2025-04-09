# -*- coding: utf-8 -*-
import KBEDebug
import ConfigObject.Item.Armor as Armor
import ItemTypeEnum

class ArmorCoats(Armor.Armor):
	"""
	胸部护甲，衣服
	"""
	def __init__(self, srcData):
		Armor.Armor.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,衣服
		"""
		return ItemTypeEnum.EQUIP_COAT

	def onWield(self, owner):
		"""
		装备完成
		"""
		Armor.Armor.onWield(self, owner)
		owner.onCoatWield(self)

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		Armor.Armor.onUnWield(self, owner)
		owner.onCoatUnWield(self)



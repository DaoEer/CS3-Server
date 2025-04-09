# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.Armor as Armor
import ItemTypeEnum

class Necklace(Armor.Armor):
	"""
	项链
	"""
	def __init__(self, srcData):
		Armor.Armor.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,项链
		"""
		return ItemTypeEnum.EQUIP_NECKLACE

	def onWield(self, owner):
		"""
		装备完成
		"""
		Armor.Armor.onWield(self, owner)
		owner.onNecklaceWield(self)

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		Armor.Armor.onUnWield(self, owner)
		owner.onNecklaceUnWield(self)
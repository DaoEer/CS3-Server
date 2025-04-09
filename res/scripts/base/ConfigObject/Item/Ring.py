# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.Armor as Armor
import ItemTypeEnum

class Ring(Armor.Armor):
	"""
	戒指
	"""
	def __init__(self, srcData):
		Armor.Armor.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,戒指
		"""
		return ItemTypeEnum.EQUIP_RING

	def onWield(self, owner):
		"""
		装备完成
		"""
		Armor.Armor.onWield(self, owner)
		owner.onRingWield(self)

	def onRingUnWield(self, owner):
		"""
		卸下道具完成
		"""
		Armor.Armor.onUnWield(self, owner)
		owner.onHatUnWield(self)

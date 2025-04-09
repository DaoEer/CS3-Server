# -*- coding: utf-8 -*-
import KBEDebug
import ItemTypeEnum
import ConfigObject.Item.Armor as Armor

class ArmorBelt(Armor.Armor):
	"""
	腰部护甲，腰带
	"""
	def __init__(self, srcData):
		Armor.Armor.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,腰带
		"""
		return ItemTypeEnum.EQUIP_WAIST

	def onWield(self, owner):
		"""
		装备完成
		"""
		Armor.Armor.onWield(self, owner)
		owner.onWaistWield(self)

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		Armor.Armor.onUnWield(self, owner)
		owner.onWaistUnWield(self)
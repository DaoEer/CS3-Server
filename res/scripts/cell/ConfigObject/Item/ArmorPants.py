# -*- coding: utf-8 -*-
import KBEDebug
import ConfigObject.Item.Armor as Armor
import ItemTypeEnum

class ArmorPants(Armor.Armor):
	"""
	腿部护甲，裤子
	"""
	def __init__(self, srcData):
		Armor.Armor.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,裤子
		"""
		return ItemTypeEnum.EQUIP_PANTS

	def onWield(self, owner):
		"""
		装备完成
		"""
		Armor.Armor.onWield(self, owner)
		owner.onPantsWield(self)

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		Armor.Armor.onUnWield(self, owner)
		owner.onPantsUnWield(self)
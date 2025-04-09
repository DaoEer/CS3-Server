# -*- coding: utf-8 -*-
import KBEDebug
import ConfigObject.Item.Armor as Armor
import ItemTypeEnum

class ArmorSuits(Armor.Armor):
	"""
	suits
	"""
	def __init__(self, srcData):
		Armor.Armor.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,手套
		"""
		return ItemTypeEnum.EQUIP_SUIT

	def onWield(self, owner):
		"""
		装备完成
		"""
		Armor.Armor.onWield(self, owner)
		owner.onSuitsWield(self)

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		Armor.Armor.onUnWield(self, owner)
		owner.onSuitsUnWield(self)



# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.Armor as Armor

class ArmorCloak(Armor.Armor):
	"""
	披风
	"""
	def __init__(self, srcData):
		Armor.Armor.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,披风
		"""
		return ItemTypeEnum.EQUIP_CLOAK

	def onWield(self, owner):
		"""
		装备完成
		"""
		Armor.Armor.onWield(self, owner)
		owner.onCloakWield(self)
	
	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		Armor.Armor.onUnWield(self, owner)
		owner.onClockUnWield(self)


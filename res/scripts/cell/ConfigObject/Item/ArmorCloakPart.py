# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.EquipPartBase as EquipPartBase

class ArmorCloakPart(EquipPartBase.EquipPartBase):
	"""
	披风 半成品
	"""
	def __init__(self, srcData):
		EquipPartBase.EquipPartBase.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,披风
		"""
		return ItemTypeEnum.EQUIP_CLOAK

	def onWield(self, owner):
		"""
		装备完成
		"""
		EquipPartBase.EquipPartBase.onWield(self, owner)
		owner.onCloakWield(self)
	
	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		EquipPartBase.EquipPartBase.onUnWield(self, owner)
		owner.onClockUnWield(self)


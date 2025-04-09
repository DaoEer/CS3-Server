# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.EquipPartBase as EquipPartBase
import ItemTypeEnum

class WeaponPart(EquipPartBase.EquipPartBase):
	"""
	武器基类
	"""
	def __init__(self, srcData):
		"""
		"""
		EquipPartBase.EquipPartBase.__init__(self, srcData)

	def onWield(self, owner, update = True):
		"""
		装备完成
		"""
		EquipPartBase.EquipPartBase.onWield(self, owner)
		owner.onWeaponWield(self)
	
	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		EquipPartBase.EquipPartBase.onUnWield(self, owner)
		owner.onWeaponUnWield(self)

	def getEquipPart(self):
		"""
		获取装备部位,武器
		"""
		return ItemTypeEnum.EQUIP_WEAPON
# -*- coding: utf-8 -*-
import KBEDebug
import ConfigObject.Item.EquipPartBase as EquipPartBase
import ItemTypeEnum

class ArmorCoatsPart(EquipPartBase.EquipPartBase):
	"""
	胸部护甲，衣服半成品
	"""
	def __init__(self, srcData):
		EquipPartBase.EquipPartBase.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,衣服
		"""
		return ItemTypeEnum.EQUIP_COAT

	def onWield(self, owner):
		"""
		装备完成
		"""
		EquipPartBase.EquipPartBase.onWield(self, owner)
		owner.onCoatWield(self)

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		EquipPartBase.EquipPartBase.onUnWield(self, owner)
		owner.onCoatUnWield(self)



# -*- coding: utf-8 -*-
import KBEDebug
import ItemTypeEnum
import ConfigObject.Item.EquipPartBase as EquipPartBase

class ArmorBeltPart(EquipPartBase.EquipPartBase):
	"""
	腰部护甲，腰带半成品
	"""
	def __init__(self, srcData):
		EquipPartBase.EquipPartBase.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,腰带
		"""
		return ItemTypeEnum.EQUIP_WAIST

	def onWield(self, owner):
		"""
		装备完成
		"""
		EquipPartBase.EquipPartBase.onWield(self, owner)
		owner.onWaistWield(self)

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		EquipPartBase.EquipPartBase.onUnWield(self, owner)
		owner.onWaistUnWield(self)
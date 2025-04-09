# -*- coding: utf-8 -*-
import KBEDebug
import ConfigObject.Item.EquipPartBase as EquipPartBase
import ItemTypeEnum

class ArmorSuitsPart(EquipPartBase.EquipPartBase):
	"""
	suits 半成品
	"""
	def __init__(self, srcData):
		EquipPartBase.EquipPartBase.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,手套
		"""
		return ItemTypeEnum.EQUIP_SUIT

	def onWield(self, owner):
		"""
		装备完成
		"""
		EquipPartBase.EquipPartBase.onWield(self, owner)
		owner.onSuitsWield(self)

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		EquipPartBase.EquipPartBase.onUnWield(self, owner)
		owner.onSuitsUnWield(self)



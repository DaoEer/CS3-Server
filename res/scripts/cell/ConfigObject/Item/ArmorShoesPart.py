# -*- coding: utf-8 -*-
import KBEDebug
import ConfigObject.Item.EquipPartBase as EquipPartBase
import ItemTypeEnum

class ArmorShoesPart(EquipPartBase.EquipPartBase):
	"""
	足部护甲，鞋子 半成品
	"""
	def __init__(self, srcData):
		EquipPartBase.EquipPartBase.__init__(self, srcData)

	def getEquipPart(self):
		"""
		获取装备部位,鞋子
		"""
		return ItemTypeEnum.EQUIP_SHOES

	def onWield(self, owner):
		"""
		装备完成
		"""
		EquipPartBase.EquipPartBase.onWield(self, owner)
		owner.onShoesWield(self)

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		EquipPartBase.EquipPartBase.onUnWield(self, owner)
		owner.onShoesUnWield(self)
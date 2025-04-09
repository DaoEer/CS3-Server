# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.Equip as Equip
import ItemTypeEnum

class Weapon(Equip.Equip):
	"""
	武器基类
	"""
	def __init__(self, srcData):
		"""
		"""
		Equip.Equip.__init__(self, srcData)

	def getDictFromObj(self):
		"""
		转化为字典打包传输或保存到数据库
		"""
		return Equip.Equip.getDictFromObj(self)

	def onWield(self, owner, update = True):
		"""
		装备完成
		"""
		Equip.Equip.onWield(self, owner)
		owner.onWeaponWield(self)
	
	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		Equip.Equip.onUnWield(self, owner)
		owner.onWeaponUnWield(self)

	def getEquipPart(self):
		"""
		获取装备部位,武器
		"""
		return ItemTypeEnum.EQUIP_WEAPON
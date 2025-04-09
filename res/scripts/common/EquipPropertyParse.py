# -*- coding: utf-8 -*-

#common
import KBEDebug
import ItemTypeEnum
import LoadModule
import Item.EquipBaseProperty

class EquipPropertyLoad:
	def __init__(self):
		self.attackproperties = Item.EquipBaseProperty.Datas

	def getDataByID(self, id):
		if id in self.attackproperties:
			return self.attackproperties[id]
		return {}

g_EquipPropertyLoadInst = EquipPropertyLoad()




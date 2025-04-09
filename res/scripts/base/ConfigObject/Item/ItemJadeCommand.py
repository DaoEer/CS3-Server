# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemBase as ItemBase

class ItemJadeCommand(ItemBase.ItemBase):
	"""
	玲珑玉令
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemBase.ItemBase.__init__(self, srcData)
		self.dynamicData = {"jadeLevel" : 1, "isValid" : 1}
		
	def setValid( self, owner, isValid ):
		"""设置有效性"""
		self.dynamicData["isValid"] = isValid
		owner.updateOneDataToClient("isValid", self.dynamicData["isValid"], self)
		
	def getJadeLevel( self ):
		""""""
		return self.dynamicData["jadeLevel"]
		
	def unGradeJade(self, owner):
		"""升级玲珑玉令"""
		self.dynamicData["jadeLevel"] += 1
		return self.dynamicData["jadeLevel"]
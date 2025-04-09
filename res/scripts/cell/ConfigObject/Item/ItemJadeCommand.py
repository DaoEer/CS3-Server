# -*- coding: utf-8 -*-

import KBEDebug
import csdefine
import Functions
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
		
	def setOwner(self, player):
		"""
		设置拥有者DBID
		"""
		ItemBase.ItemBase.setOwner(self, player)
		player.occupyLHMJSpace( csdefine.SPACE_TYPE_PUBLIC, {csdefine.LHMJ_BUIILD_LING_QUAN: self.dynamicData["jadeLevel"]})
		
	def setValid( self, owner, isValid ):
		"""设置有效性"""
		self.dynamicData["isValid"] = isValid
		owner.updateOneDataToClient("isValid", self.dynamicData["isValid"], self)
		if isValid:
			owner.occupyLHMJSpace( csdefine.SPACE_TYPE_PUBLIC, {csdefine.LHMJ_BUIILD_LING_QUAN: self.dynamicData["jadeLevel"]})
		
	def getJadeLevel( self ):
		""""""
		return self.dynamicData["jadeLevel"]
		
	def setJadeLevel( self, owner, level ):
		"""设置等级"""
		self.dynamicData["jadeLevel"] = level
		if owner:
			owner.updateOneDataToClient("jadeLevel", self.dynamicData["jadeLevel"], self)
		
	def unGradeJade(self, owner):
		"""升级玲珑玉令"""
		self.dynamicData["jadeLevel"] += 1
		owner.updateOneDataToClient("jadeLevel", self.dynamicData["jadeLevel"], self)
		
	def getDynamicDataForClient(self, entity ):
		return Functions.toJsonString( self.dynamicData )
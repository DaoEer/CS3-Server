# -*- coding: utf-8 -*-

import KBEDebug
import ItemTypeEnum
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import csdefine

class Facade(ItemUse.ItemUse):
	"""
	外观基类
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)
		self.modelSources = srcData.get("Param1", "")	#模型编号
		self.dynamicData["lifeTime"] = srcData.get("lifeTime",0)
		self.dynamicData.update({"lifeTime":self.dynamicData["lifeTime"]})
		
	
	def checkWearClasses(self, owner):
		"""
		检测穿戴职业
		"""
		return True

	def checkWearGender(self, owner):
		"""
		检测穿戴性别
		"""
		return True

	def canWear(self, owner):
		"""
		能否穿戴
		"""
		if owner.actionForbidSign( csdefine.ACTION_FORBID_USE_ITEM ):
			return False
		if not self.checkWearClasses(owner): return False
		if not self.checkWearGender(owner):	return False
		return True


	def Wear(self, owner, update = True):
		"""
		外观道具
		@param update:卸载模型是否生效
		@type update: bool
		"""
		if not self.canWear(owner):		
			return False

		self.onWear(owner)

		return True


	def onWear(self, owner, update = True):
		"""
		装备完成
		"""
		pass
	
	def unWear(self, owner, update = True):
		"""
		卸下道具
		@param update:卸载模型是否生效
		@type update: bool
		"""
		self.onUnWear(owner)

	def onUnWear(self, owner):
		"""
		卸下道具完成
		"""
		pass

	def getWearPart(self):
		"""
		获取外观部位
		"""
		return 0
	
	def isFacade( self ):
		"""
		判断是否是外观
		"""
		return True

	def getWearOrder(self):
		"""
		获取外观的ItemOrder
		"""
		return self.getWearPart()
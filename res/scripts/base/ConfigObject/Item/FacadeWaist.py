# -*- coding: utf-8 -*-

import KBEDebug
import ItemTypeEnum
import ConfigObject.Item.Facade as Facade
import Functions
import csdefine

class FacadeWaist(Facade.Facade):
	"""
	腰带
	"""
	def __init__(self, srcData):
		"""
		"""
		Facade.Facade.__init__(self, srcData)
	
	def onWear(self, owner, update = True):
		"""
		穿戴完成
		"""
		Facade.Facade.onWear(self,owner)
		#owner.onSuitsWield(self)
	
	def onUnWear(self, owner):
		"""
		卸下道具完成
		"""
		Facade.Facade.onUnWear(self,owner)
		#owner.onSuitsUnWield(self)

	def getWearPart(self):
		"""
		获取外观部位,帽子
		"""
		return ItemTypeEnum.FACADE_WAIST

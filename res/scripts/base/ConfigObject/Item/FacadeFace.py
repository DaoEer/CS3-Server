# -*- coding: utf-8 -*-

import KBEDebug
import ItemTypeEnum
import ConfigObject.Item.Facade as Facade
import Functions
import csdefine

class FacadeFace(Facade.Facade):
	"""
	捏脸
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
		获取外观部位,捏脸
		"""
		return ItemTypeEnum.FACADE_FACE

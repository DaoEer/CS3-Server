# -*- coding: utf-8 -*-
#
"""
"""
import csconst
import json
import Singleton

import KBEngine
import KBEDebug
import LoadModule
	
class StoreConfigLoader( Singleton.Singleton ):
	"""
	"""
	def __init__( self ):
		self._datas = {}
		self._Types = []

	def loadStoreConfig( self ):
		"""
		"""
		datas = LoadModule.openJsonCfg("Store/StoreConfig.json")
		for d in datas:
			id = d["ID"]
			if id in self._datas:
				KBEDebug.ERROR_MSG("Goods[%d] has exists" %(id))
				continue
			
			self._datas[id] = d
			
			if [d["GoodsType"], d["ItemType"]] not in self._Types:
				self._Types.append([d["GoodsType"], d["ItemType"]])
		
	def getGoodsByID(self, id):
		"""
		"""
		return self._datas.get(id, None)
		
	def getAllType(self):
		return self._Types
		
		
g_storeCfgLoader = StoreConfigLoader()
g_storeCfgLoader.loadStoreConfig()
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
	
class XiuWeiLoader( Singleton.Singleton ):
	"""
	"""
	def __init__( self ):
		self._roleXiuweiDatas = {}

	def loadXiuWei( self ):
		"""
		"""
		xiuWeiDatas = LoadModule.openJsonCfg("Xiuwei/RoleXiuweiCfg.json")
		for level, xiuweiData in xiuWeiDatas.items():
			tempDict = {}
			for key, value in xiuweiData.items():
				if key in ["stage_taoism", "stage_demon", "stage_layers"]:
					continue
				tempDict[key] = value
			self._roleXiuweiDatas[int(level)] = tempDict
			
	def getXiuWeiByLevel(self, level):
		"""
		"""
		if level not in self._roleXiuweiDatas: return None
		return self._roleXiuweiDatas.get(level)
		
		
g_xiuWeiLoader = XiuWeiLoader()
g_xiuWeiLoader.loadXiuWei()
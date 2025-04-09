# -*- coding:utf-8 -*-

from KBEDebug import *



class XiuweiLoader:
	_instance = None
	
	def __init__( self ):
		assert XiuweiLoader._instance is None
		self._roleXiuweiDatas = {}
		self._roleJingjieDatas = {}
		self._monsterXiuweiDatas = {}
		
	@staticmethod
	def instance():
		if XiuweiLoader._instance is None:
			XiuweiLoader._instance = XiuweiLoader()
		return XiuweiLoader._instance
		
	def init( self, rConfigDatas, mConfigDatas, rJingjieConfigDatas ):
		for level, xiuweiData in rConfigDatas.items():
			tempDict = {}
			for key, value in xiuweiData.items():
				if key in ["stage_taoism", "stage_demon", "stage_layers"]:
					continue
				tempDict[key] = value
			self._roleXiuweiDatas[int(level)] = tempDict

		for level, jingjieData in rJingjieConfigDatas.items():
			JingjieDict = {}
			for key, value in jingjieData.items():
				if key in ["stage_taoism", "stage_demon", "stage_layers"]:
					continue
				JingjieDict[key] = value
			self._roleJingjieDatas[int(level)] = JingjieDict
			
		for level, xiuwei in mConfigDatas.items():
			self._monsterXiuweiDatas[int(level)] = xiuwei
			
	def getRoleXiuweiLevel( self, player ):
		"""
		获取玩家对应的修为
		"""
		for xiuweiLevel, xiuweiData in self._roleXiuweiDatas.items():
			if player.getLevel() < xiuweiData["playerLevel"] or player.getXiuwei() < xiuweiData["xiuwei"]:
				return max( 1, xiuweiLevel - 1 )
		return 1

	def getRoleJingjieLevel( self, player ):
		"""
		获取玩家对应的境界
		"""
		for jingjieLevel, xiuweiLevel in self._roleJingjieDatas.items():
			if player.getXiuweiLevel() < xiuweiLevel["xiuweiLevel"]:
				return max( 1, jingjieLevel - 1 )
		return 1
		
	def getMonsterXiuwei( self, level ):
		"""获取怪物的修为"""
		return self._monsterXiuweiDatas.get( level, 1 )

	def getMonsterXiuweiLevel( self, xiuweiAttr ):
		"""获取怪物境界"""
		if xiuweiAttr < 0.8:
			return 1
		elif xiuweiAttr < 1:
			return 2
		elif xiuweiAttr < 1.2:
			return 3
		elif xiuweiAttr < 3:
			return 4
		elif xiuweiAttr < 10:
			return 5
		else:
			return 6

	def getRoleXiuWeiData( self, level ):
		"""
		获得玩家的修为
		"""
		return self._roleXiuweiDatas.get(level,None)

g_XiuweiMgr = XiuweiLoader.instance()

# -*- coding: utf-8 -*-


# engine
import Math

# python
import random

# script
import KST
from ObjectScript.SpawnPoint.SpawnBase import SpawnBase


"""多个刷新点，随机 刷几个"""
class SpawnPointRandomCatalog( SpawnBase ):
	def __init__( self ):
		SpawnBase.__init__( self )
		self.groupIndex = 0			# 第几组
		self.childPoint ={}			# {index : SpawnpointRandom}
		
	def initData( self, spaceEntity, spawnDatas ):
		SpawnBase.initData( self, spaceEntity, spawnDatas )
		self.groupIndex = spawnDatas["properties"]["spawnIndex"]
		for childIndex, child in spawnDatas["child"].items():
			child["properties"]["scriptID"] = child["scriptID"]
			child["properties"]["spawnIndex"] = childIndex
			child["properties"]["spawnPos"] = Math.Vector3(child["position"])
			child["properties"]["position"] = Math.Vector3(child["position"])
			child["properties"]["direction"] = Math.Vector3(child["direction"])
			
			from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
			spawnPoint = g_spawnPointFactory.createSpawnPoint( spaceEntity, child["EntityType"], child )
			if spawnPoint:
				spawnPoint.spawnDict["delaySpawn"] = 0							# 这个必须是0，减少设计的复杂度
				self.childPoint.update( { childIndex : spawnPoint } )
		
	def getSpawnIndex( self, spaceEntity ):
		"""获取已经刷新的index"""
		sList = []
		for spawnInfo in spaceEntity.spawnInfo.values():
			if spawnInfo[0] == self.groupIndex:
				sList.append( spawnInfo[1] )
		return sList
		
	def spawnCreateEntity( self, spaceEntity, params = {} ):
		"""
		"""
		entitys = []
		initRandom = self.spawnDict["InitRandom"]
		randNum = min(random.randint(initRandom[0], initRandom[1]),len(self.childPoint))
		randIndexs = random.sample(list(self.childPoint), randNum)
		for index in randIndexs:
			entity = self.childPoint[index].spawnCreateEntity( spaceEntity, {} )
			entitys.append(entity)
			
			spaceEntity.registerSpawnInfo(entity.id, (self.groupIndex, index))

		return entitys
		
	def onGameObjectDie( self, spaceEntity, spawnInfo ):
		"""
		virtual method
		"""
		if self.spawnDict.get("redivious", -1 ) >= 0:
			spaceEntity.addTimerCallBack( self.spawnDict["redivious"], "onRediviousChildMonsterCB", ( spawnInfo, ) )
		
	def onRediviousChildMonsterCB( self, spaceEntity, spawnInfo ):
		""""""
		sList = self.getSpawnIndex( spaceEntity )
		initRandom = self.spawnDict["DieRandom"]
		randNum = min(random.randint(initRandom[0], initRandom[1]),len(self.childPoint) - len( sList ))
		childList = []
		for index in self.childPoint.keys():
			if not index in sList:
				childList.append(index)
		randIndexs = random.sample(childList, randNum)
		for index in randIndexs:
			entity = self.childPoint[index].spawnCreateEntity( spaceEntity, {} )
			
			spaceEntity.registerSpawnInfo(entity.id, (self.groupIndex, index))
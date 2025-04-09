# -*- coding: utf-8 -*-


# engine

# python

# script
import csdefine
import KBEngine
import KBEDebug
import Const
import KST
import Math
from SmartImport import smartImport
from ObjectScript.SpawnPoint.SpawnPointNormal import SpawnPointNormal
from ObjectScript.SpawnPoint.SpawnPointGroup import SpawnPointGroup
from ObjectScript.SpawnPoint.SpawnPointClusterCtrl import SpawnPointClusterCtrl
from ObjectScript.SpawnPoint.SpawnPointMovingPlatform import SpawnPointMovingPlatform
from ObjectScript.SpawnPoint.SpawnPointTeleportStone import SpawnPointTeleportStone
from ObjectScript.SpawnPoint.SpawnPointTong import SpawnPointTong
from ObjectScript.SpawnPoint.SpawnPointRandom import SpawnPointRandom
from ObjectScript.SpawnPoint.SpawnPointRandomCatalog import SpawnPointRandomCatalog
from ObjectScript.SpawnPoint.SpawnPointRandomExtActivity import SpawnPointRandomExtActivity


class SpawnPointFactory:
	def __init__( self ):
		self.spawnInfo = {}								# { space scriptID : { index : SpawnPointBase } }
		
	def getSpawnPointFunc( self, entityType ):
		try:
			func = CREATE_SPAWN_POINT_MAPPING[entityType]
			return func
		except:
			KBEDebug.ERROR_MSG( "Can not find entityType(%s)" %entityType )
			return None
		
	def initSpawnPoint( self, spaceEntity, methodName ):
		"""
		"""
		spawnDatas = smartImport( "GameObject.SpaceObject.SpawnFile." + methodName + ":" + "Datas" )
		self.spawnInfo[spaceEntity.scriptID] = {}
		
		for index, spawnData in spawnDatas.items():
			lineNumber = spawnData["lineNumber"]
			if lineNumber != 0:	#刷新点线号与副本线号不一致则不加载
				continue
			entityType = spawnData["EntityType"]
			spawnData["properties"]["scriptID"] = spawnData["scriptID"]
			spawnData["properties"]["spawnIndex"] = index
			spawnData["properties"]["spawnPos"] = Math.Vector3(spawnData["position"])
			spawnData["properties"]["position"] = Math.Vector3(spawnData["position"])
			spawnData["properties"]["direction"] = Math.Vector3(spawnData["direction"])
			
			if spawnData["scriptID"].startswith('2'):				
				spaceEntity.monsterSpawnIndexs.append(index)
			point = self.createSpawnPoint( spaceEntity, entityType, spawnData )
			self.spawnInfo[spaceEntity.scriptID].update( { index : point } )
		for point in self.spawnInfo[spaceEntity.scriptID].values():
			point.onSpaceSpawnPointLoadOver( spaceEntity )
		spaceEntity.onSpaceSpawnPointLoadOver()

	def initSpawnPointTrainSoldierGround( self,spaceEntity, methodName, trainSoldierGroundDict ):
		"""
		练兵场数据
		"""
		spawnDatas = smartImport( "GameObject.SpaceObject.SpawnFile." + methodName + ":" + "Datas" )
		self.spawnInfo[spaceEntity.scriptID] = {}
		
		for index, spawnData in spawnDatas.items():
			lineNumber = spawnData["lineNumber"]
			if lineNumber != 0:	#刷新点线号与副本线号不一致则不加载
				continue

			entityType = spawnData["EntityType"]
			spawnData["properties"]["scriptID"] = spawnData["scriptID"]
			spawnData["properties"]["spawnIndex"] = index
			spawnData["properties"]["spawnPos"] = Math.Vector3(spawnData["position"])
			spawnData["properties"]["position"] = Math.Vector3(spawnData["position"])
			spawnData["properties"]["direction"] = Math.Vector3(spawnData["direction"])
			groupIndex = spawnData.get("group",-1)
			if spawnData["scriptID"].startswith('2'):				
				spaceEntity.monsterSpawnIndexs.append(index)
			if groupIndex in trainSoldierGroundDict:
				spawnData["properties"].update(trainSoldierGroundDict[groupIndex])
			point = self.createSpawnPoint( spaceEntity, entityType, spawnData )
			self.spawnInfo[spaceEntity.scriptID].update( { index : point } )
		for point in self.spawnInfo[spaceEntity.scriptID].values():
			point.onSpaceSpawnPointLoadOver( spaceEntity )
		spaceEntity.onSpaceSpawnPointLoadOver()

	def initSpawnPointNPCPoint( self, spaceEntity, methodName, pointDataDict ):
		"""
		帮会争霸据点数据
		"""
		spawnDatas = smartImport( "GameObject.SpaceObject.SpawnFile." + methodName + ":" + "Datas" )
		self.spawnInfo[spaceEntity.scriptID] = {}
		
		for index, spawnData in spawnDatas.items():
			lineNumber = spawnData["lineNumber"]
			if lineNumber != 0:	#刷新点线号与副本线号不一致则不加载
				continue
			entityType = spawnData["EntityType"]
			spawnData["properties"]["scriptID"] = spawnData["scriptID"]
			spawnData["properties"]["spawnIndex"] = index
			spawnData["properties"]["spawnPos"] = Math.Vector3(spawnData["position"])
			spawnData["properties"]["position"] = Math.Vector3(spawnData["position"])
			spawnData["properties"]["direction"] = Math.Vector3(spawnData["direction"])
			groupIndex = spawnData.get("group",-1)
			if spawnData["scriptID"].startswith('2'):				
				spaceEntity.monsterSpawnIndexs.append(index)

			if groupIndex in pointDataDict:
				spawnData["properties"].update(pointDataDict[groupIndex])
			point = self.createSpawnPoint( spaceEntity, entityType, spawnData )
			self.spawnInfo[spaceEntity.scriptID].update( { index : point } )
		for point in self.spawnInfo[spaceEntity.scriptID].values():
			point.onSpaceSpawnPointLoadOver( spaceEntity )
		spaceEntity.onSpaceSpawnPointLoadOver()
		
	def createSpawnPoint( self, spaceEntity, entityType, spawnData ):
		"""
		创建SpawnPoint
		"""
		spawnFunc = self.getSpawnPointFunc( entityType )
		if not spawnFunc:
			KBEDebug.ERROR_MSG("Creat spawn point err!!Can not find spawnpoint(%s)"%entityType)
			return
		spawnPoint = spawnFunc()
		spawnPoint.initData( spaceEntity, spawnData )
		return spawnPoint
		
	def createSpawnEntityByIndex( self, spaceEntity, index, params = {} ):
		""""""
		entitys = []
		scriptID = spaceEntity.scriptID
		if scriptID in self.spawnInfo and index in self.spawnInfo[scriptID]:
			entity = self.spawnInfo[scriptID][index].spawnCreateEntity( spaceEntity, params )
			entitys.append( entity )
		return entitys
			
	def createSpawnEntityByScriptID( self, spaceEntity, scriptID, params = {} ):
		""""""
		entitys = []
		spaceScriptID = spaceEntity.scriptID
		if spaceScriptID in self.spawnInfo:
			for point in self.spawnInfo[spaceScriptID].values():
				if str(scriptID) == point.getEntityScriptID():
					entity = point.spawnCreateEntity( spaceEntity, params )
					entitys.append( entity )
		return entitys
		
	def createSpawnEntityBySpawnType( self, spaceEntity, spawnType ):
		""""""
		entitys = []
		spaceScriptID = spaceEntity.scriptID
		if spaceScriptID in self.spawnInfo:
			for point in self.spawnInfo[spaceScriptID].values():
				entity = point.spawnCreateEntityBySpawnType( spaceEntity, spawnType )
				if entity:
					entitys.append( entity )
		return entitys
		
	def onGameObjectDie( self, spaceEntity, spawnInfo ):
		""""""
		scriptID = spaceEntity.scriptID
		index = spawnInfo[0]
		if scriptID in self.spawnInfo:
			point = self.spawnInfo[scriptID][index]
			point.onGameObjectDie( spaceEntity, spawnInfo )
			
	def onRediviousChildMonsterCB( self, spaceEntity, spawnInfo ):
		"""台子上的怪物复活"""
		scriptID = spaceEntity.scriptID
		if scriptID in self.spawnInfo:
			index = spawnInfo[0]
			point = self.spawnInfo[scriptID][index]
			point.onRediviousChildMonsterCB( spaceEntity, spawnInfo )
		
		
CREATE_SPAWN_POINT_MAPPING = { 
						"SpawnPointNormal"	:	SpawnPointNormal,
						"NPC"				:	SpawnPointNormal,								# 修改刷新点第二个版本导致
						"SpawnPointGroup"	:		SpawnPointGroup,
						"SpawnPointClusterCtrl"	:	SpawnPointClusterCtrl,
						"MovingPlatform"	:	SpawnPointMovingPlatform,						# 移动平台刷新
						"TeleportStone"		:   SpawnPointTeleportStone,						# 传送石刷新
						"SpawnPointTong"	:	SpawnPointTong,									# 帮会领地刷新
						"SpawnPointRandom"	:	SpawnPointRandom,							# 随机刷怪
						"SpawnPointRandomCatalog"	:	SpawnPointRandomCatalog,			# 随机刷怪
						"SpawnPointRandomExtActivity":SpawnPointRandomExtActivity				# 活动开启，开始随机刷怪
						}
		
g_spawnPointFactory = SpawnPointFactory()
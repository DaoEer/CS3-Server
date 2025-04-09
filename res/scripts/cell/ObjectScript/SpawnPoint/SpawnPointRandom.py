# -*- coding: utf-8 -*-


# engine
import Math

# python
import random

# script
import KST
from ObjectScript.SpawnPoint.SpawnBase import SpawnBase


"""根据权重随机刷怪（多个scriptID，随机刷一个）"""
class SpawnPointRandom( SpawnBase ):
	def __init__( self ):
		SpawnBase.__init__( self )
		
	def spawnCreateEntity( self, spaceEntity, params = {} ):
		"""
		"""
		properties = dict( self.spawnDict["properties"] )
		properties.update( params )
		
		total = int(sum( self.spawnDict["spawnWeight"] ))
		randomNum = random.randrange(0, total)
		index = 0
		for i, weight in enumerate( self.spawnDict["spawnWeight"]):
			if weight >= randomNum:
				index = i
				break
			else:
				randomNum -= weight
		
		scriptID = self.spawnDict["scriptIDs"][index]
		position = properties["position"]
		direction = properties["direction"]
		
		properties["scriptID"] = scriptID
		randPro = ["randomWalkRange", "patrolPathNode", "patrolList"]
		for pro in randPro:
			if pro in self.spawnDict:
				properties[pro] = self.spawnDict[pro][index]
		
		
		if scriptID == "":
			KBEDebug.ERROR_MSG( "====>>>Space( %s ), spawnFile Error!!( %s )"%( spaceEntity.scriptID, str( properties ) ) )
			
		properties.update({"spawnDir" :self.spawnDict["direction"]})
		if "spawnPos" not in properties:
			properties.update({"spawnPos" :self.spawnDict["position"]})
		
		entity = KST.g_objFactory.createEntity( scriptID, spaceEntity, tuple(Math.Vector3(position)), direction, properties )

		if entity:
			spaceEntity.registerSpawnInfo( entity.id, ( self.getSpawnIndex(), ) )

		return entity
# -*- coding: utf-8 -*-


# engine

# python
import random

# script
from ObjectScript.SpawnPoint.SpawnPointRandom import SpawnPointRandom

"""活动开启时，根据权重随机刷怪"""

class SpawnPointRandomExtActivity( SpawnPointRandom ):
	def __init__( self ):
		SpawnPointRandom.__init__( self )
		
	def spawnCreateEntity( self, spaceEntity, params = {} ):
		"""
		"""
		if spaceEntity and spaceEntity.openActivitySpawn:
			return SpawnPointRandom.spawnCreateEntity( spaceEntity, params )

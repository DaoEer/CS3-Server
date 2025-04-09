# -*- coding: utf-8 -*-


# engine

# python

# script
from ObjectScript.SpawnPoint.SpawnBase import SpawnBase

class SpawnPointGroup( SpawnBase ):
	"""
	带有批次（group）属性
	"""
	def __init__( self ):
		SpawnBase.__init__( self )
		self.group = 0
	
	def initData( self, spaceEntity, spawnDatas ):
		SpawnBase.initData( self, spaceEntity, spawnDatas )
		self.group = spawnDatas["group"]
		self.spawnDict["properties"]["group"] = spawnDatas["group"]
		spaceEntity.addGroupSpawnPoint( self )

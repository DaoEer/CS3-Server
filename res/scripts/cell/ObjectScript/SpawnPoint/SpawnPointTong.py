# -*- coding: utf-8 -*-


# engine

# python

# script
import KBEDebug
from ObjectScript.SpawnPoint.SpawnPointNormal import SpawnPointNormal

class SpawnPointTong( SpawnPointNormal ):
	def __init__( self ):
		SpawnPointNormal.__init__( self )

	def spawnCreateEntity( self, spaceEntity, params = {} ):
		"""
		"""
		try:
			params["ownTongDBID"] = spaceEntity.tongDBID
		except:
			KBEDebug.ERROR_MSG("SpawnPoint Create Tong entity err!can not find space(%s) tongDBID"%spaceEntity.__class__.__name__)
			return
		SpawnPointNormal.spawnCreateEntity( self, spaceEntity, params )
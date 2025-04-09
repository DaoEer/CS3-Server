# -*- coding: utf-8 -*-

import KBEDebug
from CoreObject import MgrPersistentObject
import KST


class SpawnManager( MgrPersistentObject.MgrPersistentObject ):
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		
		self.spaceInfo = {}
		self.spawnTimer = 0
		self.onCompleteInit()

#-----------------Base call----------------------------------------
	def registerSpace( self, componentid, spaceBase ):
		"""
		"""
		self.spaceInfo.setdefault(componentid, [])
		self.spaceInfo[componentid].append( spaceBase )
		
		if self.spawnTimer == 0:
			KBEDebug.DEBUG_MSG( "Start spawn entity." )
			self.spawnTimer = self.addTimer( 0.1, 0.1, 0 )
	
	def onTimer( self, id, userArg ):
		"""
		"""
		for id, _ in self.spaceInfo.items():
			if len(self.spaceInfo[id]) > 0:
				spaceBase = self.spaceInfo[id].pop( 0 )
				spaceBase.createSpawnPoint()
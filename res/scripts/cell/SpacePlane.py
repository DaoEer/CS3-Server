# -*- coding: utf-8 -*-

import Const
import KBEDebug
from CoreObject.SpaceObject import SpaceObject

class SpacePlane( SpaceObject ):
	def __init__( self ):
		SpaceObject.__init__( self )
	
	def addEntityRecord( self, scriptID, entityID ):
		"""
		virtual method
		记录entity（所有继承于NPCBaseObject的entity）ID
		"""
		if scriptID in self.entityRecord:
			self.entityRecord[ scriptID ].append( entityID )
		else:
			self.entityRecord[ scriptID ] = [ entityID ]
	
	def delEntityRecord( self, scriptID, entityID ):
		"""
		virtual method
		删除entity记录
		"""
		if scriptID not in self.entityRecord:
			return
		if entityID not in self.entityRecord[ scriptID ]:
			return
		self.entityRecord[ scriptID ].remove( entityID )
		if len( self.entityRecord[ scriptID ] ) == 0:
			self.entityRecord.pop( scriptID )
	
	def getEntityRecord( self, scriptID ):
		"""
		获取某scriptID的entity
		"""
		return self.entityRecord.get( scriptID, [] )
	
	def getAllEntityRecord( self ):
		"""
		"""
		return self.entityRecord

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		if scriptID in self.entityMailBoxRecord:
			self.entityMailBoxRecord[scriptID].append(entityMailBox)
		else:
			self.entityMailBoxRecord[scriptID] = [entityMailBox]

	def delEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		删除entityMailBox 记录
		"""
		if scriptID not in self.entityMailBoxRecord:
			return
		if entityMailBox not in self.entityMailBoxRecord[scriptID]:
			return
		self.entityMailBoxRecord[scriptID].remove(entityMailBox)
		if len( self.entityMailBoxRecord[scriptID] ) == 0:
			self.entityMailBoxRecord.pop( scriptID )

	def getEntityMailBoxRecord( self, scriptID ):
		"""
		获取某scriptID的entity
		"""
		return self.entityMailBoxRecord.get( scriptID, [] )

	def getAllEntityMailBoxRecord( self ):
		"""
		"""
		return self.entityMailBoxRecord
			
	def getSpaceStatisticsNum( self, entryIndex ):
		"""获取统计数值"""
		if self.spaceStatistics:
			return self.spaceStatistics.getSpaceStatisticsNum( entryIndex )
		else:
			KBEDebug.ERROR_MSG("Space getSpaceStatisticsNum err!")
		return 0
			
	def getEntityDynamicPosBigMapShow( self, player, scriptID ):
		"""获取entity在大地图的位置"""
		entityIDs = self.getCurrentSpace().getEntityRecord(scriptID)
		entities=[]
		for entityID in entityIDs:
			e =KBEngine.entities.get(entityID, None)
			if e:
				entities.append(e)
		return entities
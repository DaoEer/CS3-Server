# -*- coding: utf-8 -*-

import KBEngine

class EntityPool( object ):
	"""
	"""
	def __init__( self, entityType ):
		"""
		"""
		self.entities = []
		self.entityType = entityType
	
	def get( self ):
		"""
		获取一个entity
		"""
		while True:
			if self.entities:
				entity = KBEngine.entities.get( self.entities.pop(0) )
				if entity:
					return entity
				continue
			else:
				return KBEngine.createEntityLocally( self.entityType, {} )
		return None # unreachable
	
	def put( self, entity ):
		"""
		放回一个entity
		"""
		assert entity.__class__.__name__ == self.entityType
		if not entity.isDestroyed:
			self.entities.append( entity.id )

	def releaseAll( self ):
		"""
		释放所有在缓冲区中的entity
		"""
		for eid in self.entities:
			entity = KBEngine.entities.get( eid )
			entity and entity.destroy()
		self.entities.clear()

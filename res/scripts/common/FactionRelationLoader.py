# -*- coding:utf-8 -*-

import csdefine

class FactionRelationLoader:
	_instance = None
	
	def __init__( self ):
		assert FactionRelationLoader._instance is None
		self._datas = {}
	
	@staticmethod
	def instance():
		if FactionRelationLoader._instance is None:
			FactionRelationLoader._instance = FactionRelationLoader()
		return FactionRelationLoader._instance
	
	def init( self, configDatas ):
		for dDict in configDatas:
			key = (dDict["FactionA"], dDict["FactionB"])
			self._datas[ key ] = dDict["Relation"]
	
	def getRelation( self, factionA, factionB ):
		"""
		获取势力关系
		"""
		if factionA == 0 or factionB == 0:
			return csdefine.COMBAT_RELATION_DEFAULT
		
		if factionA == factionB:
			return csdefine.COMBAT_RELATION_NORMAL
		
		for key, relFlag in self._datas.items():
			if set(key) == set( (factionA, factionB) ):
				if relFlag == 0:	#友好
					return csdefine.COMBAT_RELATION_NORMAL
				elif relFlag == 1:	#敌对
					return csdefine.COMBAT_RELATION_ENEMY
				break
		
		return csdefine.COMBAT_RELATION_DEFAULT

g_FactionRelationLoader = FactionRelationLoader.instance()
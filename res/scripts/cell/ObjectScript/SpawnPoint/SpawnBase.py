# -*- coding: utf-8 -*-


# engine
import KBEngine

import KBEDebug
# python
import random
import Math

# script
import KST
import csdefine
from ObjectScript.ObjectScriptBase.GameScript import GameScript

class SpawnBase( GameScript ):
	def __init__( self ):
		GameScript.__init__( self )
		self.spawnDict = {}
		self.isDarkEntity = False		#是否是暗怪
		
	def initData( self, spaceEntity, spawnDatas ):
		GameScript.initData( self, spawnDatas )
		self.spawnDict = spawnDatas
		self.spawnDict["properties"]["createType"] = csdefine.ENTITY_CREATE_TYPE_SPAWN_POINT
		self.isDarkEntity = spawnDatas.get( "isDarkEntity", 0 )
	
	def getEntityScriptID( self ):
		return self.spawnDict.get( "scriptID", "" )
		
	def getSpawnIndex( self ):
		return self.spawnDict["properties"]["spawnIndex"]
	
	def spawnCreateEntity( self, spaceEntity, params = {} ):
		"""
		"""
		properties = dict( self.spawnDict["properties"] )
		properties.update( params )
		
		position = properties["position"]
		direction = properties["direction"]
		scriptID = properties["scriptID"]
		if scriptID == "":
			KBEDebug.ERROR_MSG( "====>>>Space( %s ), spawnFile Error!!( %s )"%( spaceEntity.scriptID, str( properties ) ) )
			
		properties.update({"spawnDir" :self.spawnDict["direction"]})
		if "spawnPos" not in properties:
			properties.update({"spawnPos" :self.spawnDict["position"]})
		
		entity = KST.g_objFactory.createEntity( scriptID, spaceEntity, tuple(Math.Vector3(position)), direction, properties )

		if entity:
			self.entityID = entity.id
			spaceEntity.registerSpawnInfo( self.entityID, ( self.getSpawnIndex(), ) )

		return entity
		
	def spawnReplaceEntity( self, spaceEntity, scriptID ):
		"""
		在此刷新点位置刷指定scriptID的怪物，目前用于刷光效怪
		注：刷此怪时只读取刷新点配置中的位置和朝向属性
		"""
		position = self.spawnDict["position"]
		direction = self.spawnDict["direction"]
		properties = {}
		properties["spawnPos"] = self.spawnDict["position"]
		entity = KST.g_objFactory.createEntity( scriptID, spaceEntity, tuple(Math.Vector3(position)), direction, properties  )
		
	def onSpaceSpawnPointLoadOver( self, spaceEntity ):
		"""
		virtual method
		"""
		if self.isDarkEntity:	#如果是暗怪，副本创建时不刷怪，由其他流程控制刷新
			return
		delayTime = self.spawnDict.get("delaySpawn", 0)
		self.delaySpawn( spaceEntity, delayTime )
		
	def delaySpawn( self, spaceEntity, delayTime ):
		"""
		延迟一定时间刷怪
		"""
		if delayTime <= 0:
			spaceEntity.onRequestSpawnEntity( self.spawnDict["properties"]["spawnIndex"] )
		else:
			spaceEntity.addTimerCallBack( delayTime, "onRequestSpawnEntity", ( self.spawnDict["properties"]["spawnIndex"], ) )
	
	def onGameObjectDie( self, spaceEntity, spawnInfo ):
		"""
		virtual method
		"""
		if self.spawnDict.get("redivious", -1 ) >= 0:
		 	 spaceEntity.addTimerCallBack( self.spawnDict["redivious"], "onRediviousMonsterCB", ( self.spawnDict["properties"]["spawnIndex"], ) )
		
	def spawnCreateEntityBySpawnType( self, spaceEntity, spawnType ):
		"""virtual method"""
		if self.spawnDict["EntityType"] == spawnType:
			delayTime = self.spawnDict.get("delaySpawn", 0)
			self.delaySpawn( spaceEntity, delayTime )

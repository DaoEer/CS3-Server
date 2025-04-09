# -*- coding: utf-8 -*-


# engine
import KBEngine
import Math
import KBEDebug

# python
import random
import Math

# script
# 移动平台刷新点

from ObjectScript.Scene import SceneFactory
from ObjectScript.SpawnPoint.SpawnBase import SpawnBase

class SpawnPointMovingPlatform( SpawnBase ):
	def __init__( self ):
		SpawnBase.__init__( self )
		self.parentIndex = 0
		self.childPoint = {}				# { 1 : SpawnBase,}
		self.childPos = {}					# { 1 : pos, }保存相对坐标
		
	def initData( self, spaceEntity, spawnDatas ):
		SpawnBase.initData( self, spaceEntity, spawnDatas )
		if "index" in spawnDatas and spawnDatas["index"]:
			self.parentIndex = spawnDatas["index"]
			for childIndex, child in spawnDatas["child"].items():
				child["properties"]["scriptID"] = child["scriptID"]
				child["properties"]["spawnIndex"] = childIndex
				child["properties"]["spawnPos"] = Math.Vector3(child["position"])
				child["properties"]["position"] = Math.Vector3(child["position"])
				child["properties"]["direction"] = Math.Vector3(child["direction"])
				
				from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
				spawnPoint = g_spawnPointFactory.createSpawnPoint( spaceEntity, child["EntityType"], child )
				if spawnPoint:
					spawnPoint.spawnDict["delaySpawn"] = 0							# 这个必须是0，减少设计的复杂度
					self.childPoint.update( { childIndex : spawnPoint } )
	
	def onSpaceSpawnPointLoadOver( self, spaceEntity ):
		"""
		virtual method
		"""
		if self.isDarkEntity:	#如果是暗怪，副本创建时不刷怪，由其他流程控制刷新
			return
		delayTime = self.spawnDict.get("delaySpawn", 0)
		if delayTime <= 0:
			spaceEntity.onRequestSpawnEntity( self.spawnDict["properties"]["spawnIndex"] )
		else:
			spaceEntity.addTimerCallBack( delayTime, "onRequestSpawnEntity", ( self.spawnDict["properties"]["spawnIndex"], ) )
			
	def spawnCreateEntity( self, spaceEntity, params = {} ):
		"""
		"""
		selfEntity = self.spawnSelfEntity( spaceEntity, params )
		if selfEntity:
			for childIndex, child in self.childPoint.items():
				pos = Math.Vector3( selfEntity.positionWorldToLocal( child.spawnDict.get("position") ) )
				self.childPos.update( { childIndex : pos } )						# 需要保存相对坐标
				childEntity = child.spawnCreateEntity( spaceEntity, {"parent" : selfEntity, "spawnPos" : pos} )
				
#				childEntity.parent = selfEntity
				# 重新注册覆盖之前的方法，记录台子索引，以及台子上刷新点的索引
				spaceEntity.registerSpawnInfo( childEntity.id, ( self.getSpawnIndex(), childIndex, selfEntity.id ))
				
	def spawnSelfEntity( self, spaceEntity, params = {} ):
		"""
		"""
		properties = dict( self.spawnDict["properties"] )
		properties.update( params )
		
		position = properties["position"]
		direction = properties["direction"]
		scriptID = properties["scriptID"]
		
		properties.update({"spawnDir" :self.spawnDict["direction"]})
		if "spawnPos" not in properties:
			properties.update({"spawnPos" :self.spawnDict["position"]})
		object = SceneFactory.g_SceneFactory.getObject( scriptID )
		if object:
			entity = object.createEntity( spaceEntity, tuple(Math.Vector3(position)), direction, properties )
		else:
			KBEDebug.ERROR_MSG( "Space(%s) Create Can not find scriptID(%s), please check!!" %( spaceEntity.getCurrentSpaceScriptID(),scriptID ) )
			return
		if entity:
			self.entityID = entity.id
			spaceEntity.registerSpawnInfo( self.entityID, ( self.getSpawnIndex(), ) )
		return entity
				
	def onGameObjectDie( self, spaceEntity, spawnInfo ):
		"""
		virtual method
		"""
		if len( spawnInfo ) == 1:				# 支持平台销毁再创建
			redivious = self.spawnDict.get("redivious", -1 )
			if redivious >= 0:
				spaceEntity.addTimerCallBack( self.spawnDict["redivious"], "onRediviousMonsterCB", ( self.spawnDict["properties"]["spawnIndex"], ) )
		else:
			childPoint = self.childPoint[spawnInfo[1]]
			redivious = childPoint.spawnDict.get("redivious", -1 )
			if redivious >= 0:
				spaceEntity.addTimerCallBack( redivious, "onRediviousChildMonsterCB", (spawnInfo,))
			
	def onRediviousChildMonsterCB( self, spaceEntity, spawnInfo ):
		childIndex = spawnInfo[1]
		parentID = spawnInfo[2]
		
		selfEntity = KBEngine.entities[parentID]
		childPoint = self.childPoint[childIndex]
		local = self.childPos[childIndex]
		pos = Math.Vector3( selfEntity.positionLocalToWorld(local) )
		childEntity = childPoint.spawnCreateEntity( spaceEntity, {"position" :pos,"parent" : selfEntity, "spawnPos" : local} )
#		childEntity.parent = selfEntity
		# 重新注册覆盖之前的方法，记录台子索引，以及台子上刷新点的索引
		spaceEntity.registerSpawnInfo( childEntity.id, spawnInfo )
		
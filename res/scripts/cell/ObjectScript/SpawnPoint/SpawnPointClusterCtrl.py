# -*- coding: utf-8 -*-

import random
import Math
import KST
import KBEngine
import KBEDebug
import FightRuleMgr
from ObjectScript.SpawnPoint.SpawnBase import SpawnBase

class SpawnPointClusterCtrl( SpawnBase ):
	"""
	刷新点：怪物集群刷新、统一警戒（CST-1019）
	实现方式：刷新点刷警戒陷阱（目前只支持圆形陷阱），同时刷新集群怪；玩家进陷阱->陷阱通知刷新点->刷新点给所有怪物加敌人。
	"""
	def __init__( self ):
		SpawnBase.__init__( self )
		self.monsterList = []
		self.spawnedPosIndex = []	#已经刷有怪物的位置

	def addEnemyToAllEntity( self, spaceEntity, enemyID ):
		"""
		给所有怪物添加敌人
		"""
		enemyEntity = KBEngine.entities.get( enemyID )
		if not enemyEntity:
			return
		
		for id in self.monsterList:
			monster = KBEngine.entities.get( id )
			if monster:
				if monster.canBuildEnemyRelation( enemyEntity ):
					FightRuleMgr.g_fightMgr.buildEnemyRelation( monster, enemyEntity )

	def spawnCreateEntity( self, spaceEntity, params = {} ):
		"""
		"""
		scriptID = self.spawnDict["scriptID"]
		position = self.spawnDict["position"]
		direction = self.spawnDict["direction"]
		properties = dict( self.spawnDict["properties"] )
		properties.update( params )
		entity = KST.g_objFactory.createEntity( scriptID, spaceEntity, tuple(Math.Vector3(position)), direction, properties )
		if entity:
			self.entityID = entity.id
			
			from TrapClusterAlert import TrapClusterAlert
			if not isinstance( entity, TrapClusterAlert):
				KBEDebug.ERROR_MSG( "SpawnPointClusterCtrl must config TrapClusterAlert entity!", scriptID )
			else:
				entity.initTriggerCon(  self.spawnDict["triggerCon"] )
		
		self.spawnClusterMonster( spaceEntity )

	def spawnClusterMonster( self, spaceEntity ):
		"""
		刷集群怪
		"""
		if not self.spawnDict["idAndAmount"]:
			return
		
		idAndAmount = {}	#怪物ID和数量
		for tempStr in self.spawnDict["idAndAmount"].split("|"):
			scriptID, amount = tempStr.split(":")
			idAndAmount[ scriptID ] = int( amount )
		
		for id, amount in idAndAmount.items():
			for i in range( amount ):
				self.spawnOneClusterMonster( spaceEntity, id )

	def spawnOneClusterMonster( self, spaceEntity, scriptID ):
		"""
		刷一个集群怪
		"""
		#取一个没刷怪的点，如果都刷怪了就在所有点中随机取一个
		allPosIndex = [ i for i in range( len(self.spawnDict["positionList"]) ) ]
		emptyPosIndex = list( set( self.spawnedPosIndex ) ^ set( allPosIndex ) )
		
		if len(emptyPosIndex) == 0:
			posIndex = random.choice( allPosIndex )
		else:
			posIndex = random.choice( emptyPosIndex )
		
		if posIndex not in self.spawnedPosIndex:
			self.spawnedPosIndex.append( posIndex )
		
		position = self.spawnDict["positionList"][posIndex]
		direction = self.spawnDict["direction"]
		
		properties = dict( self.spawnDict["monsterProp"] )	# 怪物属性
		properties["spawnPos"] = position
		properties["spawnIndex"] = self.getSpawnIndex()
		properties["clusterPosIndex"] = posIndex	#怪物记录自己的刷新位置下标，用于怪物死亡时回收此刷新位置
		entity = KST.g_objFactory.createEntity( scriptID, spaceEntity, tuple(Math.Vector3(position)), direction, properties )
		if entity:
			self.monsterList.append( entity.id )

	def onGameObjectDie( self, spaceEntity, monsterScriptID, monsterID ):
		"""
		virtual method
		"""
		#陷阱不会死亡，只会是集群怪死亡
		monster = KBEngine.entities.get( monsterID )
		if monster:
			if monster.clusterPosIndex >= 0 and monster.clusterPosIndex in self.spawnedPosIndex:
				self.spawnedPosIndex.remove( monster.clusterPosIndex )
		else:
			KBEDebug.ERROR_MSG("Can't find monster when query clusterPosIndex!", spaceEntity.scriptID, self.getSpawnIndex(), monsterScriptID, monsterID )
		
		if self.spawnDict.get("redivious", -1 ) >= 0:
			spawnIndex = self.spawnDict["properties"]["spawnIndex"]
			spaceEntity.addTimerCallBack( self.spawnDict["redivious"], "callSpawnFunction", ( spawnIndex, "spawnOneClusterMonster",(monsterScriptID,) ) )
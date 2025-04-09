# -*- coding: utf-8 -*-

"""
usage:
	SpawnInterface
	
attribute:

KBEngine method:

member function:

callback:
"""

# engine

# python

# script
import os
import KBEDebug
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory

class SpawnInterface:
	def __init__( self ):
		pass
#		self.spawnInfos = []				# { enityID : spawnInfo }
	
	def spawnPointStartLoader( self ):
		"""
		<define method>
		申请加载刷新点
		"""
		if self.inDestroying():
			return
		
		#这里有个坑，如果space的创建速度大于0.1S一个的话，那space的刷新点有可能不会加载。
		self.base.startLoaderSpawnFile(str(os.getenv("KBE_COMPONENTID")))
		
	def registerSpawnInfo( self, entityID, spawnInfo ):
		""""""
		self.spawnInfo.update( {entityID:spawnInfo} )
		
	def unRegisterSpawnInfo( self, entityID ):
		""""""
		if entityID in self.spawnInfo:
			self.spawnInfo.pop( enityID )
		
	def createSpawnPoint( self ):
		"""
		<define method>
		加载刷新点
		"""
		self.getScript().createSpawnPoint( self )
		
	def spawnPointCreateEntityByScriptID( self, scriptID, params = {} ):
		"""
		根据ID刷新Entity
		<define method>
		"""
		return g_spawnPointFactory.createSpawnEntityByScriptID( self, scriptID, params )
		
	def createSpawnEntityBySpawnType( self, spawnType ):
		"""
		根据spawnType刷新Entity
		"""
		return g_spawnPointFactory.createSpawnEntityBySpawnType( self, spawnType )
		
	def onRequestSpawnEntity( self, *args ):
		"""
		刷某个index的怪
		"""
		g_spawnPointFactory.createSpawnEntityByIndex( self, args[0] )
		
	def onMonsterDie( self, monsterScriptID, monsterID ):
		"""
		"""
		if monsterID in self.spawnInfo:
			spawnInfo = self.spawnInfo.pop(monsterID)
			g_spawnPointFactory.onGameObjectDie( self, spawnInfo )
			
	def onTrapDie( self, trapID ):
		""""""
		if trapID in self.spawnInfo:
			spawnInfo = self.spawnInfo.pop(trapID)
			g_spawnPointFactory.onGameObjectDie( self, spawnInfo )
			
	def onSpellBoxDie( self, spellBoxID ):
		""""""
		if spellBoxID in self.spawnInfo:
			spawnInfo = self.spawnInfo.pop(spellBoxID)
			g_spawnPointFactory.onGameObjectDie( self, spawnInfo )
		
	def onRediviousMonsterCB( self, spawnIndex ):
		"""
		复活怪物回调
		"""
		g_spawnPointFactory.createSpawnEntityByIndex( self, spawnIndex )
	
	def onRediviousChildMonsterCB( self, spawnInfo ):
		"""
		台子上的怪物复活
		"""
		g_spawnPointFactory.onRediviousChildMonsterCB( self, spawnInfo )
		
	def onSpaceSpawnPointLoadOver( self ):
		"""刷新点加载完成回调"""
		self.getScript().onSpaceSpawnPointLoadOver( self )
	
	def callSpawnFunction( self, spawnIndex, methodName, args ):
		"""
		<define method>
		调用某刷新点的某方法
		"""
		for spawnPoint in self.spawnInfo:
			if spawnPoint.getSpawnIndex() != spawnIndex:
				continue
			
			try:
				method = getattr( spawnPoint, methodName )
			except AttributeError as errstr:
				KBEDebug.ERROR_MSG( "Spawn point class(%s) has not method %s." % ( spawnPoint.__class__.__name__, methodName ) )
				return
			method( self, *args )

# -*- coding: utf-8 -*-

# 副本事件行为
import random
import KBEMath
import KBEDebug
import KBEngine
import Const
import Functions
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction68( SEActionBase ):
	"""
	雷域试炼：四周随机刷出雷球
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._posList = []
		self._distList = []
		self._patrolList = []
				
		for posStr in section["param1"].split("|"):
			pos = Functions.vector3TypeConvert( posStr )
			pos = KBEMath.Unreal2KBEnginePosition( pos )
			self._posList.append(pos)
				
		for distStr in section["param2"].split("|"):
			dist = Functions.vector3TypeConvert( distStr )
			dist = KBEMath.Unreal2KBEngineDirection( dist )
			self._distList.append(dist)
			
		for route in section["param3"].split("|"):
			self._patrolList.append( int(route) )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity.scriptID in g_spawnPointFactory.spawnInfo:return
		
		spawnScriptIDs = list( Const.LEI_SCRIPTID_TO_BUFFID.keys() )
		for entityID in spaceEntity.spawnInfo.keys():
			monster = KBEngine.entities.get( entityID, None )
			if monster and monster.scriptID in spawnScriptIDs:
				spawnScriptIDs.remove( monster.scriptID )	# 已经刷出,则不再刷
		
		num = min( len( spawnScriptIDs ), 4 )
		spawnList = random.sample( spawnScriptIDs, num )
		for index, scriptID in enumerate( spawnList ):
			param = {}
			param["position"] = self._posList[index]
			param["direction"] = self._distList[index]
			param["patrolList"] = self._patrolList[index]
			entitys = spaceEntity.spawnPointCreateEntityByScriptID(scriptID, param )
			for entity in entitys:
				speed = float( random.randrange(3,6) )
				entity.setTemp( "runSpeed", speed )
				entity.setTemp( "walkSpeed", speed )
				entity.initSpeed()

SEActionBase.setActionClass("SEAction68", SEAction68)

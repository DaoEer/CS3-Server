# -*- coding: utf-8 -*-

import ObjectScript.Monster.Monster as Monster
import KBEDebug
import csdefine
from ConfigObject import PatrolRouteLoader
import Math

class MonsterExtYXLMSoldier( Monster.Monster ):
	"""
	英雄联盟 小兵
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		pass

	def onEnterReset( self, selfEntity ):
		"""
		进入回走状态
		"""
		for bufIdx in list( selfEntity.getAttrBuffs().keys() ):#回走部分buff不移除 CST-1998
			buffData = selfEntity.getBuffData( bufIdx )
			if buffData and buffData.buffID not in selfEntity.resetKeepBuffs:
				selfEntity.removeBuffByIndex( bufIdx  )
		
		selfEntity.monsterAIReset()
		selfEntity.resetEnemyList()
		selfEntity.changeState( csdefine.ENTITY_STATE_FREE )
		nearestPoint = PatrolRouteLoader.g_patrolRouteLoader.getNearestRoutePoint(selfEntity.getCurrentSpaceScriptID(), selfEntity.patrolRoute,Math.Vector3(selfEntity.position))
		patrolRouteInfo = selfEntity.getCurrentSpacePatrolnfo( selfEntity.patrolRoute )
		nodeInfo = patrolRouteInfo.get( nearestPoint )
		selfEntity.spawnPos = Math.Vector3( nodeInfo[ "position" ] )
		time = selfEntity.position.distTo( selfEntity.spawnPos ) / self.getWalkSpeed(selfEntity)
		if time < 0.1:
			time = 0.1
		selfEntity.addTimerCallBackForScript(time, "checkState", ())
		
	def checkState( self, selfEntity ):
		"""
		"""
		selfEntity.triggerEvent(csdefine.ENTITY_EVENT_ON_ENTER_FREE,[])
		if selfEntity.getState() == csdefine.ENTITY_STATE_FREE:
			selfEntity.monsterAIReTriggerNearTrap()
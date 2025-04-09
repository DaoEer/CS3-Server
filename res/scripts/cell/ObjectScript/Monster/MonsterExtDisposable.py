# -*- coding: utf-8 -*-
#############
#一次性的随从怪物
#############
import Math
import csdefine
import KBEngine
import KBEDebug
import ObjectScript.Monster.Monster as Monster


class MonsterExtDisposable( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def onEnterReset( self, selfEntity ):
		"""
		进入回走状态
		"""
		for buffIndex in list( selfEntity.getAttrBuffs() ):
			buffData = selfEntity.getAttrBuffs()[buffIndex]
			if buffData.buffID not in selfEntity.resetKeepBuffs:
				selfEntity.removeBuff( buffIndex )
		
		selfEntity.monsterAIReset()
		selfEntity.resetEnemyList()
		ownerEntity = selfEntity.getOwnerEntity()
		if not ownerEntity:
			selfEntity.changeState( csdefine.ENTITY_STATE_FREE )
			return
		
		if selfEntity.position.distTo( ownerEntity.position ) >= 3.0:			# 如果怪物的位置距离主人，小于3m直接改变为自由状态
			selfEntity.spawnPos = Math.Vector3(ownerEntity.position)
			selfEntity.moveStart( csdefine.MOVE_TYPE_GOBACK, selfEntity.getSpeed(), False )
		else:
			selfEntity.changeState( csdefine.ENTITY_STATE_FREE )

	def chooseTarget( self, selfEntity):
		"""
		"""
		ownerEntity = selfEntity.getOwnerEntity()
		if not ownerEntity:
			return
		
		#优先选择owner当前的目标
		attackID = ownerEntity.getTargetID()
		if attackID:
			self.setTargetID(attackID)
			return
		
		enemyIDList = [e for e in ownerEntity.enemyList.keys() if selfEntity.monsterAICheckInViewRange(e)]
			
		if not len(enemyIDList):
			selfEntity.changeState(csdefine.ENTITY_STATE_RESET)
			return
		
		minDis = 100000.0
		targetID = 0
		for eID in enemyIDList:
			e = KBEngine.entities.get(eID,None)
			if not e:
				continue
			distance = e.position.flatDistTo( ownerEntity.position )
			if distance<=minDis:
				minDis = distance
				targetID = eID
		
		selfEntity.behControlReset(csdefine.BEHAVIOUR_TYPE_SPELL)
		selfEntity.setTargetID(targetID)



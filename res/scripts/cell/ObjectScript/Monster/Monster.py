# -*- coding: utf-8 -*-

import csdefine
import Math
from ObjectScript.Monster import MonsterBase
import KBEDebug

MIN_DISTANCE_SPAWN_POS = 2.0

class Monster( MonsterBase.MonsterBase ):
	def __init__( self ):
		MonsterBase.MonsterBase.__init__( self )
		self._callRange = 0
		self._callList = []
		self._scoutHeight = 0

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		if configData is not None:
			MonsterBase.MonsterBase.initData( self, configData )
			if "WalkSpeed" in configData:		#走路速度
				self.walkSpeed = float(configData["WalkSpeed"])
			if "RunSpeed" in configData:		#跑步速度
				self.runSpeed = float(configData["RunSpeed"])

			if "callRange" in configData:
				self._callRange = int(configData[ "callRange" ])
			
			if "callList" in configData:
				self._callList = configData["callList"]
			if "deadEffectType" in configData:
				self._deadEffectType = configData["deadEffectType"]
			
			if "ScoutHeight" in configData:
				self._scoutHeight = int( configData["ScoutHeight"] )

			if "Param1" in configData:
				self.param1 = configData["Param1"]

			if "Param2" in configData:
				self.param2 = configData["Param2"]

			if "Param3" in configData:
				self.param3 = configData["Param3"]

			if "Param4" in configData:
				self.param4 = configData["Param4"]

			if "Param5" in configData:
				self.param5 = configData["Param5"]

	def getCallRange( self ):
		return self._callRange

	def getCallList( self ):
		return self._callList

	def getDeadEffectType( self ):
		return self._deadEffectType
	
	def getScoutHeight( self ):
		return self._scoutHeight
	
	def getRunSpeed( self, selfEntity ):
		""""""
		return self.runSpeed
		
	def getWalkSpeed( self, selfEntity ):
		""""""
		return self.walkSpeed
	
	def onAddEnemy( self, selfEntity, entityID ):
		"""
		"""
		#if selfEntity.isState( csdefine.ENTITY_STATE_FREE ):
		#	selfEntity.changeAttackTarget( entityID )
		pass

	def onRemoveEnemy( self, selfEntity, entityID ):
		"""
		"""
		if selfEntity.inDestroying():
			return
		#战斗状态下 敌人列表为空 重置
		if len( selfEntity.enemyList ) == 0 and selfEntity.isState( csdefine.ENTITY_STATE_FIGHT ):
			selfEntity.changeState( csdefine.ENTITY_STATE_RESET )


	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		selfEntity.setHP( selfEntity.HP_Max )
		selfEntity.setMP( selfEntity.MP_Max )
		selfEntity.setBootyOwner( None )
		selfEntity.changeDefaultMove()
		
	def onEnterDead( self, selfEntity ):
		"""
		死亡
		"""
		selfEntity.resetEnemyList()
		selfEntity.delayDestroy( 5 )

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
		#AI心跳在一个tick时间之后开启 在此给个0.2s时间执行AI 之后再回走
		selfEntity.addTimerCallBack(selfEntity.monsterAITickSpeed, "moveGoBack", ())

	def onLeaveReset( self, selfEntity ):
		"""
		离开回走状态
		"""
		pass

	def onEnterShow(self, selfEntity):
		"""
		进入表演状态
		"""
		#取消主动攻击范围
		selfEntity.monsterAICancelAttackTrap()
		selfEntity.setOldMinHPPercent(selfEntity.minHPPercent)
		selfEntity.setMinHPPercent(selfEntity.HP/selfEntity.HP_Max*100)

	def onLeaveShow(self, selfEntity):
		"""
		离开表演状态
		"""
		selfEntity.monsterAIAddAttackTrap()
		selfEntity.setMinHPPercent(selfEntity.oldMinHPPercent)


	def onEnterPead(self, selfEntity):
		"""
		进入未决状态
		"""
		#取消主动攻击范围
		selfEntity.monsterAICancelAttackTrap()

	def onLeavePead(self, selfEntity):
		"""
		离开未决状态
		"""
		if selfEntity.state != csdefine.ENTITY_STATE_SHOW:
			selfEntity.monsterAIReTriggerNearTrap()
			selfEntity.monsterAIAddAttackTrap()
		#初始状态为不可见，离开未决状态时恢复可见
		#if selfEntity.hasFlag(csdefine.FLAG_UNVISIBLE):
			#selfEntity.removeFlag(csdefine.FLAG_UNVISIBLE)
	


	def onEnterStable(self, selfEntity):
		"""
		进入稳定状态
		"""
		pass

	def onLeaveStable(self, selfEntity):
		"""
		离开稳定状态
		"""
		pass




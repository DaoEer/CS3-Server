# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import csdefine
from ConfigObject.MonsterClientAIDataLoader import g_monsterClientAIDataLoader

class MonsterExtJDCY( Monster.Monster ):
	"""
	禁地采药怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )

	def setUpMonsterBaseDatas( self, selfEntity ):
		"""
		设置基本数据
		"""
		monsterDatas = g_monsterClientAIDataLoader.getMonsterBaseData( selfEntity.scriptID )
		if not monsterDatas:
			return
		selfEntity.enemyRange = monsterDatas["enemyRange"]
		selfEntity.distance = monsterDatas["distance"]
		selfEntity.wanderRange = monsterDatas["wanderRange"]
		if monsterDatas["useSkills"]:
			selfEntity.attcakSkills = [int(i) for i in monsterDatas["useSkills"].split("|")]

	def onEnterFight( self, selfEntity ):
		"""
		virtual method
		进入战斗
		"""
		Monster.Monster.onEnterFight( self, selfEntity )
		selfEntity.moveSpeed = self.runSpeed

	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		selfEntity.setHP( selfEntity.HP_Max )
		selfEntity.setMP( selfEntity.MP_Max )
		selfEntity.setBootyOwner( None )

	def onEnterReset( self, selfEntity ):
		"""
		进入回走状态
		"""
		selfEntity.moveSpeed = self.walkSpeed
		for bufIdx in list( selfEntity.getAttrBuffs().keys() ):#回走部分buff不移除 CST-1998
			buffData = selfEntity.getBuffData( bufIdx )
			if buffData and buffData.buffID not in selfEntity.resetKeepBuffs:
				selfEntity.removeBuffByIndex( bufIdx  )
		
		selfEntity.monsterAIReset()
		selfEntity.resetEnemyList()
		time = selfEntity.position.flatDistTo(selfEntity.spawnPos) / self.walkSpeed
		if time > 0:
			selfEntity.addTimerCallBack(time,"changeState",(csdefine.ENTITY_STATE_FREE,))
		else:
			selfEntity.changeState(csdefine.ENTITY_STATE_FREE)

# -*- coding: utf-8 -*-
import KBEngine
import ObjectScript.Monster.Monster as Monster
import csdefine
import Math
import KBEDebug

class MonsterExtYCJMDBoss( Monster.Monster ):
	"""
	CST-8727 勇闯夺命岛Boss
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.deadKeepActionID = ""

	def initData( self, configData ):
		Monster.Monster.initData( self, configData )
		self.deadKeepActionID = configData["Param1"]	#死亡后保持的动作

	def getDeadKeepActionID( self ):
		return self.deadKeepActionID

	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		selfEntity.setBootyOwner( None )
		selfEntity.changeDefaultMove()

	def onEnterReset( self, selfEntity ):
		"""
		进入回走状态
		"""
		selfEntity.monsterAISetTarget(0)
		selfEntity.monsterAIResetEAI()
		selfEntity.resetAIIDLoops()
		selfEntity.resetEnemyList()
		selfEntity.changeState( csdefine.ENTITY_STATE_FREE )
		#AI心跳在一个tick时间之后开启 在此给个0.2s时间执行AI 之后再回走
		#selfEntity.addTimerCallBack(selfEntity.monsterAITickSpeed, "moveGoBack", ())

	def onEnterDead( self, selfEntity ):
		"""
		死亡
		"""
		selfEntity.resetEnemyList()
		selfEntity.monsterAIStop()
		#处理死亡下落
		pos = Math.Vector3(selfEntity.position)
		layers = selfEntity.getCurrentSpace().getScript().getNavmeshLayers()
		for i in range(layers):
			posList = KBEngine.collideVertical( selfEntity.spaceID, selfEntity.layer, selfEntity.position, 0, -50 )
			if posList:
				pos = Math.Vector3(posList[0])
				pos.y += 1.8
				break
		selfEntity.addTimerCallBack( 1.0 , "moveFlyToPoint", ( pos, 3.0, False,False,0.1 ))


# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import MonsterExtMain
import Math
import csdefine
import KBEDebug

class MonsterExtAttackCityLadder( MonsterExtMain.MonsterExtMain ):
	"""
	攻城梯 
	"""
	def __init__( self ):
		MonsterExtMain.MonsterExtMain.__init__( self )
		self.patrolRoute = self.getScript().patrolRoute
		self.isOpenLadder = False

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		MonsterExtMain.MonsterExtMain.CELL_onClientReady( self, srcEntityID )
		if self.isOpenLadder:
			player = KBEngine.entities.get( srcEntityID )
			if not player or not player.getClient():
				return
			if player.clientEntity( self.id ):
				player.clientEntity( self.id ).CLIENT_LadderMoveFinish( self.getScript().actionID )

	def onAddEnemy( self, entityID ):
		"""
		重载此方法，添加敌人时不会进入战斗状态
		"""
		self.onEnemyListChange( entityID )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_ATTACK_LADDER)

	def CELL_operationLadder( self, srcEntityID ):
		"""
		操作攻城梯
		"""
		self.isOperationLadder = 1
		self.addBuff( self, self.getScript().beginAddBuffID )
		self.addTimerCallBack(self.getScript().delyTimeMove,"startMove",())
		try:
			space = self.getCurrentSpace()
			space.recordOpterationMachine(self.id)
		except:
			KBEDebug.INFO_MSG("This use in SpaceCopyAtackCityWar!")

	def startMove( self ):
		if self.patrolRoute:
			self.startPatrol(self.getSpeed(),True)
			
	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		MonsterExtMain.MonsterExtMain.onMoveOver( self, controllerID, userData )
		if not self.isOpenLadder and self.getState() != csdefine.ENTITY_STATE_DEAD:
			self.isOpenLadder = True
			self.addBuff( self, self.getScript().endAddBuffID )
			#self.initActionId = self.getScript().actionID
			self.allClients.CLIENT_LadderMoveFinish( self.getScript().actionID )
			try:
				space = self.getCurrentSpace()
				space.removeOpterationMachine(self.id)
			except:
				KBEDebug.INFO_MSG("This use in SpaceCopyAtackCityWar!")
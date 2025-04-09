# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import Math
import csdefine
import KBEDebug

class MonsterExtAerialLadder( Monster.Monster ):
	"""
	云梯 
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		Monster.Monster.CELL_onClientReady( self, srcEntityID )
		if self.getAerialLadderState() == csdefine.AERIAL_LADDER_STATE_BUILD_SUCCESS:
			player = KBEngine.entities.get( srcEntityID )
			if not player or not player.getClient():
				return
			if player.clientEntity( self.id ):
				player.clientEntity( self.id ).CLIENT_EnterAerialLadderAOI( self.getScript().leaveTopOffset,self.getScript().climbLadderSpeed )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_AERIAL_LADDER)

	def onAddEnemy( self, entityID ):
		"""
		重载此方法，添加敌人时不会进入战斗状态
		"""
		self.onEnemyListChange( entityID )

	def setFollowerID( self, followerID ):
		"""
		设置跟随ID
		"""
		self.followerID = followerID
		role = KBEngine.entities.get(self.followerID,None)
		if role:
			role.setTemp( "callAerialLadder",self.id )
		self.changeAerialLadderState( csdefine.AERIAL_LADDER_STATE_FOLLOWER )

	def getFollowerID( self ):
		"""
		获得跟随ID
		"""
		return self.followerID

	def getAerialLadderState( self ):
		"""
		获得云梯的状态
		"""
		return self.ladderState

	def changeAerialLadderState( self, ladderState ):
		"""
		改变云梯的状态
		"""
		try:
			if ladderState == csdefine.AERIAL_LADDER_STATE_FOLLOWER:
				space = self.getCurrentSpace()
				space.recordOpterationMachine(self.id)
			else:
				space = self.getCurrentSpace()
				space.removeOpterationMachine(self.id)
		except:
			KBEDebug.INFO_MSG("This use in SpaceCopyAtackCityWar!")
			
		self.ladderState = ladderState
		self.onAerialLadderStateChange()

	def onAerialLadderStateChange( self ):
		"""
		"""
		if self.ladderState == csdefine.AERIAL_LADDER_STATE_BUILD:
			role = KBEngine.entities.get(self.followerID,None)
			if role:
				role.removeTemp( "callAerialLadder" )
			spaceEntity = self.getCurrentSpace()
			if not spaceEntity:
				self.destroySelf()
				return

			index,pos = spaceEntity.getAerialLadderOccurInfo( self.position )
			self.ladderPosIndex = index
			self.gotoPosition( pos )

	def getLadderPosIndex( self ):
		"""
		"""
		return self.ladderPosIndex

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		Monster.Monster.onMoveOver( self, controllerID, userData )
		if self.ladderState == csdefine.AERIAL_LADDER_STATE_BUILD:
			spaceEntity = self.getCurrentSpace()
			if not spaceEntity:
				return
			dir = spaceEntity.getScript().getAerialLadderDirInfo( self.ladderPosIndex )
			if dir == None:
				dir = self.direction
			self.changeDirection( dir )
			self.initActionId = self.getScript().initActionID
			self.allClients.CLIENT_AerialLadderMoveFinish( self.getScript().finishActionID, self.getScript().leaveTopOffset,self.getScript().climbLadderSpeed )

	def CELL_LadderBuildComplete( self, srcEntityID ):
		"""
		云梯搭建完毕
		"""
		self.ladderState = csdefine.AERIAL_LADDER_STATE_BUILD_SUCCESS
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			self.destroySelf()
			return

		spaceEntity.addAerialLadderPosIndex( self.ladderPosIndex )

	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		Monster.Monster.beforeDestroy( self )
		if self.getAerialLadderState() == csdefine.AERIAL_LADDER_STATE_BUILD_SUCCESS:
			spaceEntity = self.getCurrentSpace()
			if not spaceEntity:
				return
			spaceEntity.removeAerialLadderPosIndex( self.ladderPosIndex )

	def aerialLadderReadyToFall( self ):
		"""
		梯子被推到
		"""
		self.allClients.CLIENT_AerialLadderReadyToFall( self.getScript().fallActionID )

	def CELL_LadderFallDead( self, srcEntityID, fallEntityIDs ):
		"""
		梯子倒下时 计算伤害
		"""
		for fallEntityID in fallEntityIDs:
			entity = KBEngine.entities.get( fallEntityID, None )
			if not entity:
				continue
			if entity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
				entity.startFallLand()


	def CELL_LadderFallActionFinish( self, srcEntityID ):
		"""
		梯子完全倒下
		"""
		self.destroySelf()

	def CELL_EntityEnterLadder( self, srcEntityID, enterID ):
		"""
		进入梯子 该动作表 变身姿势
		"""
		if srcEntityID != enterID:
			return
		entity = KBEngine.entities.get( enterID,None )
		if entity:
			entity.addBuff( entity,self.getScript().buffID )

	def CELL_EntityExitLadder( self, srcEntityID, leaveID ):
		"""
		离开梯子 还原动作表
		"""
		if srcEntityID != leaveID:
			return
		entity = KBEngine.entities.get( leaveID,None )
		if entity:
			entity.removeBuffByID( self.getScript().buffID )
			if entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and entity.getClient():
				entity.client.CLIENT_ChangeReadyToClimbLadder(0)

	def CELL_RoleReadyClimbLadder( self, srcEntityID ):
		"""
		玩家准备开始爬梯子
		"""
		player = KBEngine.entities.get( srcEntityID, None )
		if player.getClient():
			player.client.CLIENT_ChangeReadyToClimbLadder(1)

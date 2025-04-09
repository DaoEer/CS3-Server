# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine
import KBEMath
import Functions
import csdefine

class SpaceCopyQiJueLing( SpaceCopy ):
	"""
	七绝岭
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.platScriptIDList = []  #台子对应的释放毒物的scriptID  顺序为从左至右
		self.skillPoisonIDList = [] #毒物技能的ID列表

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.platScriptIDList = configData["SpaceData"]["scriptIDList"].split("|")
		#self.skillPoisonIDList = configData["SpaceData"][""]

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		KBEngine.globalData["QiJueLingManager"].onSpaceCreate( selfEntity.spaceKey, selfEntity.base )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.setPkMode( csdefine.PK_MODE_PEACE )
		playerRole.lockPkMode()
		playerRole.setTemp("CurrentMPMax",playerRole.MP_Max)
		playerRole.setTemp("CurrentHPMax",playerRole.HP_Max)
		playerRole.HP_Max = playerRole.HP_Max * 3
		playerRole.MP_Max = playerRole.MP_Max * 3
		playerRole.setHP(playerRole.HP_Max)
		playerRole.setMP(playerRole.MP_Max)

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		playerRole.setPkMode( csdefine.PK_MODE_RIGHTFUL )
		playerRole.unLockPkMode()
		mpMax = playerRole.queryTemp("CurrentMPMax")
		hpMax = playerRole.queryTemp("CurrentHPMax")
		if mpMax:
			playerRole.MP_Max = mpMax
			playerRole.setMP(mpMax)
		if hpMax:
			playerRole.HP_Max = hpMax
			playerRole.setHP(hpMax)
		KBEngine.globalData["QiJueLingManager"].onPlayerLeaveSpace( selfEntity.spaceKey, playerRole.playerDBID )

	def onTeleportCompleted( self, selfEntity, playerRole ):
		"""
		传送完毕
		"""
		SpaceCopy.onTeleportCompleted( self, selfEntity, playerRole )
		KBEngine.globalData["QiJueLingManager"].onPlayerTeleportReady( selfEntity.spaceKey, playerRole.playerDBID )

	def enterFightProcess( self, selfEntity ):
		"""
		进入战斗  所有玩家进入恶意模式
		"""
		for player in selfEntity._spaceRoles:
			player.setPkMode( csdefine.PK_MODE_SLAUGHTER )
			player.lockPkMode()

	def onPlayerDie( self, selfEntity, playerID, playerMB ):
		"""
		玩家死亡
		"""
		SpaceCopy.onPlayerDie( self, selfEntity, playerID, playerMB )
		KBEngine.globalData["QiJueLingManager"].onPlayerDie( playerMB.playerDBID )

	def releasePoison( self, selfEntity, stageType ):
		"""
		释放毒物
		"""
		#自己对自己释放毒物技能
		pass

	def onPlatFightOver( self, selfEntity, platNumber ):
		"""
		一个平台的战斗结束
		"""
		scriptID = self.platScriptIDList[platNumber - 1]
		entity = selfEntity.getEntityRecord(scriptID)
		entity.destroySelf()
